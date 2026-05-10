#!/usr/bin/env python3
"""
AvatarArts Distribution System Demo Script

This script demonstrates the usage of the AvatarArts music distribution integrations
with the nocTurneMeLoDieS V4 system.
"""

import asyncio
import json
from pathlib import Path

from avatararts_distribution_manager import AvatarArtsDistributionManager


async def demo_distribution_setup():
    """Demonstrate the setup and initialization of the distribution system"""
    print("🚀 Setting up AvatarArts Distribution System...")

    # Load configuration
    config_path = Path("avatararts_distribution_config.json")
    if config_path.exists():
        with open(config_path, "r") as f:
            config = json.load(f)["avatararts_distribution_config"]
    else:
        # Fallback configuration
        config = {
            "local_storage_path": "/Users/steven/Music/nocTurneMeLoDieS",
            "artist_name": "AvatarArts",
            "label_name": "AvatarArts Creative Automation",
            "platforms": {
                "distrokid": {"enabled": True},
                "spotify": {"enabled": True},
                "soundcloud": {"enabled": True},
            },
        }

    # Initialize the distribution manager
    manager = AvatarArtsDistributionManager(config)
    await manager.initialize_all_platforms()

    print("✅ Distribution system initialized successfully!")
    return manager, config


async def demo_album_distribution(manager, config):
    """Demonstrate album distribution to all platforms"""
    print("\n📦 Demonstrating album distribution...")

    # Look for sample albums in the ALBUMS directory
    albums_dir = Path(config["local_storage_path"]) / "ALBUMS"
    if albums_dir.exists():
        sample_albums = list(albums_dir.glob("*"))
        if sample_albums:
            sample_album = sample_albums[0]  # Use the first album as a demo
            print(f"Using sample album: {sample_album.name}")

            # Distribute the album to all platforms
            result = await manager.distribute_to_all_platforms(str(sample_album))

            print(f"✅ Distribution completed for: {sample_album.name}")
            print(f"   DistroKid: {result.get('distrokid_result', {}).get('success', 'N/A')}")
            print(f"   SoundCloud: {result.get('soundcloud_result', {}).get('success', 'N/A')}")
        else:
            print("⚠️  No sample albums found in ALBUMS directory")
    else:
        print("⚠️  ALBUMS directory not found")


async def demo_auto_distribution(manager):
    """Demonstrate automatic distribution of new content"""
    print("\n🤖 Demonstrating auto-distribution of new content...")

    # Perform auto-distribution
    results = await manager.auto_distribute_new_content()

    print("✅ Auto-distribution completed!")
    print(f"   Albums processed: {results['albums_processed']}")
    print(f"   Albums distributed: {results['albums_distributed']}")
    print(f"   Errors: {len(results['errors'])}")


async def demo_monitoring(manager):
    """Demonstrate platform monitoring"""
    print("\n📊 Demonstrating platform monitoring...")

    # Monitor all platforms
    monitoring_results = await manager.monitor_all_platforms()

    print("✅ Monitoring completed!")

    # Display key metrics
    dk_status = monitoring_results.get("distrokid_monitoring", {})
    if dk_status:
        print(f"   DistroKid active submissions: {dk_status.get('active_submissions', 0)}")

    sc_stats = monitoring_results.get("soundcloud_stats", {})
    if sc_stats and "user_info" in sc_stats:
        user_info = sc_stats["user_info"]
        print(f"   SoundCloud followers: {user_info.get('followers', 0)}")
        print(f"   SoundCloud tracks: {user_info.get('tracks_count', 0)}")


async def demo_comprehensive_summary(manager):
    """Demonstrate comprehensive system summary"""
    print("\n📋 Generating comprehensive system summary...")

    # Get comprehensive summary
    summary = await manager.get_comprehensive_summary()

    print("✅ Comprehensive summary generated!")
    print(f"   Total albums distributed: {summary['overall_stats']['total_albums_distributed']}")
    print(f"   Recent activities tracked: {len(summary['recent_activities'])}")

    # Show recent activities
    if summary["recent_activities"]:
        print("   Recent activities:")
        for activity in summary["recent_activities"][:3]:  # Show first 3
            print(f"     - {activity['activity_type']}: {activity['file']}")


async def main():
    """Main demonstration function"""
    print("🎵 AvatarArts Music Distribution Integration Demo")
    print("=" * 50)

    try:
        # Setup the distribution system
        manager, config = await demo_distribution_setup()

        # Demonstrate various features
        await demo_album_distribution(manager, config)
        await demo_auto_distribution(manager)
        await demo_monitoring(manager)
        await demo_comprehensive_summary(manager)

        print("\n🎉 Demo completed successfully!")
        print("\n💡 Next steps:")
        print("   1. Configure your API keys in the environment variables")
        print("   2. Set up your preferred distribution settings")
        print("   3. Run auto-distribution to publish your content")
        print("   4. Monitor performance across all platforms")

    except Exception as e:
        print(f"❌ Error during demo: {str(e)}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
