
import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_033 = 033

#!/usr/bin/env python3
"""
Setup Verification Script
========================
Verifies that all automation and API packages are properly installed
and accessible in the global Python environment.
"""

import sys
import importlib
from pathlib import Path

# Color codes
class Colors:
    GREEN = '\CONSTANT_033[0;32m'
    RED = '\CONSTANT_033[0;31m'
    YELLOW = '\CONSTANT_033[1;33m'
    BLUE = '\CONSTANT_033[0;34m'
    CYAN = '\CONSTANT_033[0;36m'
    NC = '\CONSTANT_033[0m'  # No Color

def test_import(module_name, display_name=None):
    """Test if a module can be imported"""
    if display_name is None:
        display_name = module_name
    
    try:
        importlib.import_module(module_name)
        logger.info(f"{Colors.GREEN}✅ {display_name}{Colors.NC}")
        return True
    except ImportError as e:
        logger.info(f"{Colors.RED}❌ {display_name} - {e}{Colors.NC}")
        return False

def test_environment():
    """Test the Python environment setup"""
    logger.info(f"{Colors.CYAN}🐍 Python Environment Test{Colors.NC}")
    logger.info("=" * 50)
    
    # Python version
    logger.info(f"Python Version: {sys.version}")
    logger.info(f"Python Executable: {sys.executable}")
    print()
    
    # Check if we're in the global environment
    if "global_python_env" in sys.executable:
        logger.info(f"{Colors.GREEN}✅ Using global Python environment{Colors.NC}")
    else:
        logger.info(f"{Colors.YELLOW}⚠️  Not using global Python environment{Colors.NC}")
    
    print()

def test_core_packages():
    """Test core automation packages"""
    logger.info(f"{Colors.CYAN}📦 Core Automation Packages{Colors.NC}")
    logger.info("=" * 50)
    
    core_packages = [
        ("requests", "HTTP requests"),
        ("httpx", "Async HTTP client"),
        ("aiohttp", "Async HTTP server/client"),
        ("bs4", "HTML parsing"),
        ("selenium", "Web automation"),
        ("playwright", "Modern web automation"),
        ("pandas", "Data manipulation"),
        ("numpy", "Numerical computing"),
        ("matplotlib", "Plotting"),
        ("seaborn", "Statistical visualization"),
        ("plotly", "Interactive plots"),
        ("jupyter", "Jupyter notebooks"),
        ("IPython", "Enhanced Python shell"),
    ]
    
    success_count = 0
    for module, description in core_packages:
        if test_import(module, f"{module} ({description})"):
            success_count += 1
    
    logger.info(f"\nCore packages: {success_count}/{len(core_packages)} available")
    return success_count == len(core_packages)

def test_ai_packages():
    """Test AI and LLM packages"""
    logger.info(f"\n{Colors.CYAN}🤖 AI & LLM Packages{Colors.NC}")
    logger.info("=" * 50)
    
    ai_packages = [
        ("openai", "OpenAI API"),
        ("anthropic", "Anthropic Claude API"),
        ("groq", "Groq API"),
        ("ollama", "Ollama local models"),
    ]
    
    success_count = 0
    for module, description in ai_packages:
        if test_import(module, f"{module} ({description})"):
            success_count += 1
    
    logger.info(f"\nAI packages: {success_count}/{len(ai_packages)} available")
    return success_count == len(ai_packages)

def test_utility_packages():
    """Test utility packages"""
    logger.info(f"\n{Colors.CYAN}🛠️  Utility Packages{Colors.NC}")
    logger.info("=" * 50)
    
    utility_packages = [
        ("dotenv", "Environment variables"),
        ("schedule", "Job scheduling"),
        ("croniter", "Cron parsing"),
        ("psutil", "System monitoring"),
        ("yaml", "YAML parsing"),
        ("click", "CLI framework"),
        ("typer", "Modern CLI framework"),
        ("rich", "Rich text formatting"),
        ("tqdm", "Progress bars"),
        ("colorama", "Cross-platform colors"),
        ("termcolor", "Terminal colors"),
    ]
    
    success_count = 0
    for module, description in utility_packages:
        if test_import(module, f"{module} ({description})"):
            success_count += 1
    
    logger.info(f"\nUtility packages: {success_count}/{len(utility_packages)} available")
    return success_count == len(utility_packages)

