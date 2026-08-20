#!/usr/bin/env python3
"""
Advanced PyDoc Generator and Code Descriptor
Generates comprehensive documentation and analysis for Python codebases
"""

import ast
import os
import re
import inspect
import pydoc
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any, Union
from collections import defaultdict, Counter
import json
import sys
import importlib.util


@dataclass
class FunctionDoc:
    """Comprehensive function documentation"""
    name: str
    file_path: str
    line_number: int
    docstring: Optional[str] = None
    signature: str = ""
    parameters: List[Dict[str, Any]] = field(default_factory=list)
    return_annotation: Optional[str] = None
    return_description: Optional[str] = None
    examples: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    see_also: List[str] = field(default_factory=list)
    complexity: int = 0
    lines_of_code: int = 0
    is_async: bool = False
    is_generator: bool = False
    is_class_method: bool = False
    is_static_method: bool = False
    decorators: List[str] = field(default_factory=list)
    calls_made: Set[str] = field(default_factory=set)
    imports_used: Set[str] = field(default_factory=set)
    error_handling: List[str] = field(default_factory=list)
    performance_notes: List[str] = field(default_factory=list)


@dataclass
class ClassDoc:
    """Comprehensive class documentation"""
    name: str
    file_path: str
    line_number: int
    docstring: Optional[str] = None
    base_classes: List[str] = field(default_factory=list)
    methods: List[FunctionDoc] = field(default_factory=list)
    properties: List[Dict[str, Any]] = field(default_factory=list)
    attributes: List[Dict[str, Any]] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)
    inheritance_diagram: str = ""
    is_abstract: bool = False
    is_dataclass: bool = False
    is_enum: bool = False
    complexity: int = 0
    lines_of_code: int = 0


@dataclass
class ModuleDoc:
    """Comprehensive module documentation"""
    name: str
    file_path: str
    docstring: Optional[str] = None
    functions: List[FunctionDoc] = field(default_factory=list)
    classes: List[ClassDoc] = field(default_factory=list)
    constants: List[Dict[str, Any]] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)
    exports: List[str] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)
    dependencies: Set[str] = field(default_factory=set)
    is_package: bool = False
    is_main_module: bool = False
    lines_of_code: int = 0
    complexity: int = 0


