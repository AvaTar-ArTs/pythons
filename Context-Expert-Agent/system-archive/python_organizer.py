#!/usr/bin/env python3
"""
Python Code Organizer and Describer
Advanced analysis and organization system for Python codebases
"""

import ast
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
from collections import defaultdict, Counter
import json


@dataclass
class PythonFunction:
    """Represents a Python function with metadata"""
    name: str
    file_path: str
    line_number: int
    docstring: Optional[str] = None
    parameters: List[str] = field(default_factory=list)
    return_type: Optional[str] = None
    complexity: int = 0
    lines_of_code: int = 0
    imports_used: Set[str] = field(default_factory=set)
    calls_made: Set[str] = field(default_factory=set)
    is_async: bool = False
    is_generator: bool = False
    is_class_method: bool = False
    is_static_method: bool = False
    decorators: List[str] = field(default_factory=list)


@dataclass
class PythonClass:
    """Represents a Python class with metadata"""
    name: str
    file_path: str
    line_number: int
    docstring: Optional[str] = None
    methods: List[PythonFunction] = field(default_factory=list)
    attributes: List[str] = field(default_factory=list)
    base_classes: List[str] = field(default_factory=list)
    is_abstract: bool = False
    complexity: int = 0
    lines_of_code: int = 0


@dataclass
class PythonModule:
    """Represents a Python module with metadata"""
    file_path: str
    name: str
    docstring: Optional[str] = None
    functions: List[PythonFunction] = field(default_factory=list)
    classes: List[PythonClass] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)
    exports: List[str] = field(default_factory=list)
    dependencies: Set[str] = field(default_factory=set)
    lines_of_code: int = 0
    complexity: int = 0
    is_main_module: bool = False
    is_package: bool = False


@dataclass
class CodePattern:
    """Represents a code pattern or anti-pattern"""
    pattern_type: str
    description: str
    severity: str  # 'low', 'medium', 'high', 'critical'
    file_path: str
    line_number: int
    suggestion: str
    category: str  # 'performance', 'security', 'maintainability', 'style'