def test_environment_variables():
    """Test environment variable loading"""
    logger.info(f"\n{Colors.CYAN}🔧 Environment Variables{Colors.NC}")
    logger.info("=" * 50)
    
    try:
        from dotenv import load_dotenv
        import os
        
        # Load environment variables
        load_dotenv()
        
        # Check for common API keys
        api_keys = [
            "OPENAI_API_KEY",
            "ANTHROPIC_API_KEY", 
            "GROQ_API_KEY",
            "GROK_API_KEY",
            "DEEPSEEK_API_KEY"
        ]
        
        loaded_keys = []
        for key in api_keys:
            if os.getenv(key):
                loaded_keys.append(key)
                logger.info(f"{Colors.GREEN}✅ {key} loaded{Colors.NC}")
            else:
                logger.info(f"{Colors.YELLOW}⚠️  {key} not found{Colors.NC}")
        
        logger.info(f"\nAPI keys loaded: {len(loaded_keys)}/{len(api_keys)}")
        return len(loaded_keys) > 0
        
    except ImportError:
        logger.info(f"{Colors.RED}❌ python-dotenv not available{Colors.NC}")
        return False

def test_ollama_connection():
    """Test Ollama connection"""
    logger.info(f"\n{Colors.CYAN}🦙 Ollama Connection Test{Colors.NC}")
    logger.info("=" * 50)
    
    try:
        import ollama
        
        # Try to list models
        models = ollama.list()
        logger.info(f"{Colors.GREEN}✅ Ollama connection successful{Colors.NC}")
        logger.info(f"Available models: {len(models['models'])}")
        
        for model in models['models'][:3]:  # Show first 3 models
            model_name = model.get('name', 'Unknown')
            logger.info(f"  • {model_name}")
        
        if len(models['models']) > 3:
            logger.info(f"  ... and {len(models['models']) - 3} more")
        
        return True
        
    except Exception as e:
        logger.info(f"{Colors.RED}❌ Ollama connection failed: {e}{Colors.NC}")
        logger.info(f"{Colors.YELLOW}💡 Make sure Ollama is running: ollama serve{Colors.NC}")
        return False

def main():
    """Main verification function"""
    logger.info(f"{Colors.BLUE}🚀 Python Automation Setup Verification{Colors.NC}")
    logger.info("=" * 60)
    print()
    
    # Run all tests
    tests = [
        ("Environment", test_environment),
        ("Core Packages", test_core_packages),
        ("AI Packages", test_ai_packages),
        ("Utility Packages", test_utility_packages),
        ("Environment Variables", test_environment_variables),
        ("Ollama Connection", test_ollama_connection),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.info(f"{Colors.RED}❌ {test_name} test failed: {e}{Colors.NC}")
            results.append((test_name, False))
    
    # Summary
    logger.info(f"\n{Colors.CYAN}📊 Summary{Colors.NC}")
    logger.info("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = f"{Colors.GREEN}✅ PASS{Colors.NC}" if result else f"{Colors.RED}❌ FAIL{Colors.NC}"
        logger.info(f"{test_name}: {status}")
    
    logger.info(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info(f"\n{Colors.GREEN}🎉 All tests passed! Your automation environment is ready!{Colors.NC}")
        return 0
    else:
        logger.info(f"\n{Colors.YELLOW}⚠️  Some tests failed. Check the output above for details.{Colors.NC}")
        return 1

if __name__ == "__main__":
    sys.exit(main())