#!/usr/bin/env python3
"""
Organize Archives directory - analyze and provide cleanup recommendations
"""
import os
from pathlib import Path
from collections import defaultdict
import json
from datetime import datetime

ARCHIVES_DIR = Path("/Users/steven/Documents/Archives")

def analyze_harbor():
    """Analyze .harbor subdirectory"""
    harbor_path = ARCHIVES_DIR / "repos" / ".harbor"
    if not harbor_path.exists():
        return {"exists": False}
    
    tools = []
    for item in harbor_path.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            # Check if it has meaningful content
            files = list(item.rglob("*"))
            py_files = [f for f in files if f.suffix == '.py']
            docker_files = [f for f in files if f.name in ['Dockerfile', 'docker-compose.yml']]
            scripts = [f for f in files if f.suffix in ['.sh', '.mjs', '.js']]
            
            tools.append({
                "name": item.name,
                "has_python": len(py_files) > 0,
                "has_docker": len(docker_files) > 0,
                "has_scripts": len(scripts) > 0,
                "file_count": len(files),
                "description": get_tool_description(item.name)
            })
    
    return {
        "exists": True,
        "path": str(harbor_path),
        "tools": sorted(tools, key=lambda x: x["name"]),
        "total_tools": len(tools)
    }

def get_tool_description(name):
    """Get description for known tools"""
    descriptions = {
        "aider": "AI pair programming assistant",
        "ollama": "Local LLM runner",
        "open-webui": "Web UI for LLMs",
        "litellm": "LLM proxy/load balancer",
        "llamacpp": "C++ LLM inference",
        "vllm": "Fast LLM serving",
        "agent": "AI agent framework",
        "boost": "Modular AI system",
        "chatui": "Chat UI interface",
        "librechat": "Open source ChatGPT alternative",
        "dify": "LLM app development platform",
        "comfyui": "Stable Diffusion UI",
        "langfuse": "LLM observability",
        "plandex": "AI coding assistant",
        "openinterpreter": "Code interpreter",
        "perplexica": "AI search engine",
        "maigret": "OSINT username search",
        "txtairag": "RAG (Retrieval Augmented Generation)",
        "raglite": "Lightweight RAG",
    }
    return descriptions.get(name, "Unknown tool")

