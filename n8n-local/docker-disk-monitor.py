#!/usr/bin/env python3
"""
Monitor Docker disk usage and warn if it's getting too large.
Run this periodically to keep an eye on Docker's disk consumption.
"""

import subprocess
import sys
from pathlib import Path

# Disk usage thresholds (in GB)
WARNING_THRESHOLD = 10  # Warn if Docker uses more than 10GB
CRITICAL_THRESHOLD = 20  # Critical if Docker uses more than 20GB

def get_docker_disk_usage():
    """Get Docker's total disk usage in GB."""
    try:
        result = subprocess.run(
            ['docker', 'system', 'df', '--format', '{{.Size}}'],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Parse the output to get total size
        result = subprocess.run(
            ['docker', 'system', 'df'],
            capture_output=True,
            text=True,
            check=True
        )
        
        lines = result.stdout.strip().split('\n')
        if len(lines) < 2:
            return None
        
        # Get the total line (usually the last line)
        total_line = lines[-1]
        # Extract size (format: "Local Volumes  2  1.234 GB  512 MB")
        parts = total_line.split()
        for i, part in enumerate(parts):
            if part in ['GB', 'MB', 'KB']:
                size = float(parts[i-1])
                unit = part
                if unit == 'GB':
                    return size
                elif unit == 'MB':
                    return size / 1024
                elif unit == 'KB':
                    return size / (1024 * 1024)
        
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error running docker command: {e}")
        return None
    except FileNotFoundError:
        print("Docker not found. Is Docker installed?")
        return None

def get_detailed_usage():
    """Get detailed breakdown of Docker disk usage."""
    try:
        result = subprocess.run(
            ['docker', 'system', 'df', '-v'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"

def main():
    print("🐳 Docker Disk Usage Monitor\n")
    print("=" * 50)
    
    # Get detailed usage
    detailed = get_detailed_usage()
    print(detailed)
    print("=" * 50)
    
    # Get total usage
    total_gb = get_docker_disk_usage()
    
    if total_gb is None:
        print("\n⚠️  Could not determine Docker disk usage.")
        sys.exit(1)
    
    print(f"\n📊 Total Docker Disk Usage: {total_gb:.2f} GB")
    
    if total_gb >= CRITICAL_THRESHOLD:
        print(f"\n🚨 CRITICAL: Docker is using {total_gb:.2f} GB!")
        print("   Run cleanup script: python docker-cleanup.py")
        sys.exit(2)
    elif total_gb >= WARNING_THRESHOLD:
        print(f"\n⚠️  WARNING: Docker is using {total_gb:.2f} GB")
        print("   Consider running cleanup: python docker-cleanup.py")
        sys.exit(1)
    else:
        print(f"\n✅ Docker disk usage is healthy ({total_gb:.2f} GB)")
        sys.exit(0)

if __name__ == "__main__":
    main()
