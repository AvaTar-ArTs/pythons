#!/usr/bin/env python3
"""
UNIVERSAL ROUTER v1.0
The central nervous system for the AVATARARTS Ecosystem.
Routes natural language intents to specific Functional Hub scripts.
"""

import sys
import os
import subprocess
from pathlib import Path

# Add generic python path to find avatar_utils if not in current dir
sys.path.append(os.path.expanduser("~/pythons"))
try:
    from avatar_utils import print_header, timing_decorator, load_env_d
except ImportError:
    # Fallback if avatar_utils is missing (bootstrapping)
    def print_header(text): print(f"\n=== {text} ===\n")
    def timing_decorator(func): return func
    def load_env_d(): pass

# --- Configuration ---
LOGIC_HUB = Path(os.path.expanduser("~/pythons"))
PRODUCTION_HUB = Path(os.path.expanduser("~/AVATARARTS"))
MAINTENANCE_HUB = Path(os.path.expanduser("~/clean"))
HOME = Path(os.path.expanduser("~"))

# --- Command Map ---
# Maps verbs/intents to specific script paths and default arguments
COMMAND_MAP = {
    "reindex": {
        "description": "Refresh ecosystem-wide file inventories",
        "steps": [
            {"cmd": ["bash", str(HOME / "create_comprehensive_index.sh")], "desc": "Filesystem Index"},
            {"cmd": ["python3", str(HOME / "inventory_avatararts.py")], "desc": "AvatarArts Inventory"}
        ]
    },
    "scan": {
        "description": "Deep recursive scan of a directory",
        "script": MAINTENANCE_HUB / "all.py",
        "default_args": [str(HOME), "-r"]
    },
    "status": {
        "description": "System health and business activation status",
        "steps": [
            {"cmd": ["du", "-sh", str(PRODUCTION_HUB)], "desc": "Production Size"},
            {"cmd": ["pystatus"], "desc": "Python Environment"}, # Relies on zsh function, might need shell=True
        ]
    }
}

@timing_decorator
def execute_step(step_config):
    """Executes a single step defined in the command map."""
    cmd = step_config.get("cmd")
    desc = step_config.get("desc", "Operation")
    
    print(f"--> Starting: {desc}")
    try:
        # If it's a shell command string, run with shell=True. If list, run directly.
        if isinstance(cmd, str):
            subprocess.run(cmd, shell=True, check=True)
        else:
            subprocess.run(cmd, check=True)
        print(f"--> Completed: {desc}")
    except subprocess.CalledProcessError as e:
        print(f"!! Failed: {desc} (Exit Code: {e.returncode})")
    except FileNotFoundError:
        print(f"!! Failed: {desc} (Script/Command not found)")

def router(args):
    """Parses arguments and routes to the correct handler."""
    if not args:
        print_header("UNIVERSAL ROUTER")
        print("Usage: universal [command] [args]")
        print("\nAvailable Commands:")
        for key, val in COMMAND_MAP.items():
            print(f"  {key.ljust(15)} : {val['description']}")
        return

    intent = args[0].lower()
    
    if intent in COMMAND_MAP:
        config = COMMAND_MAP[intent]
        print_header(f"UNIVERSAL EXECUTION: {intent.upper()}")
        
        # 1. Multi-step workflows
        if "steps" in config:
            for step in config["steps"]:
                execute_step(step)
                
        # 2. Single script execution
        elif "script" in config:
            script_path = config["script"]
            # Pass remaining args or defaults
            script_args = args[1:] if len(args) > 1 else config.get("default_args", [])
            
            cmd = ["python3", str(script_path)] + script_args
            execute_step({"cmd": cmd, "desc": f"Running {script_path.name}"})
            
    else:
        print(f"Unknown command: '{intent}'.")
        print("Try 'universal' to see available commands.")

if __name__ == "__main__":
    load_env_d()
    router(sys.argv[1:])