def find_duplicates():
    """Find duplicate files"""
    duplicates = defaultdict(list)
    
    # Simple gallery duplicates
    for item in ARCHIVES_DIR.iterdir():
        if item.is_file() and "simplegallery" in item.name.lower():
            duplicates["simplegallery"].append(item.name)
    
    # Ollama config duplicates
    for item in ARCHIVES_DIR.iterdir():
        if item.is_file() and "ollama" in item.name.lower() and item.suffix == '.zip':
            duplicates["ollama_configs"].append(item.name)
    
    # Notion exports
    notion_exports = []
    for item in ARCHIVES_DIR.iterdir():
        if item.is_file() and ("Export" in item.name or item.name.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f')) and len(item.stem) > 20):
            notion_exports.append(item.name)
    
    if notion_exports:
        duplicates["notion_exports"] = notion_exports
    
    return duplicates

def analyze_directories():
    """Analyze main directories"""
    results = {}
    
    # llama.cpp
    llama_path = ARCHIVES_DIR / "repos" / "llama.cpp"
    if llama_path.exists():
        files = list(llama_path.rglob("*"))
        results["llama.cpp"] = {
            "exists": True,
            "file_count": len([f for f in files if f.is_file()]),
            "dir_count": len([f for f in files if f.is_dir()]),
            "has_cuda": len([f for f in files if f.suffix == '.cu']) > 0,
            "has_cpp": len([f for f in files if f.suffix == '.cpp']) > 0,
        }
    
    # maigret
    maigret_path = ARCHIVES_DIR / "repos" / "maigret"
    if maigret_path.exists():
        files = list(maigret_path.rglob("*"))
        py_files = [f for f in files if f.suffix == '.py']
        results["maigret"] = {
            "exists": True,
            "file_count": len([f for f in files if f.is_file()]),
            "py_files": len(py_files),
            "has_tests": len([f for f in files if 'test' in f.parts]) > 0,
            "has_docs": len([f for f in files if 'docs' in f.parts]) > 0,
        }
    
    return results

def generate_report():
    """Generate comprehensive organization report"""
    print("🔍 Analyzing Archives directory...")
    print("=" * 80)
    
    # Analyze .harbor
    print("\n📦 .harbor/ Subdirectory Analysis")
    print("-" * 80)
    harbor = analyze_harbor()
    if harbor.get("exists"):
        print(f"✅ Found {harbor['total_tools']} tools in .harbor/")
        print("\nTools breakdown:")
        for tool in harbor["tools"]:
            indicators = []
            if tool["has_python"]:
                indicators.append("🐍")
            if tool["has_docker"]:
                indicators.append("🐳")
            if tool["has_scripts"]:
                indicators.append("📜")
            indicators_str = " ".join(indicators) if indicators else "📁"
            print(f"  {indicators_str} {tool['name']:20} - {tool['description']}")
            print(f"      Files: {tool['file_count']}")
    else:
        print("❌ .harbor/ not found")
    
    # Analyze directories
    print("\n📂 Directory Analysis")
    print("-" * 80)
    dirs = analyze_directories()
    for name, info in dirs.items():
        if info.get("exists"):
            print(f"\n✅ {name}/")
            for key, value in info.items():
                if key != "exists":
                    print(f"   {key}: {value}")
    
    # Find duplicates
    print("\n🔄 Duplicate Detection")
    print("-" * 80)
    duplicates = find_duplicates()
    for category, files in duplicates.items():
        if files:
            print(f"\n{category.upper()}: {len(files)} files")
            for f in files:
                print(f"  - {f}")
    
    # Generate recommendations
    print("\n\n🎯 ORGANIZATION RECOMMENDATIONS")
    print("=" * 80)
    
    recommendations = []
    
    # .harbor recommendations
    if harbor.get("exists"):
        print("\n1. .harbor/ Tools:")
        print("   - Review which tools you actively use")
        print("   - Consider moving unused tools to deeper archive")
        print("   - Keep: ollama, open-webui, litellm (if using)")
        print("   - Archive: tools you haven't used in 6+ months")
    
    # Duplicate recommendations
    if duplicates.get("simplegallery"):
        print(f"\n2. SimpleGallery Duplicates ({len(duplicates['simplegallery'])} versions):")
        print("   - Keep: simplegallery_2025.zip or simplegallery-Perfect.zip")
        print("   - Delete: other versions")
        recommendations.append({
            "action": "consolidate",
            "type": "simplegallery",
            "keep": "simplegallery_2025.zip",
            "remove": duplicates["simplegallery"]
        })
    
    if duplicates.get("ollama_configs"):
        print(f"\n3. Ollama Config Duplicates ({len(duplicates['ollama_configs'])} versions):")
        print("   - Keep: ollama-setup-kit-Intel-macOS.zip (most recent)")
        print("   - Delete: older versions")
        recommendations.append({
            "action": "consolidate",
            "type": "ollama_configs",
            "keep": "ollama-setup-kit-Intel-macOS.zip",
            "remove": [f for f in duplicates["ollama_configs"] if f != "ollama-setup-kit-Intel-macOS.zip"]
        })
    
    if duplicates.get("notion_exports"):
        print(f"\n4. Notion Exports ({len(duplicates['notion_exports'])} files):")
        print("   - Extract and organize if needed")
        print("   - Or move to dedicated Notion exports folder")
        print("   - Consider deleting if already imported")
    
    # Directory recommendations
    if dirs.get("llama.cpp"):
        print("\n5. llama.cpp/:")
        print("   - Large C++ codebase (985 files)")
        print("   - Keep if you compile/use it")
        print("   - Consider: git clone when needed instead of archiving")
    
    if dirs.get("maigret"):
        print("\n6. maigret/:")
        print("   - OSINT tool with full test suite")
        print("   - Keep if you use OSINT")
        print("   - Or: pip install maigret instead of archiving source")
    
    # Save recommendations
    output_file = ARCHIVES_DIR / "organization_recommendations.json"
    with open(output_file, 'w') as f:
        json.dump({
            "generated": datetime.now().isoformat(),
            "harbor": harbor,
            "directories": dirs,
            "duplicates": duplicates,
            "recommendations": recommendations
        }, f, indent=2)
    
    print(f"\n\n✅ Full analysis saved to: {output_file}")
    return recommendations

if __name__ == "__main__":
    generate_report()