class PyDocGenerator:
    """Advanced PyDoc-style documentation generator"""
    
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.modules: List[ModuleDoc] = []
        self.functions: List[FunctionDoc] = []
        self.classes: List[ClassDoc] = []
        self.documentation: Dict[str, Any] = {}
        
        # Documentation templates
        self.templates = {
            'function': self._generate_function_doc,
            'class': self._generate_class_doc,
            'module': self._generate_module_doc
        }
    
    def generate_documentation(self) -> Dict[str, Any]:
        """Generate comprehensive documentation for the codebase"""
        print("📚 Generating PyDoc-style documentation...")
        
        # Find all Python files
        python_files = list(self.root_dir.rglob("*.py"))
        print(f"   Found {len(python_files)} Python files")
        
        # Analyze each file
        for file_path in python_files:
            try:
                self._analyze_file(file_path)
            except Exception as e:
                print(f"   ⚠️  Error analyzing {file_path}: {e}")
        
        # Generate documentation
        self._generate_all_documentation()
        
        return {
            'modules': self.modules,
            'functions': self.functions,
            'classes': self.classes,
            'documentation': self.documentation,
            'summary': self._generate_summary()
        }
    
    def _analyze_file(self, file_path: Path):
        """Analyze a single Python file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            # Create module documentation
            module = ModuleDoc(
                name=file_path.stem,
                file_path=str(file_path),
                lines_of_code=len(content.splitlines()),
                is_main_module=file_path.name == '__main__.py',
                is_package=file_path.name == '__init__.py'
            )
            
            # Extract module docstring
            if (tree.body and 
                isinstance(tree.body[0], ast.Expr) and 
                isinstance(tree.body[0].value, ast.Constant) and
                isinstance(tree.body[0].value.value, str)):
                module.docstring = tree.body[0].value.value
            
            # Analyze AST nodes
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_doc = self._analyze_function(node, file_path)
                    module.functions.append(func_doc)
                    self.functions.append(func_doc)
                
                elif isinstance(node, ast.AsyncFunctionDef):
                    func_doc = self._analyze_function(node, file_path, is_async=True)
                    module.functions.append(func_doc)
                    self.functions.append(func_doc)
                
                elif isinstance(node, ast.ClassDef):
                    class_doc = self._analyze_class(node, file_path)
                    module.classes.append(class_doc)
                    self.classes.append(class_doc)
                
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    import_name = self._extract_import_name(node)
                    if import_name:
                        module.imports.append(import_name)
                        module.dependencies.add(import_name.split('.')[0])
            
            self.modules.append(module)
            
        except SyntaxError as e:
            print(f"   ⚠️  Syntax error in {file_path}: {e}")
        except Exception as e:
            print(f"   ⚠️  Error parsing {file_path}: {e}")
    
    def _analyze_function(self, node: ast.FunctionDef, file_path: Path, is_async: bool = False) -> FunctionDoc:
        """Analyze a function and create comprehensive documentation"""
        func_doc = FunctionDoc(
            name=node.name,
            file_path=str(file_path),
            line_number=node.lineno,
            is_async=is_async,
            is_generator=isinstance(node, ast.AsyncFunctionDef) or 
                       any(isinstance(n, ast.Yield) for n in ast.walk(node)),
            is_class_method=any(isinstance(parent, ast.ClassDef) for parent in ast.walk(node)),
            lines_of_code=node.end_lineno - node.lineno + 1 if hasattr(node, 'end_lineno') else 0
        )
        
        # Extract docstring
        if (node.body and 
            isinstance(node.body[0], ast.Expr) and 
            isinstance(node.body[0].value, ast.Constant) and
            isinstance(node.body[0].value.value, str)):
            func_doc.docstring = node.body[0].value.value
        
        # Extract signature
        func_doc.signature = self._generate_function_signature(node)
        
        # Extract parameters
        func_doc.parameters = self._extract_parameters(node)
        
        # Extract return annotation
        if node.returns:
            func_doc.return_annotation = ast.unparse(node.returns) if hasattr(ast, 'unparse') else str(node.returns)
        
        # Extract decorators
        for decorator in node.decorator_list:
            if hasattr(ast, 'unparse'):
                func_doc.decorators.append(ast.unparse(decorator))
            else:
                func_doc.decorators.append(str(decorator))
        
        # Calculate complexity
        func_doc.complexity = self._calculate_cyclomatic_complexity(node)
        
        # Extract function calls and imports
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name):
                    func_doc.calls_made.add(child.func.id)
                elif isinstance(child.func, ast.Attribute):
                    func_doc.calls_made.add(child.func.attr)
        
        # Analyze error handling
        func_doc.error_handling = self._analyze_error_handling(node)
        
        # Generate performance notes
        func_doc.performance_notes = self._analyze_performance(node)
        
        return func_doc
    
    def _analyze_class(self, node: ast.ClassDef, file_path: Path) -> ClassDoc:
        """Analyze a class and create comprehensive documentation"""
        class_doc = ClassDoc(
            name=node.name,
            file_path=str(file_path),
            line_number=node.lineno,
            lines_of_code=node.end_lineno - node.lineno + 1 if hasattr(node, 'end_lineno') else 0
        )
        
        # Extract docstring
        if (node.body and 
            isinstance(node.body[0], ast.Expr) and 
            isinstance(node.body[0].value, ast.Constant) and
            isinstance(node.body[0].value.value, str)):
            class_doc.docstring = node.body[0].value.value
        
        # Extract base classes
        for base in node.bases:
            if hasattr(ast, 'unparse'):
                class_doc.base_classes.append(ast.unparse(base))
            else:
                class_doc.base_classes.append(str(base))
        
        # Check for special class types
        class_doc.is_abstract = any('abstract' in dec for dec in [str(d) for d in node.decorator_list])
        class_doc.is_dataclass = any('dataclass' in dec for dec in [str(d) for d in node.decorator_list])
        class_doc.is_enum = any('Enum' in base for base in class_doc.base_classes)
        
        # Analyze methods
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                method_doc = self._analyze_function(item, file_path)
                method_doc.is_class_method = True
                method_doc.is_static_method = any('staticmethod' in dec for dec in method_doc.decorators)
                class_doc.methods.append(method_doc)
        
        # Calculate complexity
        class_doc.complexity = sum(method.complexity for method in class_doc.methods)
        
        return class_doc
    
    def _extract_import_name(self, node: ast.Import) -> Optional[str]:
        """Extract import name from import node"""
        if isinstance(node, ast.Import):
            return node.names[0].name if node.names else None
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                return node.module
            elif node.names:
                return node.names[0].name
        return None
    
    def _generate_function_signature(self, node: ast.FunctionDef) -> str:
        """Generate function signature string"""
        params = []
        for arg in node.args.args:
            param = arg.arg
            if arg.annotation:
                param += f": {ast.unparse(arg.annotation) if hasattr(ast, 'unparse') else str(arg.annotation)}"
            params.append(param)
        
        signature = f"{node.name}({', '.join(params)})"
        
        if node.returns:
            signature += f" -> {ast.unparse(node.returns) if hasattr(ast, 'unparse') else str(node.returns)}"
        
        return signature
    
    def _extract_parameters(self, node: ast.FunctionDef) -> List[Dict[str, Any]]:
        """Extract detailed parameter information"""
        parameters = []
        
        for arg in node.args.args:
            param = {
                'name': arg.arg,
                'type': None,
                'default': None,
                'description': None
            }
            
            if arg.annotation:
                param['type'] = ast.unparse(arg.annotation) if hasattr(ast, 'unparse') else str(arg.annotation)
            
            parameters.append(param)
        
        return parameters
    
    def _calculate_cyclomatic_complexity(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity"""
        complexity = 1
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        
        return complexity
    
    def _analyze_error_handling(self, node: ast.FunctionDef) -> List[str]:
        """Analyze error handling patterns"""
        error_patterns = []
        
        for child in ast.walk(node):
            if isinstance(child, ast.Try):
                error_patterns.append("Uses try-except blocks")
            elif isinstance(child, ast.Raise):
                error_patterns.append("Raises exceptions")
            elif isinstance(child, ast.Assert):
                error_patterns.append("Uses assertions")
        
        return error_patterns
    
    def _analyze_performance(self, node: ast.FunctionDef) -> List[str]:
        """Analyze performance characteristics"""
        performance_notes = []
        
        for child in ast.walk(node):
            if isinstance(child, ast.For):
                performance_notes.append("Contains loops - consider vectorization")
            elif isinstance(child, ast.ListComp):
                performance_notes.append("Uses list comprehension - good performance")
            elif isinstance(child, ast.GeneratorExp):
                performance_notes.append("Uses generator expression - memory efficient")
            elif isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                if child.func.id in ['sleep', 'time.sleep']:
                    performance_notes.append("Contains blocking operations")
        
        return performance_notes
    
    def _generate_all_documentation(self):
        """Generate comprehensive documentation for all analyzed components"""
        print("   📝 Generating documentation...")
        
        # Generate module documentation
        for module in self.modules:
            self.documentation[f"module_{module.name}"] = self._generate_module_doc(module)
        
        # Generate function documentation
        for func in self.functions:
            self.documentation[f"function_{func.name}"] = self._generate_function_doc(func)
        
        # Generate class documentation
        for cls in self.classes:
            self.documentation[f"class_{cls.name}"] = self._generate_class_doc(cls)
    
    def _generate_module_doc(self, module: ModuleDoc) -> str:
        """Generate module documentation"""
        doc = f"MODULE: {module.name}\n"
        doc += "=" * (len(module.name) + 8) + "\n\n"
        
        if module.docstring:
            doc += f"DESCRIPTION:\n{module.docstring}\n\n"
        
        doc += f"FILE: {module.file_path}\n"
        doc += f"LINES OF CODE: {module.lines_of_code}\n"
        doc += f"COMPLEXITY: {module.complexity}\n\n"
        
        if module.functions:
            doc += "FUNCTIONS:\n"
            doc += "-" * 10 + "\n"
            for func in module.functions:
                doc += f"  {func.name}() - Line {func.line_number}\n"
                if func.docstring:
                    doc += f"    {func.docstring.split('.')[0]}...\n"
            doc += "\n"
        
        if module.classes:
            doc += "CLASSES:\n"
            doc += "-" * 7 + "\n"
            for cls in module.classes:
                doc += f"  {cls.name} - Line {cls.line_number}\n"
                if cls.docstring:
                    doc += f"    {cls.docstring.split('.')[0]}...\n"
            doc += "\n"
        
        if module.imports:
            doc += "IMPORTS:\n"
            doc += "-" * 7 + "\n"
            for imp in module.imports[:10]:  # Limit to first 10
                doc += f"  {imp}\n"
            if len(module.imports) > 10:
                doc += f"  ... and {len(module.imports) - 10} more\n"
            doc += "\n"
        
        return doc
    
    def _generate_function_doc(self, func: FunctionDoc) -> str:
        """Generate function documentation"""
        doc = f"FUNCTION: {func.name}\n"
        doc += "=" * (len(func.name) + 10) + "\n\n"
        
        doc += f"SIGNATURE: {func.signature}\n"
        doc += f"FILE: {func.file_path}\n"
        doc += f"LINE: {func.line_number}\n"
        doc += f"COMPLEXITY: {func.complexity}\n"
        doc += f"LINES OF CODE: {func.lines_of_code}\n\n"
        
        if func.docstring:
            doc += "DESCRIPTION:\n"
            doc += func.docstring + "\n\n"
        
        if func.parameters:
            doc += "PARAMETERS:\n"
            doc += "-" * 11 + "\n"
            for param in func.parameters:
                doc += f"  {param['name']}"
                if param['type']:
                    doc += f" ({param['type']})"
                doc += "\n"
            doc += "\n"
        
        if func.return_annotation:
            doc += f"RETURNS: {func.return_annotation}\n\n"
        
        if func.decorators:
            doc += "DECORATORS:\n"
            doc += "-" * 10 + "\n"
            for decorator in func.decorators:
                doc += f"  @{decorator}\n"
            doc += "\n"
        
        if func.error_handling:
            doc += "ERROR HANDLING:\n"
            doc += "-" * 14 + "\n"
            for error in func.error_handling:
                doc += f"  • {error}\n"
            doc += "\n"
        
        if func.performance_notes:
            doc += "PERFORMANCE NOTES:\n"
            doc += "-" * 17 + "\n"
            for note in func.performance_notes:
                doc += f"  • {note}\n"
            doc += "\n"
        
        if func.calls_made:
            doc += "FUNCTION CALLS:\n"
            doc += "-" * 14 + "\n"
            for call in sorted(func.calls_made)[:10]:  # Limit to first 10
                doc += f"  {call}()\n"
            if len(func.calls_made) > 10:
                doc += f"  ... and {len(func.calls_made) - 10} more\n"
            doc += "\n"
        
        return doc
    
    def _generate_class_doc(self, cls: ClassDoc) -> str:
        """Generate class documentation"""
        doc = f"CLASS: {cls.name}\n"
        doc += "=" * (len(cls.name) + 7) + "\n\n"
        
        doc += f"FILE: {cls.file_path}\n"
        doc += f"LINE: {cls.line_number}\n"
        doc += f"COMPLEXITY: {cls.complexity}\n"
        doc += f"LINES OF CODE: {cls.lines_of_code}\n\n"
        
        if cls.docstring:
            doc += "DESCRIPTION:\n"
            doc += cls.docstring + "\n\n"
        
        if cls.base_classes:
            doc += "INHERITANCE:\n"
            doc += "-" * 12 + "\n"
            doc += f"  Inherits from: {', '.join(cls.base_classes)}\n\n"
        
        if cls.methods:
            doc += "METHODS:\n"
            doc += "-" * 7 + "\n"
            for method in cls.methods:
                doc += f"  {method.name}() - Line {method.line_number}\n"
                if method.docstring:
                    doc += f"    {method.docstring.split('.')[0]}...\n"
            doc += "\n"
        
        if cls.is_abstract:
            doc += "NOTE: This is an abstract class\n\n"
        if cls.is_dataclass:
            doc += "NOTE: This is a dataclass\n\n"
        if cls.is_enum:
            doc += "NOTE: This is an enum class\n\n"
        
        return doc
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate documentation summary"""
        total_functions = len(self.functions)
        total_classes = len(self.classes)
        total_modules = len(self.modules)
        
        functions_with_docs = sum(1 for f in self.functions if f.docstring)
        classes_with_docs = sum(1 for c in self.classes if c.docstring)
        modules_with_docs = sum(1 for m in self.modules if m.docstring)
        
        return {
            'total_modules': total_modules,
            'total_functions': total_functions,
            'total_classes': total_classes,
            'documentation_coverage': {
                'modules': f"{modules_with_docs}/{total_modules} ({modules_with_docs/total_modules*100:.1f}%)" if total_modules > 0 else "0/0 (0%)",
                'functions': f"{functions_with_docs}/{total_functions} ({functions_with_docs/total_functions*100:.1f}%)" if total_functions > 0 else "0/0 (0%)",
                'classes': f"{classes_with_docs}/{total_classes} ({classes_with_docs/total_classes*100:.1f}%)" if total_classes > 0 else "0/0 (0%)"
            },
            'average_complexity': sum(f.complexity for f in self.functions) / max(total_functions, 1),
            'most_complex_functions': sorted(self.functions, key=lambda x: x.complexity, reverse=True)[:5],
            'largest_functions': sorted(self.functions, key=lambda x: x.lines_of_code, reverse=True)[:5]
        }
    
    def export_documentation(self, output_dir: str = "documentation"):
        """Export documentation to files"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        print(f"📁 Exporting documentation to {output_dir}...")
        
        # Export individual documentation files
        for key, doc in self.documentation.items():
            file_path = output_path / f"{key}.txt"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(doc)
        
        # Export summary
        summary_path = output_path / "summary.json"
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(self._generate_summary(), f, indent=2, default=str)
        
        # Export HTML documentation
        self._export_html_documentation(output_path)
        
        print(f"   ✅ Documentation exported to {output_dir}")
    
    def _export_html_documentation(self, output_path: Path):
        """Export HTML documentation"""
        html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Python Code Documentation</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .module { margin-bottom: 30px; border: 1px solid #ccc; padding: 15px; }
        .function { margin-bottom: 20px; border-left: 3px solid #007acc; padding-left: 10px; }
        .class { margin-bottom: 20px; border-left: 3px solid #28a745; padding-left: 10px; }
        .signature { font-family: monospace; background: #f5f5f5; padding: 5px; }
        .complexity { color: #dc3545; font-weight: bold; }
        .low-complexity { color: #28a745; }
        .medium-complexity { color: #ffc107; }
        .high-complexity { color: #dc3545; }
    </style>
</head>
<body>
    <h1>Python Code Documentation</h1>
"""
        
        # Add modules
        for module in self.modules:
            html_content += f"""
    <div class="module">
        <h2>Module: {module.name}</h2>
        <p><strong>File:</strong> {module.file_path}</p>
        <p><strong>Lines of Code:</strong> {module.lines_of_code}</p>
        {f'<p><strong>Description:</strong> {module.docstring}</p>' if module.docstring else ''}
        
        <h3>Functions ({len(module.functions)})</h3>
"""
            for func in module.functions:
                complexity_class = "low-complexity" if func.complexity < 5 else "medium-complexity" if func.complexity < 10 else "high-complexity"
                html_content += f"""
        <div class="function">
            <h4>{func.name}() <span class="complexity {complexity_class}">[Complexity: {func.complexity}]</span></h4>
            <div class="signature">{func.signature}</div>
            {f'<p>{func.docstring}</p>' if func.docstring else ''}
        </div>
"""
            
            html_content += f"""
        <h3>Classes ({len(module.classes)})</h3>
"""
            for cls in module.classes:
                html_content += f"""
        <div class="class">
            <h4>{cls.name}</h4>
            {f'<p>{cls.docstring}</p>' if cls.docstring else ''}
            <p><strong>Methods:</strong> {len(cls.methods)}</p>
        </div>
"""
            
            html_content += "    </div>"
        
        html_content += """
</body>
</html>
"""
        
        with open(output_path / "index.html", 'w', encoding='utf-8') as f:
            f.write(html_content)


def main():
    """Main function for testing"""
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python pydoc_generator.py <directory>")
        sys.exit(1)
    
    generator = PyDocGenerator(sys.argv[1])
    results = generator.generate_documentation()
    
    print("\n📚 Documentation Generated:")
    print(f"   📁 Modules: {results['summary']['total_modules']}")
    print(f"   🔧 Functions: {results['summary']['total_functions']}")
    print(f"   🏗️  Classes: {results['summary']['total_classes']}")
    print(f"   📝 Documentation Coverage: {results['summary']['documentation_coverage']}")
    
    # Export documentation
    generator.export_documentation("python_documentation")


if __name__ == "__main__":
    main()