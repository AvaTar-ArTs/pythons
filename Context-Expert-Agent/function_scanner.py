#!/usr/bin/env python3
"""
Deep Content Function Scanner
Analyzes all Python files to extract function definitions and signatures
"""

import ast
import os
from pathlib import Path
from collections import defaultdict
import json
from datetime import datetime


class FunctionScanner:
    def __init__(self, base_directory):
        self.base_directory = Path(base_directory)
        self.functions = []  # Store all functions found
        self.function_map = defaultdict(list)  # Map function names to their locations
        self.file_functions = {}  # Map files to their functions

    def extract_functions_from_file(self, file_path):
        """Extract function definitions from a Python file"""
        functions_in_file = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Parse the AST
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_info = {
                        'name': node.name,
                        'file_path': str(file_path),
                        'line_number': node.lineno,
                        'args': [],
                        'defaults': [],
                        'docstring': ast.get_docstring(node),
                        'decorators': [ast.unparse(d) for d in node.decorator_list],
                        'return_annotation': None,
                        'complexity': self._calculate_complexity(node)
                    }
                    
                    # Extract arguments
                    args = node.args
                    arg_names = []
                    
                    # Regular arguments
                    for arg in args.args:
                        if isinstance(arg, ast.arg):
                            arg_names.append(arg.arg)
                    
                    # Default values
                    defaults = []
                    for default in args.defaults:
                        try:
                            defaults.append(ast.unparse(default))
                        except:
                            defaults.append(str(default))
                    
                    func_info['args'] = arg_names
                    func_info['defaults'] = defaults
                    
                    # Return annotation
                    if node.returns:
                        try:
                            func_info['return_annotation'] = ast.unparse(node.returns)
                        except:
                            func_info['return_annotation'] = str(node.returns)
                    
                    functions_in_file.append(func_info)
                    self.functions.append(func_info)
                    self.function_map[node.name].append(func_info)
        
        except SyntaxError:
            print(f"Syntax error in file: {file_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
        
        self.file_functions[str(file_path)] = functions_in_file
        return functions_in_file

    def _calculate_complexity(self, node):
        """Calculate function complexity based on AST nodes"""
        # This is a simple cyclomatic complexity calculation
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):  # and/or expressions
                complexity += len(child.values) - 1
        
        return complexity

    def scan_all_files(self):
        """Scan all Python files in the directory"""
        print(f"Scanning Python files in {self.base_directory}")
        
        python_files = list(self.base_directory.rglob("*.py"))
        print(f"Found {len(python_files)} Python files")
        
        for i, file_path in enumerate(python_files, 1):
            if i % 100 == 0:
                print(f"Scanned {i}/{len(python_files)} files...")
            
            self.extract_functions_from_file(file_path)
        
        print(f"\nFound {len(self.functions)} functions total")
        print(f"Unique function names: {len(self.function_map)}")
        
        # Summary statistics
        unique_functions = [
            name for name, funcs in self.function_map.items() 
            if len(funcs) == 1
        ]
        duplicate_functions = [
            name for name, funcs in self.function_map.items() 
            if len(funcs) > 1
        ]
        
        print(f"Unique function names: {len(unique_functions)}")
        print(f"Duplicate function names: {len(duplicate_functions)}")
        
        return self.functions

    def save_results(self, output_file):
        """Save function scan results to a file"""
        results = {
            'scan_date': datetime.now().isoformat(),
            'directory': str(self.base_directory),
            'total_functions': len(self.functions),
            'unique_function_names': len(self.function_map),
            'function_details': self.functions,
            'function_map': dict(self.function_map),
            'file_functions': self.file_functions
        }
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"Results saved to {output_file}")

    def get_functions_by_file(self, filename):
        """Get all functions in a specific file"""
        return self.file_functions.get(filename, [])

    def get_function_definitions(self, function_name):
        """Get all definitions of a function with the given name"""
        return self.function_map.get(function_name, [])


def main():
    scanner = FunctionScanner("/Users/steven/pythons")
    functions = scanner.scan_all_files()
    
    # Save results
    output_file = f"/Users/steven/pythons/function_scan_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    scanner.save_results(output_file)
    
    # Print some statistics
    print("\n=== FUNCTION SCAN STATISTICS ===")
    print(f"Total functions found: {len(scanner.functions)}")
    print(f"Unique function names: {len(scanner.function_map)}")
    
    # Show top 20 most common function names
    print("\n=== TOP 20 MOST COMMON FUNCTION NAMES ===")
    function_counts = [(name, len(funcs)) for name, funcs in scanner.function_map.items()]
    function_counts.sort(key=lambda x: x[1], reverse=True)
    
    for name, count in function_counts[:20]:
        print(f"{name}: {count} definitions")
    
    # Show examples of duplicated functions
    print("\n=== EXAMPLES OF DUPLICATED FUNCTIONS ===")
    duplicate_funcs = [(name, funcs) for name, funcs in scanner.function_map.items() if len(funcs) > 1]
    
    for name, funcs in duplicate_funcs[:10]:
        print(f"\nFunction '{name}' ({len(funcs)} definitions):")
        for func in funcs:
            print(f"  - File: {func['file_path']}")
            print(f"    Args: {func['args']}")
            print(f"    Line: {func['line_number']}")
    
    print(f"\nDetailed results saved to: {output_file}")


if __name__ == "__main__":
    main()