class PythonOrganizer:
    """Advanced Python code organizer and analyzer"""
    
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.modules: List[PythonModule] = []
        self.functions: List[PythonFunction] = []
        self.classes: List[PythonClass] = []
        self.patterns: List[CodePattern] = []
        self.import_graph: Dict[str, Set[str]] = defaultdict(set)
        self.dependency_tree: Dict[str, Set[str]] = defaultdict(set)
        self.code_metrics: Dict[str, Any] = {}
        
        # Pattern detection rules
        self.anti_patterns = {
            'long_function': {'threshold': 50, 'severity': 'medium'},
            'deep_nesting': {'threshold': 4, 'severity': 'high'},
            'duplicate_code': {'threshold': 0.8, 'severity': 'high'},
            'complex_expression': {'threshold': 10, 'severity': 'medium'},
            'missing_docstring': {'severity': 'low'},
            'unused_import': {'severity': 'low'},
            'hardcoded_values': {'severity': 'medium'},
            'exception_broad_catch': {'severity': 'medium'},
        }
    
    def analyze_codebase(self) -> Dict[str, Any]:
        """Perform comprehensive analysis of the Python codebase"""
        print("🔍 Analyzing Python codebase...")
        
        # Find all Python files
        python_files = list(self.root_dir.rglob("*.py"))
        print(f"   Found {len(python_files)} Python files")
        
        # Analyze each file
        for file_path in python_files:
            try:
                self._analyze_file(file_path)
            except Exception as e:
                print(f"   ⚠️  Error analyzing {file_path}: {e}")
        
        # Build dependency graph
        self._build_dependency_graph()
        
        # Detect patterns and anti-patterns
        self._detect_patterns()
        
        # Calculate metrics
        self._calculate_metrics()
        
        # Generate organization suggestions
        suggestions = self._generate_organization_suggestions()
        
        return {
            'modules': self.modules,
            'functions': self.functions,
            'classes': self.classes,
            'patterns': self.patterns,
            'import_graph': dict(self.import_graph),
            'dependency_tree': dict(self.dependency_tree),
            'metrics': self.code_metrics,
            'suggestions': suggestions,
            'summary': self._generate_summary()
        }
    
    def _analyze_file(self, file_path: Path):
        """Analyze a single Python file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            # Create module
            module = PythonModule(
                file_path=str(file_path),
                name=file_path.stem,
                lines_of_code=len(content.splitlines()),
                is_main_module=file_path.name == '__main__.py',
                is_package=file_path.name == '__init__.py'
            )
            
            # Extract docstring
            if (tree.body and 
                isinstance(tree.body[0], ast.Expr) and 
                isinstance(tree.body[0].value, ast.Constant) and
                isinstance(tree.body[0].value.value, str)):
                module.docstring = tree.body[0].value.value
            
            # Analyze AST nodes
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func = self._analyze_function(node, file_path)
                    module.functions.append(func)
                    self.functions.append(func)
                
                elif isinstance(node, ast.AsyncFunctionDef):
                    func = self._analyze_function(node, file_path, is_async=True)
                    module.functions.append(func)
                    self.functions.append(func)
                
                elif isinstance(node, ast.ClassDef):
                    cls = self._analyze_class(node, file_path)
                    module.classes.append(cls)
                    self.classes.append(cls)
                
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
    
    def _analyze_function(self, node: ast.FunctionDef, file_path: Path, is_async: bool = False) -> PythonFunction:
        """Analyze a function definition"""
        func = PythonFunction(
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
            func.docstring = node.body[0].value.value
        
        # Extract parameters
        for arg in node.args.args:
            func.parameters.append(arg.arg)
        
        # Extract return type annotation
        if node.returns:
            func.return_type = ast.unparse(node.returns) if hasattr(ast, 'unparse') else str(node.returns)
        
        # Extract decorators
        for decorator in node.decorator_list:
            if hasattr(ast, 'unparse'):
                func.decorators.append(ast.unparse(decorator))
            else:
                func.decorators.append(str(decorator))
        
        # Calculate complexity
        func.complexity = self._calculate_cyclomatic_complexity(node)
        
        # Extract function calls and imports
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name):
                    func.calls_made.add(child.func.id)
                elif isinstance(child.func, ast.Attribute):
                    func.calls_made.add(child.func.attr)
        
        return func
    
    def _analyze_class(self, node: ast.ClassDef, file_path: Path) -> PythonClass:
        """Analyze a class definition"""
        cls = PythonClass(
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
            cls.docstring = node.body[0].value.value
        
        # Extract base classes
        for base in node.bases:
            if hasattr(ast, 'unparse'):
                cls.base_classes.append(ast.unparse(base))
            else:
                cls.base_classes.append(str(base))
        
        # Check if abstract
        cls.is_abstract = any('abstract' in dec for dec in [str(d) for d in node.decorator_list])
        
        # Analyze methods
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                method = self._analyze_function(item, file_path)
                method.is_class_method = True
                method.is_static_method = any('staticmethod' in dec for dec in method.decorators)
                cls.methods.append(method)
        
        # Calculate complexity
        cls.complexity = sum(method.complexity for method in cls.methods)
        
        return cls
    
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
    
    def _calculate_cyclomatic_complexity(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity of a function"""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        
        return complexity
    
    def _build_dependency_graph(self):
        """Build import and dependency graph"""
        for module in self.modules:
            for dep in module.dependencies:
                self.import_graph[module.name].add(dep)
                self.dependency_tree[dep].add(module.name)
    
    def _detect_patterns(self):
        """Detect code patterns and anti-patterns"""
        for func in self.functions:
            # Long function
            if func.lines_of_code > self.anti_patterns['long_function']['threshold']:
                self.patterns.append(CodePattern(
                    pattern_type='long_function',
                    description=f'Function {func.name} is {func.lines_of_code} lines long',
                    severity=self.anti_patterns['long_function']['severity'],
                    file_path=func.file_path,
                    line_number=func.line_number,
                    suggestion='Consider breaking into smaller functions',
                    category='maintainability'
                ))
            
            # High complexity
            if func.complexity > 10:
                self.patterns.append(CodePattern(
                    pattern_type='high_complexity',
                    description=f'Function {func.name} has complexity {func.complexity}',
                    severity='high',
                    file_path=func.file_path,
                    line_number=func.line_number,
                    suggestion='Refactor to reduce complexity',
                    category='maintainability'
                ))
            
            # Missing docstring
            if not func.docstring and not func.name.startswith('_'):
                self.patterns.append(CodePattern(
                    pattern_type='missing_docstring',
                    description=f'Function {func.name} lacks docstring',
                    severity=self.anti_patterns['missing_docstring']['severity'],
                    file_path=func.file_path,
                    line_number=func.line_number,
                    suggestion='Add docstring for better documentation',
                    category='style'
                ))
    
    def _calculate_metrics(self):
        """Calculate codebase metrics"""
        total_lines = sum(module.lines_of_code for module in self.modules)
        total_functions = len(self.functions)
        total_classes = len(self.classes)
        total_modules = len(self.modules)
        
        avg_function_length = sum(func.lines_of_code for func in self.functions) / total_functions if total_functions > 0 else 0
        avg_complexity = sum(func.complexity for func in self.functions) / total_functions if total_functions > 0 else 0
        
        self.code_metrics = {
            'total_lines_of_code': total_lines,
            'total_functions': total_functions,
            'total_classes': total_classes,
            'total_modules': total_modules,
            'average_function_length': avg_function_length,
            'average_complexity': avg_complexity,
            'functions_with_docstrings': sum(1 for f in self.functions if f.docstring),
            'classes_with_docstrings': sum(1 for c in self.classes if c.docstring),
            'duplicate_functions': self._find_duplicate_functions(),
            'most_used_imports': self._get_most_used_imports(),
            'largest_functions': sorted(self.functions, key=lambda x: x.lines_of_code, reverse=True)[:10],
            'most_complex_functions': sorted(self.functions, key=lambda x: x.complexity, reverse=True)[:10]
        }
    
    def _find_duplicate_functions(self) -> List[Tuple[str, List[str]]]:
        """Find potentially duplicate functions"""
        function_signatures = defaultdict(list)
        
        for func in self.functions:
            signature = f"{func.name}({', '.join(func.parameters)})"
            function_signatures[signature].append(func.file_path)
        
        return [(sig, files) for sig, files in function_signatures.items() if len(files) > 1]
    
    def _get_most_used_imports(self) -> List[Tuple[str, int]]:
        """Get most frequently used imports"""
        import_counter = Counter()
        for module in self.modules:
            for imp in module.imports:
                import_counter[imp.split('.')[0]] += 1
        
        return import_counter.most_common(10)
    
    def _generate_organization_suggestions(self) -> List[Dict[str, Any]]:
        """Generate suggestions for code organization"""
        suggestions = []
        
        # Group related functions
        function_groups = defaultdict(list)
        for func in self.functions:
            # Group by name prefix or similar functionality
            group_key = func.name.split('_')[0] if '_' in func.name else func.name
            function_groups[group_key].append(func)
        
        for group_name, functions in function_groups.items():
            if len(functions) > 3:  # Suggest grouping if more than 3 related functions
                suggestions.append({
                    'type': 'group_functions',
                    'title': f'Group {group_name} related functions',
                    'description': f'Found {len(functions)} functions related to {group_name}',
                    'functions': [f.name for f in functions],
                    'suggestion': f'Consider creating a {group_name} module or class'
                })
        
        # Suggest module consolidation
        small_modules = [m for m in self.modules if m.lines_of_code < 50 and len(m.functions) < 3]
        if small_modules:
            suggestions.append({
                'type': 'consolidate_modules',
                'title': 'Consolidate small modules',
                'description': f'Found {len(small_modules)} small modules that could be consolidated',
                'modules': [m.name for m in small_modules],
                'suggestion': 'Consider merging small modules into larger, more cohesive units'
            })
        
        return suggestions
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate analysis summary"""
        return {
            'total_files_analyzed': len(self.modules),
            'total_functions': len(self.functions),
            'total_classes': len(self.classes),
            'total_patterns_found': len(self.patterns),
            'code_quality_score': self._calculate_quality_score(),
            'main_concerns': self._get_main_concerns(),
            'recommendations': self._get_top_recommendations()
        }
    
    def _calculate_quality_score(self) -> int:
        """Calculate overall code quality score (0-100)"""
        score = 100
        
        # Deduct for anti-patterns
        for pattern in self.patterns:
            if pattern.severity == 'critical':
                score -= 20
            elif pattern.severity == 'high':
                score -= 10
            elif pattern.severity == 'medium':
                score -= 5
            else:
                score -= 2
        
        # Bonus for good practices
        docstring_ratio = self.code_metrics['functions_with_docstrings'] / max(self.code_metrics['total_functions'], 1)
        if docstring_ratio > 0.8:
            score += 10
        elif docstring_ratio > 0.5:
            score += 5
        
        return max(0, min(100, score))
    
    def _get_main_concerns(self) -> List[str]:
        """Get main code quality concerns"""
        concerns = []
        
        high_complexity = sum(1 for f in self.functions if f.complexity > 10)
        if high_complexity > 0:
            concerns.append(f'{high_complexity} functions with high complexity')
        
        missing_docs = sum(1 for f in self.functions if not f.docstring)
        if missing_docs > 0:
            concerns.append(f'{missing_docs} functions missing docstrings')
        
        long_functions = sum(1 for f in self.functions if f.lines_of_code > 50)
        if long_functions > 0:
            concerns.append(f'{long_functions} functions are too long')
        
        return concerns
    
    def _get_top_recommendations(self) -> List[str]:
        """Get top recommendations for improvement"""
        recommendations = []
        
        if self.code_metrics['average_complexity'] > 5:
            recommendations.append('Refactor high-complexity functions')
        
        if self.code_metrics['functions_with_docstrings'] / max(self.code_metrics['total_functions'], 1) < 0.5:
            recommendations.append('Add docstrings to improve documentation')
        
        if len(self.patterns) > 10:
            recommendations.append('Address code quality issues')
        
        return recommendations


def main():
    """Main function for testing"""
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python python_organizer.py <directory>")
        sys.exit(1)
    
    organizer = PythonOrganizer(sys.argv[1])
    results = organizer.analyze_codebase()
    
    print("\n📊 Analysis Results:")
    print(f"   📁 Modules: {results['summary']['total_files_analyzed']}")
    print(f"   🔧 Functions: {results['summary']['total_functions']}")
    print(f"   🏗️  Classes: {results['summary']['total_classes']}")
    print(f"   ⚠️  Issues: {results['summary']['total_patterns_found']}")
    print(f"   📈 Quality Score: {results['summary']['code_quality_score']}/100")
    
    if results['summary']['main_concerns']:
        print("\n🚨 Main Concerns:")
        for concern in results['summary']['main_concerns']:
            print(f"   • {concern}")
    
    if results['summary']['recommendations']:
        print("\n💡 Recommendations:")
        for rec in results['summary']['recommendations']:
            print(f"   • {rec}")


if __name__ == "__main__":
    main()