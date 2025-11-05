#!/usr/bin/env python3
"""
Master Runner for All Rename Utilities
Demonstrates and runs all advanced renaming capabilities
"""

import argparse
import sys
from pathlib import Path
from typing import List, Dict, Any

# Import all renamers
from master_renamer import MasterRenamer
from intelligent_renamer import IntelligentRenamer
from content_aware_renamer import ContentAwareRenamer
from deep_content_renamer import DeepContentRenamer
from thinketh_renamer import ThinkethRenamer

# Optional imports
try:
    from ocr_gpt_renamer import OCRGPTRenamer

    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


class RenameRunner:
    """Master runner for all rename utilities"""

    def __init__(self):
        """__init__ function."""

        self.renamers = {
            "master": MasterRenamer,
            "intelligent": IntelligentRenamer,
            "content": ContentAwareRenamer,
            "deep": DeepContentRenamer,
            "thinketh": ThinkethRenamer,
        }

        if OCR_AVAILABLE:
            self.renamers["ocr"] = OCRGPTRenamer

    def list_renamers(self):
        """List all available renamers"""
        logger.info("🚀 Available Rename Utilities:")
        logger.info("=" * 50)

        for name, renamer_class in self.renamers.items():
            doc = renamer_class.__doc__ or "No description available"
            logger.info(f"📝 {name.upper()}")
            logger.info(f"   {doc.strip()}")
            print()

    def run_renamer(self, renamer_name: str, target_path: Path, **kwargs):
        """Run a specific renamer"""
        if renamer_name not in self.renamers:
            logger.info(f"❌ Unknown renamer: {renamer_name}")
            logger.info(f"Available: {', '.join(self.renamers.keys())}")
            return False

        try:
            renamer_class = self.renamers[renamer_name]

            # Special handling for different renamers
            if renamer_name == "master":
                renamer = renamer_class(target_path)
                suggestions = renamer.analyze_project()
                if kwargs.get("apply", False):
                    renamer.apply_renames(suggestions, auto_approve=True)
                return True

            elif renamer_name == "intelligent":
                renamer = renamer_class(target_path)
                suggestions = renamer.analyze_project()
                if kwargs.get("apply", False):
                    renamer.apply_renames(suggestions, auto_approve=True)
                return True

            elif renamer_name == "content":
                renamer = renamer_class(target_path)
                renamer.process_directory()
                return True

            elif renamer_name == "deep":
                renamer = renamer_class()
                renamer.analyze_and_rename(
                    target_path, apply=kwargs.get("apply", False)
                )
                return True

            elif renamer_name == "thinketh":
                renamer = renamer_class(target_path)
                renamer.process_directory()
                return True

            elif renamer_name == "ocr":
                if not OCR_AVAILABLE:
                    logger.info("❌ OCR renamer requires additional dependencies")
                    logger.info(
                        "Install with: pip install opencv-python pytesseract pillow openai python-dotenv"
                    )
                    return False

                renamer = renamer_class()
                rows = renamer.walk_and_process(
                    target_path,
                    apply=kwargs.get("apply", False),
                    confirm=not kwargs.get("yes", False),
                )
                logger.info(f"Processed {len(rows)} files")
                return True

            return False

        except Exception as e:
            logger.info(f"❌ Error running {renamer_name}: {e}")
            return False

    def run_all_renamers(self, target_path: Path, apply: bool = False):
        """Run all renamers on the target path"""
        logger.info(f"🚀 Running all renamers on: {target_path}")
        logger.info("=" * 60)

        results = {}

        for name in self.renamers.keys():
            logger.info(f"\n📝 Running {name.upper()} renamer...")
            logger.info("-" * 30)

            try:
                success = self.run_renamer(name, target_path, apply=apply)
                results[name] = success

                if success:
                    logger.info(f"✅ {name.upper()} completed successfully")
                else:
                    logger.info(f"❌ {name.upper()} failed")

            except Exception as e:
                logger.info(f"❌ {name.upper()} error: {e}")
                results[name] = False

        # Summary
        logger.info(Path("\n") + "=" * 60)
        logger.info("📊 SUMMARY")
        logger.info("=" * 60)

        successful = sum(1 for success in results.values() if success)
        total = len(results)

        for name, success in results.items():
            status = "✅ SUCCESS" if success else "❌ FAILED"
            logger.info(f"{name.upper():15} {status}")

        logger.info(f"\nOverall: {successful}/{total} renamers completed successfully")

        return results

    def demo_renamers(self, target_path: Path):
        """Demonstrate all renamers with dry run"""
        logger.info("🎬 RENAME UTILITIES DEMO")
        logger.info("=" * 60)
        logger.info(f"Target: {target_path}")
        logger.info("Mode: DRY RUN (no changes will be made)")
        print()

        # Run each renamer in demo mode
        for name in self.renamers.keys():
            logger.info(f"🔍 Demo: {name.upper()} renamer")
            logger.info("-" * 40)

            try:
                self.run_renamer(name, target_path, apply=False)
                logger.info(f"✅ {name.upper()} demo completed")
            except Exception as e:
                logger.info(f"❌ {name.upper()} demo error: {e}")

            print()


def main():
    """main function."""

    parser = argparse.ArgumentParser(
        description="Master Runner for All Rename Utilities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all available renamers
  python run_renamers.py --list

  # Demo all renamers (dry run)
  python run_renamers.py --demo /path/to/project

  # Run specific renamer
  python run_renamers.py --renamer master /path/to/project

  # Run all renamers with apply
  python run_renamers.py --all /path/to/project --apply

  # Run OCR renamer on media files
  python run_renamers.py --renamer ocr /path/to/media --apply
        """,
    )

    parser.add_argument(
        "path", type=Path, nargs="?", help="Target directory to process"
    )

    parser.add_argument(
        "--list", action="store_true", help="List all available renamers"
    )

    parser.add_argument(
        "--demo", action="store_true", help="Demo all renamers (dry run)"
    )

    parser.add_argument("--all", action="store_true", help="Run all renamers")

    parser.add_argument(
        "--renamer",
        choices=["master", "intelligent", "content", "deep", "thinketh", "ocr"],
        help="Run specific renamer",
    )

    parser.add_argument(
        "--apply", action="store_true", help="Actually apply changes (default: dry run)"
    )

    parser.add_argument("--yes", action="store_true", help="Skip confirmation prompts")

    args = parser.parse_args()

    runner = RenameRunner()

    # List renamers
    if args.list:
        runner.list_renamers()
        return

    # Check if path is provided for other operations
    if not args.path:
        logger.info(
            "❌ Error: Path required for demo, all, or specific renamer operations"
        )
        logger.info("Use --list to see available renamers")
        return

    if not args.path.exists():
        logger.info(f"❌ Error: Path does not exist: {args.path}")
        return

    # Demo mode
    if args.demo:
        runner.demo_renamers(args.path)
        return

    # Run all renamers
    if args.all:
        runner.run_all_renamers(args.path, apply=args.apply)
        return

    # Run specific renamer
    if args.renamer:
        success = runner.run_renamer(
            args.renamer, args.path, apply=args.apply, yes=args.yes
        )
        sys.exit(0 if success else 1)

    # Default: show help
    parser.print_help()


if __name__ == "__main__":
    main()
