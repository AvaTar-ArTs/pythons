#!/usr/bin/env python3
"""
AI Ecosystem Monitor

This script monitors the status of all AI platforms in the ecosystem
and updates the dashboard with current status information.
"""

import json
import os
from datetime import datetime
from pathlib import Path


def get_ai_platform_statuses():
    """Get the current status of all AI platforms in the ecosystem."""
    
    statuses = {}
    
    # Define the platforms and their key directories/files to check
    platforms = {
        "Claude": {
            "path": Path("/Users/steven/iterm2/claude-ecosystem"),
            "config_files": [".claude.json"],
            "activity_indicators": ["history", "sessions"]
        },
        "Cursor": {
            "path": Path("/Users/steven/iterm2/cursor-ecosystem"),
            "config_files": ["ide_state.json", "prompt_history.json"],
            "activity_indicators": ["shell_snapshots", "sessions"]
        },
        "Gemini": {
            "path": Path("/Users/steven/iterm2/gemini"),
            "config_files": [".gemini", ".gemini_backup"],
            "activity_indicators": [".gemini/chats", ".gemini/tmp"]
        },
        "Qwen": {
            "path": Path("/Users/steven/iterm2/.qwen"),
            "config_files": ["settings.json", "oauth_creds.json"],
            "activity_indicators": ["history", "projects", "todos"]
        },
        "Grok": {
            "path": Path("/Users/steven/iterm2/.grok"),
            "config_files": ["config.json"],  # assuming a config file exists
            "activity_indicators": ["history", "logs"]  # assuming these exist
        }
    }
    
    for platform_name, platform_info in platforms.items():
        platform_path = platform_info["path"]
        
        if platform_path.exists():
            # Check if platform directory exists
            statuses[platform_name] = {
                "status": "active",
                "last_activity": "unknown",
                "active_sessions": "unknown",
                "performance_metrics": "not_implemented_yet"
            }
            
            # Look for recent activity
            try:
                # Get the most recently modified file in the directory
                latest_file = max(
                    platform_path.glob("**/*"), 
                    key=lambda x: x.stat().st_mtime,
                    default=None
                )
                
                if latest_file:
                    mtime = datetime.fromtimestamp(latest_file.stat().st_mtime)
                    statuses[platform_name]["last_activity"] = mtime.isoformat()
                    
            except (OSError, ValueError):
                statuses[platform_name]["last_activity"] = "error_accessing"
        else:
            statuses[platform_name] = {
                "status": "inactive",
                "last_activity": "not_found",
                "active_sessions": "N/A",
                "performance_metrics": "N/A"
            }
    
    return statuses


def update_dashboard(statuses):
    """Update the dashboard file with current status information."""
    
    dashboard_path = Path("/Users/steven/iterm2/ai_dashboard.md")
    
    if not dashboard_path.exists():
        print(f"Dashboard file not found at {dashboard_path}")
        return
    
    # Read the current dashboard
    with open(dashboard_path, 'r') as f:
        content = f.read()
    
    # Update the status section
    updated_content = content
    
    # Update each platform status
    for platform, status_info in statuses.items():
        status_tag = f"### {platform}\n- Status: "
        if status_tag in updated_content:
            # Replace the status line
            start_idx = updated_content.find(status_tag) + len(status_tag)
            end_idx = updated_content.find("\n", start_idx)
            current_status_line = updated_content[start_idx:end_idx]
            
            # Update status
            new_status_line = status_info["status"]
            updated_content = updated_content.replace(
                f"{status_tag}{current_status_line}",
                f"{status_tag}{new_status_line}"
            )
            
            # Update last activity
            activity_tag = "- Last Activity: "
            activity_start = updated_content.find(activity_tag, start_idx)
            if activity_start != -1:
                activity_start += len(activity_tag)
                activity_end = updated_content.find("\n", activity_start)
                current_activity = updated_content[activity_start:activity_end]
                
                updated_content = updated_content.replace(
                    f"{activity_tag}{current_activity}",
                    f"{activity_tag}{status_info['last_activity']}"
                )
    
    # Add timestamp to the dashboard
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    updated_content = f"# AI Ecosystem Dashboard\n\n_Last updated: {timestamp}_\n\n" + \
                     updated_content.split("\n\n", 1)[1]  # Remove old header
    
    # Write the updated dashboard
    with open(dashboard_path, 'w') as f:
        f.write(updated_content)
    
    print(f"Dashboard updated at {timestamp}")


def main():
    """Main function to run the AI ecosystem monitor."""
    print("AI Ecosystem Monitor Starting...")
    
    # Get current statuses
    statuses = get_ai_platform_statuses()
    
    # Print statuses to console
    print("\nCurrent AI Platform Statuses:")
    for platform, status_info in statuses.items():
        print(f"- {platform}: {status_info['status']} (Last activity: {status_info['last_activity']})")
    
    # Update the dashboard
    update_dashboard(statuses)
    
    print("\nMonitoring complete.")


if __name__ == "__main__":
    main()