#!/usr/bin/env python3
"""
Advanced Dependency Graph Generator
Maps all scripts and their parent-child relationships
"""

import os
import json
import re
from pathlib import Path
from collections import defaultdict

def extract_dependencies(script_path):
    """Extract all scripts called/sourced by this script"""
    dependencies = set()
    try:
        with open(script_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
            # Pattern 1: source/. scriptname
            patterns = [
                r'(?:source|\.|bash)\s+([^\s]+\.sh)',
                r'bash\s+-c\s+["\']([^\s"\']+\.sh)',
                r'/bin/bash\s+([^\s]+\.sh)',
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, content)
                dependencies.update(matches)
    except:
        pass
    
    return list(dependencies)

def get_script_type(path):
    """Classify script by its purpose"""
    path_str = str(path).lower()
    
    if 'cleanup' in path_str:
        return 'cleanup'
    elif 'setup' in path_str or 'init' in path_str:
        return 'setup'
    elif 'launch' in path_str or 'run' in path_str:
        return 'orchestrator'
    elif 'automat' in path_str:
        return 'automation'
    elif 'monitor' in path_str or 'check' in path_str:
        return 'monitoring'
    elif 'convert' in path_str or 'process' in path_str or 'transcribe' in path_str:
        return 'processor'
    elif 'archive' in path_str or 'history' in path_str:
        return 'obsolete'
    else:
        return 'utility'

def analyze_scripts(root_dir):
    """Analyze all scripts and build dependency graph"""
    
    graph = {}
    all_scripts = {}
    dependencies_map = defaultdict(list)  # script -> [dependents]
    
    print("🔍 Scanning scripts...")
    
    # Find all .sh files
    script_files = []
    for root, dirs, files in os.walk(root_dir):
        # Skip certain directories
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '.history']]
        
        for file in files:
            if file.endswith('.sh'):
                script_files.append(os.path.join(root, file))
    
    print(f"Found {len(script_files)} scripts")
    
    # Build dependency map
    print("📊 Building dependency graph...")
    
    for script_path in script_files:
        rel_path = script_path.replace(root_dir, '~')
        deps = extract_dependencies(script_path)
        
        script_type = get_script_type(script_path)
        file_size = os.path.getsize(script_path)
        
        graph[rel_path] = {
            'type': script_type,
            'children': deps,  # scripts this calls
            'parents': [],      # will be populated below
            'file_size': file_size,
            'path': script_path
        }
        
        # Track reverse dependencies
        for dep in deps:
            dependencies_map[dep].append(rel_path)
    
    # Fill in parents
    for script, parents in dependencies_map.items():
        if script in graph:
            graph[script]['parents'] = parents
    
    return graph

def identify_criticality(graph):
    """Identify critical scripts based on dependents"""
    
    for script, data in graph.items():
        parent_count = len(data['parents'])
        
        if parent_count >= 10:
            data['criticality'] = 'critical'
        elif parent_count >= 5:
            data['criticality'] = 'high'
        elif parent_count >= 2:
            data['criticality'] = 'medium'
        else:
            data['criticality'] = 'low'

def generate_report(graph):
    """Generate analysis report"""
    
    print("\n" + "="*60)
    print("📊 SCRIPT DEPENDENCY ANALYSIS REPORT")
    print("="*60 + "\n")
    
    # Statistics
    total_scripts = len(graph)
    orchestrators = sum(1 for s in graph.values() if s['type'] == 'orchestrator')
    utilities = sum(1 for s in graph.values() if s['type'] == 'utility')
    critical = sum(1 for s in graph.values() if s['criticality'] == 'critical')
    
    print(f"Total Scripts: {total_scripts}")
    print(f"Orchestrators: {orchestrators}")
    print(f"Utilities: {utilities}")
    print(f"Critical Hub Scripts: {critical}\n")
    
    # Show critical scripts
    print("🎯 CRITICAL HUB SCRIPTS (10+ dependents):")
    print("-" * 60)
    
    critical_scripts = sorted(
        [(s, d) for s, d in graph.items() if d['criticality'] == 'critical'],
        key=lambda x: len(x[1]['parents']),
        reverse=True
    )
    
    for script, data in critical_scripts[:10]:
        print(f"\n{script}")
        print(f"  Type: {data['type']}")
        print(f"  Dependents: {len(data['parents'])}")
        print(f"  Size: {data['file_size']} bytes")
        if data['parents']:
            print(f"  Called by: {', '.join(data['parents'][:3])}")
    
    # Show orphans (no parents, no children)
    print("\n\n⚪ ORPHAN SCRIPTS (standalone, no dependencies):")
    print("-" * 60)
    
    orphans = [s for s, d in graph.items() if not d['parents'] and not d['children']]
    print(f"Found {len(orphans)} orphan scripts")
    for script in orphans[:10]:
        print(f"  {script}")
    
    return graph

# Run analysis
root = os.path.expanduser('~')
graph = analyze_scripts(root)
identify_criticality(graph)
report_graph = generate_report(graph)

# Save to JSON
output_file = os.path.expanduser('~/script_dependency_graph.json')
with open(output_file, 'w') as f:
    json.dump(graph, f, indent=2)
print(f"\n✅ Full dependency graph saved to: {output_file}")

