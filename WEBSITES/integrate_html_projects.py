import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#!/usr/bin/env python3
"""
Integrate existing HTML projects with Creative AI Empire
"""

import shutil
from pathlib import Path


def integrate_html_projects():
    """Integrate existing HTML projects with the empire"""

    # Source and destination paths
    source_html = Path("/Users/steven/Documents/HTML")
    empire_html = Path("/Users/steven/ai-sites/legacy-html-projects")

    # Create legacy projects directory
    empire_html.mkdir(exist_ok=True)

    # Categories to integrate
    categories = {
        "portfolios": ["portfolios", "gallery"],
        "landing_pages": ["landing", "demos"],
        "tools": ["tools", "cheetsheet"],
        "misc": ["misc", "zips"],
    }

    integrated_count = 0

    for category, dirs in categories.items():
        category_path = empire_html / category
        category_path.mkdir(exist_ok=True)

        for dir_name in dirs:
            source_dir = source_html / dir_name
            if source_dir.exists():
                dest_dir = category_path / dir_name
                if not dest_dir.exists():
                    shutil.copytree(source_dir, dest_dir)
                    integrated_count += 1
                    print(f"Integrated: {dir_name} -> {category}")

    print(f"✅ Integrated {integrated_count} HTML project directories")

    # Create integration manifest
    manifest = {
        "integrated_projects": integrated_count,
        "categories": list(categories.keys()),
        "source_path": str(source_html),
        "destination_path": str(empire_html),
    }

    import json

    with open(empire_html / "integration_manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)


try:
        integrate_html_projects()
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)