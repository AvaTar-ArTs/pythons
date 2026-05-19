#!/usr/bin/env python3
"""
Clean up Docker to free disk space.
Safely removes unused containers, images, volumes, and networks.
"""

import subprocess


def run_command(cmd, description):
    """Run a command and return success status."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, check=True
        )
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e.stderr}")
        return False


def get_disk_usage_before():
    """Get Docker disk usage before cleanup."""
    try:
        result = subprocess.run(
            ["docker", "system", "df"], capture_output=True, text=True, check=True
        )
        return result.stdout
    except:
        return None


def main():
    print("🧹 Docker Cleanup Script")
    print("=" * 50)

    # Show usage before
    print("\n📊 Disk Usage BEFORE cleanup:")
    before = get_disk_usage_before()
    if before:
        print(before)

    print("\n" + "=" * 50)
    print("Starting cleanup...")
    print("=" * 50)

    # Safe cleanup operations (in order of safety)
    operations = [
        (
            "docker system prune -f",
            "Removing stopped containers, unused networks, dangling images",
        ),
        ("docker image prune -a -f", "Removing all unused images (not just dangling)"),
        ("docker volume prune -f", "Removing unused volumes"),
        ("docker builder prune -a -f", "Removing build cache"),
    ]

    success_count = 0
    for cmd, desc in operations:
        if run_command(cmd, desc):
            success_count += 1

    # Show usage after
    print("\n" + "=" * 50)
    print("📊 Disk Usage AFTER cleanup:")
    after = get_disk_usage_before()
    if after:
        print(after)

    print("\n" + "=" * 50)
    if success_count == len(operations):
        print("✅ Cleanup completed successfully!")
    else:
        print(f"⚠️  Cleanup completed with {len(operations) - success_count} errors")

    print("\n💡 Tip: Run 'python docker-disk-monitor.py' to check usage regularly")


if __name__ == "__main__":
    main()
