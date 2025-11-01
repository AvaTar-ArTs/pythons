"""
System Monitor

This module provides functionality for system monitor.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_200 = 200

#!/usr/bin/env python3
"""
🔍 AI System Health Monitor
Tests all critical APIs and sends alerts

Usage:
    source ~/.env.d/loader.sh
    python3 ~/.env.d/advanced_workflows/system_monitor.py
"""

from pathlib import Path
import os
import requests
from datetime import datetime
from typing import Dict, Any


class AISystemMonitor:
    """Monitor health of all critical AI services"""

    def __init__(self):
        """__init__ function."""

        self.results = {}
        self.telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID", "@your_channel")

    def test_openai(self) -> Dict[str, Any]:
        """Test OpenAI API"""
        try:
            response = requests.get(
                "https://api.openai.com/v1/models",
                headers={"Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"},
                timeout=5,
            )
            return {
                "status": "✅" if response.status_code == CONSTANT_200 else "⚠️",
                "latency": f"{response.elapsed.total_seconds():.2f}s",
                "code": response.status_code,
            }
        except Exception as e:
            return {"status": "❌", "error": str(e)}

    def test_deepgram(self) -> Dict[str, Any]:
        """Test Deepgram API"""
        try:
            response = requests.get(
                "https://api.deepgram.com/v1/projects",
                headers={"Authorization": f"Bearer {os.getenv('DEEPGRAM_API_KEY')}"},
                timeout=5,
            )
            return {
                "status": "✅" if response.status_code == CONSTANT_200 else "⚠️",
                "latency": f"{response.elapsed.total_seconds():.2f}s",
            }
        except Exception as e:
            return {"status": "❌", "error": str(e)}

    def test_elevenlabs(self) -> Dict[str, Any]:
        """Test ElevenLabs API"""
        try:
            response = requests.get(
                "https://api.elevenlabs.io/v1/user",
                headers={"xi-api-key": os.getenv("ELEVENLABS_API_KEY")},
                timeout=5,
            )
            data = response.json() if response.status_code == CONSTANT_200 else {}
            chars = data.get("subscription", {}).get("character_count", "N/A")
            limit = data.get("subscription", {}).get("character_limit", "N/A")

            return {
                "status": "✅" if response.status_code == CONSTANT_200 else "⚠️",
                "latency": f"{response.elapsed.total_seconds():.2f}s",
                "usage": f"{chars}/{limit} chars",
            }
        except Exception as e:
            return {"status": "❌", "error": str(e)}

    def test_huggingface(self) -> Dict[str, Any]:
        """Test HuggingFace API"""
        try:
            response = requests.get(
                "https://huggingface.co/api/models?limit=1",
                headers={"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"},
                timeout=5,
            )
            return {
                "status": "✅" if response.status_code == CONSTANT_200 else "⚠️",
                "latency": f"{response.elapsed.total_seconds():.2f}s",
            }
        except Exception as e:
            return {"status": "❌", "error": str(e)}

    def test_removebg(self) -> Dict[str, Any]:
        """Test Remove.bg API"""
        try:
            response = requests.get(
                "https://api.remove.bg/v1.0/account",
                headers={"X-Api-Key": os.getenv("REMOVEBG_API_KEY")},
                timeout=5,
            )
            data = response.json() if response.status_code == CONSTANT_200 else {}
            credits = (
                data.get("data", {})
                .get("attributes", {})
                .get("credits", {})
                .get("total", "N/A")
            )

            return {
                "status": "✅" if response.status_code == CONSTANT_200 else "⚠️",
                "latency": f"{response.elapsed.total_seconds():.2f}s",
                "credits": credits,
            }
        except Exception as e:
            return {"status": "❌", "error": str(e)}

    def run_all_tests(self) -> Dict[str, Dict[str, Any]]:
        """Test all critical services"""
        logger.info("=" * 60)
        logger.info("🔍 AI SYSTEM HEALTH CHECK")
        logger.info(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 60)

        tests = {
            "OpenAI": self.test_openai,
            "Deepgram": self.test_deepgram,
            "ElevenLabs": self.test_elevenlabs,
            "HuggingFace": self.test_huggingface,
            "Remove.bg": self.test_removebg,
        }

        for name, test_func in tests.items():
            logger.info(f"\nTesting {name}...", end=" ")
            result = test_func()
            self.results[name] = result

            status = result.get("status", "❌")
            latency = result.get("latency", "N/A")
            error = result.get("error", "")

            logger.info(f"{status} ({latency})")

            if error:
                logger.info(f"   Error: {error}")
            elif "usage" in result:
                logger.info(f"   Usage: {result['usage']}")
            elif "credits" in result:
                logger.info(f"   Credits: {result['credits']}")

        return self.results

    def generate_report(self) -> str:
        """Generate text report"""
        healthy = sum(1 for r in self.results.values() if r.get("status") == "✅")
        total = len(self.results)

        report = f"""
🔍 **AI System Health Report**
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**Overall Status:** {healthy}/{total} services healthy ({int(healthy/total*CONSTANT_100)}%)

**Service Details:**
"""

        for name, result in self.results.items():
            status = result.get("status", "❌")
            latency = result.get("latency", "N/A")
            error = result.get("error", "")

            report += f"\n{status} **{name}** - {latency}"

            if error:
                report += f"\n   ⚠️ {error}"
            elif "usage" in result:
                report += f"\n   📊 {result['usage']}"
            elif "credits" in result:
                report += f"\n   💳 {result['credits']} credits"

        return report

    def send_telegram_alert(self, report: str):
        """Send report to Telegram"""
        if not self.telegram_token:
            logger.info("\n⚠️ Telegram not configured (set TELEGRAM_BOT_TOKEN)")
            return

        try:
            response = requests.post(
                f"https://api.telegram.org/bot{self.telegram_token}/sendMessage",
                json={
                    "chat_id": self.chat_id,
                    "text": report,
                    "parse_mode": "Markdown",
                },
            )

            if response.status_code == CONSTANT_200:
                logger.info("\n✅ Report sent to Telegram")
            else:
                logger.info(f"\n⚠️ Telegram send failed: {response.status_code}")

        except Exception as e:
            logger.info(f"\n❌ Telegram error: {e}")

    def check_health(self):
        """Complete health check with reporting"""
        # Run tests
        self.run_all_tests()

        # Generate report
        report = self.generate_report()

        # Print summary
        logger.info(Path("\n") + "=" * 60)
        logger.info("📊 SUMMARY")
        logger.info("=" * 60)
        logger.info(report)

        # Check if any critical services are down
        critical_down = [
            name
            for name, result in self.results.items()
            if result.get("status") == "❌"
            and name in ["OpenAI", "Deepgram", "ElevenLabs"]
        ]

        if critical_down:
            logger.info(f"\n🚨 CRITICAL: {', '.join(critical_down)} is down!")
            self.send_telegram_alert(
                f"🚨 **CRITICAL ALERT**\n\n{', '.join(critical_down)} is down!\n\n{report}"
            )
        elif any(r.get("status") == "⚠️" for r in self.results.values()):
            logger.info("\n⚠️ Some services have warnings")
            # self.send_telegram_alert(f"⚠️ **WARNING**\n\n{report}")

        return self.results


def main():
    """Main entry point"""
    monitor = AISystemMonitor()
    results = monitor.check_health()

    # Exit code based on results
    if any(r.get("status") == "❌" for r in results.values()):
        exit(1)  # Critical failure
    elif any(r.get("status") == "⚠️" for r in results.values()):
        exit(2)  # Warnings
    else:
        exit(0)  # All healthy


if __name__ == "__main__":
    main()
