"""
AvatarArts Music Distribution Integration Manager
Coordinates DistroKid, Spotify, and SoundCloud integrations with nocTurneMeLoDieS V4 system
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from DISTROKID_INTEGRATION.distrokid_api import DistroKidIntegrationManager
from SOUNDCLOUD_INTEGRATION.soundcloud_api import SoundCloudIntegrationManager
from SPOTIFY_INTEGRATION.spotify_api import SpotifyIntegrationManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AvatarArtsDistributionManager:
    """Main manager for all music distribution platform integrations"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.local_storage_path = Path(config.get("local_storage_path", "/Users/steven/Music/nocTurneMeLoDieS"))

        # Initialize platform managers
        self.distrokid_manager = DistroKidIntegrationManager(
            {**config, "avatararts_analyzer": config.get("avatararts_analyzer")}
        )

        self.spotify_manager = SpotifyIntegrationManager(
            {**config, "avatararts_analyzer": config.get("avatararts_analyzer")}
        )

        self.soundcloud_manager = SoundCloudIntegrationManager(
            {**config, "avatararts_analyzer": config.get("avatararts_analyzer")}
        )

        # Directory for storing integration logs
        self.integration_logs_dir = self.local_storage_path / "AVATARARTS_DISTRIBUTION_LOGS"
        self.integration_logs_dir.mkdir(parents=True, exist_ok=True)

    async def initialize_all_platforms(self):
        """Initialize all platform integrations"""
        logger.info("Initializing all music distribution platform integrations")

        # Initialize all managers in parallel
        await asyncio.gather(
            self.distrokid_manager.initialize(), self.spotify_manager.initialize(), self.soundcloud_manager.initialize()
        )

        logger.info("All platform integrations initialized successfully")

    async def distribute_to_all_platforms(self, album_path: str) -> Dict[str, Any]:
        """Distribute an album to all platforms"""
        logger.info(f"Distributing album to all platforms: {album_path}")

        results = {
            "album_path": album_path,
            "distrokid_result": None,
            "spotify_result": None,
            "soundcloud_result": None,
            "errors": [],
            "start_time": datetime.now().isoformat(),
            "end_time": None,
        }

        try:
            # Distribute to DistroKid
            try:
                distrokid_result = await self.distrokid_manager.submit_album(album_path)
                results["distrokid_result"] = {
                    "success": True,
                    "submission_id": distrokid_result.submission_id,
                    "status": distrokid_result.status,
                    "estimated_release_date": distrokid_result.estimated_release_date,
                }
                logger.info(f"DistroKid distribution successful: {distrokid_result.submission_id}")
            except Exception as e:
                error_msg = f"DistroKid distribution failed: {str(e)}"
                logger.error(error_msg)
                results["errors"].append(error_msg)
                results["distrokid_result"] = {"success": False, "error": str(e)}

            # For Spotify and SoundCloud, we'll handle individual tracks from the album (per-track listing TBD)

            # Upload to SoundCloud
            try:
                soundcloud_result = await self.soundcloud_manager.upload_album_content(album_path)
                results["soundcloud_result"] = {
                    "success": True,
                    "tracks_found": soundcloud_result["tracks_found"],
                    "tracks_uploaded": soundcloud_result["tracks_uploaded"],
                }
                logger.info(f"SoundCloud upload successful: {soundcloud_result['tracks_uploaded']} tracks uploaded")
            except Exception as e:
                error_msg = f"SoundCloud upload failed: {str(e)}"
                logger.error(error_msg)
                results["errors"].append(error_msg)
                results["soundcloud_result"] = {"success": False, "error": str(e)}

        except Exception as e:
            error_msg = f"Critical error in distribution process: {str(e)}"
            logger.error(error_msg)
            results["errors"].append(error_msg)

        results["end_time"] = datetime.now().isoformat()

        # Log distribution result
        log_file = self.integration_logs_dir / f"distribution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(log_file, "w") as f:
            json.dump(results, f, indent=2)

        logger.info(f"Distribution completed for album: {album_path}")
        return results

    async def auto_distribute_new_content(self) -> Dict[str, Any]:
        """Automatically distribute all new content across all platforms"""
        logger.info("Starting auto-distribution of new content")

        results = {
            "albums_processed": 0,
            "albums_distributed": 0,
            "platform_distributions": {
                "distrokid": {"submitted": 0, "failed": 0},
                "spotify": {"playlists_created": 0, "failed": 0},
                "soundcloud": {"uploaded": 0, "failed": 0},
            },
            "errors": [],
            "start_time": datetime.now().isoformat(),
            "end_time": None,
        }

        # Get new albums for distribution
        new_albums = await self.distrokid_manager.detect_new_albums_for_distribution()

        for album_path in new_albums:
            try:
                logger.info(f"Processing album for distribution: {album_path}")

                # Distribute to all platforms
                distribution_result = await self.distribute_to_all_platforms(album_path)

                results["albums_processed"] += 1

                # Update platform-specific counters
                if distribution_result["distrokid_result"] and distribution_result["distrokid_result"]["success"]:
                    results["platform_distributions"]["distrokid"]["submitted"] += 1
                else:
                    results["platform_distributions"]["distrokid"]["failed"] += 1

                if distribution_result["soundcloud_result"] and distribution_result["soundcloud_result"]["success"]:
                    results["platform_distributions"]["soundcloud"]["uploaded"] += 1
                else:
                    results["platform_distributions"]["soundcloud"]["failed"] += 1

                results["albums_distributed"] += 1

                logger.info(f"Successfully distributed album: {Path(album_path).name}")

            except Exception as e:
                error_msg = f"Error distributing album {album_path}: {str(e)}"
                logger.error(error_msg)
                results["errors"].append(error_msg)

        # Create thematic playlists on Spotify
        try:
            spotify_results = await self.spotify_manager.create_theme_based_playlists()
            results["platform_distributions"]["spotify"]["playlists_created"] = spotify_results["playlists_created"]
        except Exception as e:
            error_msg = f"Spotify playlist creation failed: {str(e)}"
            logger.error(error_msg)
            results["errors"].append(error_msg)
            results["platform_distributions"]["spotify"]["failed"] += 1

        results["end_time"] = datetime.now().isoformat()

        # Save comprehensive results
        summary_file = (
            self.integration_logs_dir / f"auto_distribution_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(summary_file, "w") as f:
            json.dump(results, f, indent=2)

        logger.info(f"Auto-distribution completed: {results['albums_distributed']} albums distributed")
        return results

    async def monitor_all_platforms(self) -> Dict[str, Any]:
        """Monitor status across all platforms"""
        logger.info("Monitoring all platform distributions")

        results = {
            "distrokid_monitoring": None,
            "spotify_stats": None,
            "soundcloud_stats": None,
            "errors": [],
            "timestamp": datetime.now().isoformat(),
        }

        # Monitor DistroKid submissions
        try:
            distrokid_status = await self.distrokid_manager.monitor_submissions()
            results["distrokid_monitoring"] = {
                "active_submissions": len(distrokid_status),
                "statuses": distrokid_status,
            }
        except Exception as e:
            error_msg = f"DistroKid monitoring failed: {str(e)}"
            logger.error(error_msg)
            results["errors"].append(error_msg)

        # Get Spotify stats
        try:
            spotify_stats = await self.spotify_manager.get_artist_analytics()
            results["spotify_stats"] = spotify_stats
        except Exception as e:
            error_msg = f"Spotify stats retrieval failed: {str(e)}"
            logger.error(error_msg)
            results["errors"].append(error_msg)

        # Get SoundCloud stats
        try:
            soundcloud_stats = await self.soundcloud_manager.get_user_stats()
            results["soundcloud_stats"] = soundcloud_stats
        except Exception as e:
            error_msg = f"SoundCloud stats retrieval failed: {str(e)}"
            logger.error(error_msg)
            results["errors"].append(error_msg)

        # Save monitoring results
        monitor_file = self.integration_logs_dir / f"monitoring_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(monitor_file, "w") as f:
            json.dump(results, f, indent=2)

        logger.info("Platform monitoring completed")
        return results

    async def get_comprehensive_summary(self) -> Dict[str, Any]:
        """Get a comprehensive summary of all integrations"""
        logger.info("Getting comprehensive integration summary")

        summary = {
            "timestamp": datetime.now().isoformat(),
            "platform_integrations": {"distrokid": None, "spotify": None, "soundcloud": None},
            "overall_stats": {
                "total_albums_distributed": 0,
                "active_submissions": 0,
                "total_tracks_distributed": 0,
                "total_plays_across_platforms": 0,
            },
            "recent_activities": [],
        }

        # Get individual platform summaries
        try:
            summary["platform_integrations"]["distrokid"] = await self.distrokid_manager.get_artist_performance()
        except Exception as e:
            logger.error(f"Error getting DistroKid summary: {str(e)}")

        try:
            summary["platform_integrations"]["spotify"] = await self.spotify_manager.get_integration_summary()
        except Exception as e:
            logger.error(f"Error getting Spotify summary: {str(e)}")

        try:
            summary["platform_integrations"]["soundcloud"] = await self.soundcloud_manager.get_integration_summary()
        except Exception as e:
            logger.error(f"Error getting SoundCloud summary: {str(e)}")

        # Calculate overall stats
        # This would aggregate data from all platforms in a real implementation
        summary["overall_stats"]["total_albums_distributed"] = len(
            list((self.local_storage_path / "ALBUMS").glob("*"))
            if (self.local_storage_path / "ALBUMS").exists()
            else []
        )

        # Get recent activity logs
        log_files = list(self.integration_logs_dir.glob("*.json"))
        recent_logs = sorted(log_files, key=lambda x: x.stat().st_mtime, reverse=True)[:10]

        for log_file in recent_logs:
            try:
                with open(log_file, "r") as f:
                    log_data = json.load(f)
                    summary["recent_activities"].append(
                        {
                            "file": log_file.name,
                            "activity_type": log_file.stem.split("_")[0],
                            "timestamp": log_data.get("start_time", log_file.stat().st_mtime),
                            "summary": {k: v for k, v in log_data.items() if k not in ["errors"]},
                        }
                    )
            except Exception as e:
                logger.error(f"Error reading log file {log_file}: {str(e)}")

        # Save comprehensive summary
        summary_file = (
            self.integration_logs_dir / f"comprehensive_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2)

        logger.info("Comprehensive summary generated")
        return summary


# Example usage and testing
async def main():
    # Configuration
    config = {
        "local_storage_path": "/Users/steven/Music/nocTurneMeLoDieS",
        "artist_name": "AvatarArts",
        "label_name": "AvatarArts Creative Automation",
        "distrokid_api_key": None,  # Would be set in production
        "spotify_client_id": None,  # Would be set in production
        "spotify_client_secret": None,  # Would be set in production
        "soundcloud_access_token": None,  # Would be set in production
        "avatararts_analyzer": None,  # Placeholder for AvatarArts analyzer
    }

    # Initialize the main manager
    manager = AvatarArtsDistributionManager(config)
    await manager.initialize_all_platforms()

    # Example: Get comprehensive summary
    # summary = await manager.get_comprehensive_summary()
    # print("Comprehensive Summary:")
    # print(json.dumps(summary, indent=2))

    # Example: Auto-distribute new content
    # distribution_results = await manager.auto_distribute_new_content()
    # print(f"\nAuto-distribution results:")
    # print(json.dumps(distribution_results, indent=2))

    # Example: Monitor all platforms
    # monitoring_results = await manager.monitor_all_platforms()
    # print(f"\nMonitoring results:")
    # print(json.dumps(monitoring_results, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
