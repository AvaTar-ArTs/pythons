"""
Enhanced Gallery Build Module for SimpleGallery
Integrates content awareness and AI-powered features
"""

import argparse
import os
import sys
import json
import jinja2
from collections import OrderedDict
import simplegallery.common as spg_common
from simplegallery.logic.gallery_logic import get_gallery_logic
from simplegallery.enhanced_metadata import get_enhanced_metadata
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_args():
    """
    Configures the argument parser for enhanced gallery build
    :return: Parsed arguments
    """
    description = """Build an enhanced gallery with content awareness and AI-powered features.
                    Generates all files needed to display the gallery with advanced content analysis.
                    For detailed documentation please refer to https://github.com/haltakov/simple-photo-gallery."""

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        "-p",
        "--path",
        dest="path",
        action="store",
        default=".",
        help="Path to the folder containing the gallery.json file",
    )

    parser.add_argument(
        "-ft",
        "--force-thumbnails",
        dest="force_thumbnails",
        action="store_true",
        help="Forces the generation of the thumbnails even if they already exist",
    )

    parser.add_argument(
        "--enhanced",
        dest="enhanced",
        action="store_true",
        help="Enable enhanced content analysis and AI features",
    )

    parser.add_argument(
        "--ai-analysis",
        dest="ai_analysis",
        action="store_true",
        help="Enable AI-powered content analysis (requires additional dependencies)",
    )

    parser.add_argument(
        "--content-tags",
        dest="content_tags",
        action="store_true",
        help="Generate automatic content tags based on image analysis",
    )

    parser.add_argument(
        "--quality-scoring",
        dest="quality_scoring",
        action="store_true",
        help="Enable automatic quality scoring for images",
    )

    parser.add_argument(
        "--face-detection",
        dest="face_detection",
        action="store_true",
        help="Enable face detection and analysis",
    )

    parser.add_argument(
        "--color-analysis",
        dest="color_analysis",
        action="store_true",
        help="Enable detailed color palette analysis",
    )

    parser.add_argument(
        "--template",
        dest="template",
        action="store",
        default="enhanced",
        choices=["enhanced", "original"],
        help="Choose template type: 'enhanced' for content-aware version, 'original' for standard version",
    )

    return parser.parse_args()


def build_enhanced_html(gallery_config, images_data, background_photo, remote_data):
    """
    Generates the enhanced HTML file with content awareness features
    :param gallery_config: Gallery configuration dictionary
    :param images_data: Images data with enhanced metadata
    :param background_photo: Background photo filename
    :param remote_data: Remote gallery data
    """
    # Convert images data to list format
    images_data_list = [
        {**images_data[image], "name": image} for image in images_data.keys()
    ]

    # Setup the jinja2 environment
    template_name = (
        "enhanced_index_template.jinja"
        if gallery_config.get("template", "enhanced") == "enhanced"
        else "index_template.jinja"
    )
    file_loader = jinja2.FileSystemLoader(gallery_config["templates_path"])
    env = jinja2.Environment(loader=file_loader)

    # Render the HTML template
    template = env.get_template(template_name)
    html = template.render(
        images=images_data_list,
        gallery_config=gallery_config,
        background_photo=background_photo,
        remote_data=remote_data,
    )

    # Write the HTML file
    with open(
        os.path.join(gallery_config["public_path"], "index.html"), "w", encoding="utf-8"
    ) as out:
        out.write(html)


def enhance_images_data(images_data, gallery_config, enhanced_features):
    """
    Enhance images data with content analysis
    :param images_data: Original images data
    :param gallery_config: Gallery configuration
    :param enhanced_features: Dictionary of enabled features
    :return: Enhanced images data
    """
    logger.info("Enhancing images data with content analysis...")

    enhanced_data = {}

    for image_name, image_data in images_data.items():
        logger.info(f"Processing {image_name}...")

        # Start with original data
        enhanced_image_data = image_data.copy()

        # Add enhanced metadata if enabled
        if enhanced_features.get("enhanced", False):
            try:
                image_path = os.path.join(gallery_config["images_path"], image_name)
                thumbnail_path = os.path.join(
                    gallery_config["thumbnails_path"], image_name
                )
                public_path = gallery_config["public_path"]

                # Get enhanced metadata
                enhanced_metadata = get_enhanced_metadata(
                    image_path, thumbnail_path, public_path
                )
                enhanced_image_data.update(enhanced_metadata)

            except Exception as e:
                logger.warning(f"Failed to enhance metadata for {image_name}: {e}")
                # Add empty enhanced metadata structure
                enhanced_image_data.update(
                    {
                        "content_analysis": {},
                        "color_analysis": {},
                        "composition_analysis": {},
                        "text_content": {"has_text": False, "extracted_text": ""},
                        "face_analysis": {"face_count": 0, "faces_detected": False},
                        "scene_classification": {},
                        "quality_metrics": {},
                        "temporal_context": {},
                        "geographic_data": {},
                        "device_info": {},
                        "aesthetic_score": {
                            "overall_aesthetic_score": 0.5,
                            "aesthetic_grade": "C",
                        },
                    }
                )

        enhanced_data[image_name] = enhanced_image_data

    return enhanced_data


def generate_content_analysis_report(enhanced_data, gallery_config):
    """
    Generate a content analysis report for the gallery
    :param enhanced_data: Enhanced images data
    :param gallery_config: Gallery configuration
    """
    logger.info("Generating content analysis report...")

    # Analyze overall gallery statistics
    total_images = len(enhanced_data)
    images_with_faces = sum(
        1
        for img in enhanced_data.values()
        if img.get("face_analysis", {}).get("faces_detected", False)
    )
    images_with_text = sum(
        1
        for img in enhanced_data.values()
        if img.get("text_content", {}).get("has_text", False)
    )

    # Quality distribution
    quality_grades = {"A": 0, "B": 0, "C": 0, "D": 0}
    for img in enhanced_data.values():
        grade = img.get("aesthetic_score", {}).get("aesthetic_grade", "C")
        if grade in quality_grades:
            quality_grades[grade] += 1

    # Color analysis
    all_colors = []
    for img in enhanced_data.values():
        colors = img.get("color_analysis", {}).get("dominant_colors", [])
        all_colors.extend(colors)

    # Scene classification
    scene_categories = {}
    for img in enhanced_data.values():
        scene = img.get("scene_classification", {}).get("scene_category", "unknown")
        scene_categories[scene] = scene_categories.get(scene, 0) + 1

    # Generate report
    report = {
        "total_images": total_images,
        "images_with_faces": images_with_faces,
        "face_percentage": (images_with_faces / total_images * 100)
        if total_images > 0
        else 0,
        "images_with_text": images_with_text,
        "text_percentage": (images_with_text / total_images * 100)
        if total_images > 0
        else 0,
        "quality_distribution": quality_grades,
        "top_colors": sorted(
            all_colors, key=lambda x: x.get("percentage", 0), reverse=True
        )[:10],
        "scene_categories": dict(
            sorted(scene_categories.items(), key=lambda x: x[1], reverse=True)
        ),
        "generated_at": str(
            os.path.getctime(os.path.join(gallery_config["public_path"], "index.html"))
        ),
    }

    # Save report
    report_path = os.path.join(
        gallery_config["public_path"], "content_analysis_report.json"
    )
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    logger.info(f"Content analysis report saved to {report_path}")
    return report


def copy_enhanced_assets(gallery_config):
    """
    Copy enhanced CSS and JavaScript assets
    :param gallery_config: Gallery configuration
    """
    logger.info("Copying enhanced assets...")

    # Copy enhanced CSS
    enhanced_css_src = os.path.join(
        os.path.dirname(__file__), "data", "public", "css", "enhanced-main.css"
    )
    enhanced_css_dst = os.path.join(
        gallery_config["public_path"], "css", "enhanced-main.css"
    )

    if os.path.exists(enhanced_css_src):
        import shutil

        shutil.copy2(enhanced_css_src, enhanced_css_dst)
        logger.info("Enhanced CSS copied")

    # Copy enhanced JavaScript
    enhanced_js_src = os.path.join(
        os.path.dirname(__file__), "data", "public", "js", "enhanced-main.js"
    )
    enhanced_js_dst = os.path.join(
        gallery_config["public_path"], "js", "enhanced-main.js"
    )

    if os.path.exists(enhanced_js_src):
        import shutil

        shutil.copy2(enhanced_js_src, enhanced_js_dst)
        logger.info("Enhanced JavaScript copied")

    # Copy enhanced templates
    enhanced_template_src = os.path.join(
        os.path.dirname(__file__), "data", "templates", "enhanced_index_template.jinja"
    )
    enhanced_template_dst = os.path.join(
        gallery_config["templates_path"], "enhanced_index_template.jinja"
    )

    if os.path.exists(enhanced_template_src):
        import shutil

        shutil.copy2(enhanced_template_src, enhanced_template_dst)
        logger.info("Enhanced template copied")

    # Copy enhanced macros
    enhanced_macros_src = os.path.join(
        os.path.dirname(__file__), "data", "templates", "enhanced_gallery_macros.jinja"
    )
    enhanced_macros_dst = os.path.join(
        gallery_config["templates_path"], "enhanced_gallery_macros.jinja"
    )

    if os.path.exists(enhanced_macros_src):
        import shutil

        shutil.copy2(enhanced_macros_src, enhanced_macros_dst)
        logger.info("Enhanced macros copied")


def main():
    """
    Builds the enhanced HTML gallery with content awareness features
    """
    # Parse the arguments
    args = parse_args()

    # Read the gallery config
    gallery_root = args.path
    gallery_config_path = os.path.join(gallery_root, "gallery.json")
    gallery_config = spg_common.read_gallery_config(gallery_config_path)
    if not gallery_config:
        spg_common.log(f"Cannot load the gallery.json file ({gallery_config_path})!")
        sys.exit(1)

    # Add enhanced features to config
    enhanced_features = {
        "enhanced": args.enhanced,
        "ai_analysis": args.ai_analysis,
        "content_tags": args.content_tags,
        "quality_scoring": args.quality_scoring,
        "face_detection": args.face_detection,
        "color_analysis": args.color_analysis,
        "template": args.template,
    }

    gallery_config.update(enhanced_features)

    spg_common.log("Building the Enhanced Simple Photo Gallery...")

    # Get the gallery logic
    gallery_logic = get_gallery_logic(gallery_config)

    # Check if thumbnails exist and generate them if needed or if specified by the user
    try:
        spg_common.log("Generating thumbnails...")
        gallery_logic.create_thumbnails(args.force_thumbnails)
    except spg_common.SPGException as exception:
        spg_common.log(exception.message)
        sys.exit(1)
    except Exception as exception:
        spg_common.log(
            f"Something went wrong while generating the thumbnails: {str(exception)}"
        )
        sys.exit(1)

    # Generate the images_data.json
    try:
        spg_common.log("Generating the images_data.json file...")
        gallery_logic.create_images_data_file()
        spg_common.log(
            "The image descriptions are stored in images_data.json. You can edit the file to add more "
            "descriptions and build the gallery again."
        )
    except spg_common.SPGException as exception:
        spg_common.log(exception.message)
        sys.exit(1)
    except Exception as exception:
        spg_common.log(
            f"Something went wrong while generating the images_data.json file: {str(exception)}"
        )
        sys.exit(1)

    # Load the images_data for enhancement
    with open(gallery_config["images_data_file"], "r") as images_data_in:
        images_data = json.load(images_data_in, object_pairs_hook=OrderedDict)

    # Enhance images data with content analysis
    if enhanced_features.get("enhanced", False):
        try:
            spg_common.log("Enhancing images with content analysis...")
            enhanced_images_data = enhance_images_data(
                images_data, gallery_config, enhanced_features
            )

            # Save enhanced images data
            enhanced_images_data_file = os.path.join(
                gallery_root, "enhanced_images_data.json"
            )
            with open(enhanced_images_data_file, "w", encoding="utf-8") as f:
                json.dump(
                    enhanced_images_data, f, indent=2, ensure_ascii=False, default=str
                )

            spg_common.log(f"Enhanced images data saved to {enhanced_images_data_file}")

            # Generate content analysis report
            generate_content_analysis_report(enhanced_images_data, gallery_config)

            # Use enhanced data for HTML generation
            images_data = enhanced_images_data

        except Exception as exception:
            spg_common.log(
                f"Something went wrong while enhancing images data: {str(exception)}"
            )
            spg_common.log("Continuing with standard gallery build...")

    # Copy enhanced assets if using enhanced template
    if enhanced_features.get("template") == "enhanced":
        try:
            copy_enhanced_assets(gallery_config)
        except Exception as exception:
            spg_common.log(f"Warning: Could not copy enhanced assets: {str(exception)}")

    # Build the HTML from the templates
    try:
        spg_common.log("Creating the enhanced index.html...")

        # Remove descriptions if the corresponding option is enabled
        if "disable_captions" in gallery_config and gallery_config["disable_captions"]:
            for image in images_data:
                images_data[image]["description"] = ""

        # Use folder name as gallery title
        gallery_title = os.path.basename(os.path.abspath(gallery_root))
        gallery_config["title"] = gallery_title

        # Find the first photo for the background if no background photo specified
        background_photo = gallery_config.get("background_photo", "")
        if not background_photo:
            for image in images_data:
                if images_data[image]["type"] == "image":
                    background_photo = image
                    break

        # Remove description and URL from config for cleaner output
        gallery_config["description"] = ""
        gallery_config["url"] = ""

        # Collect the information for a remote gallery attribution
        remote_data = {}
        if "remote_gallery_type" in gallery_config and "remote_link" in gallery_config:
            remote_data["link"] = gallery_config["remote_link"]

            if gallery_config["remote_gallery_type"] == "google":
                remote_data["text"] = "Google Photos album"
            elif gallery_config["remote_gallery_type"] == "onedrive":
                remote_data["text"] = "OneDrive album"
            else:
                remote_data["text"] = "shared album"

        # Build the enhanced HTML
        build_enhanced_html(gallery_config, images_data, background_photo, remote_data)

    except Exception as exception:
        spg_common.log(
            f"Something went wrong while generating the gallery HTML: {str(exception)}"
        )
        sys.exit(1)

    spg_common.log(
        "The enhanced gallery was built successfully. Open public/index.html to view it."
    )

    if enhanced_features.get("enhanced", False):
        spg_common.log("Enhanced features enabled:")
        if enhanced_features.get("ai_analysis", False):
            spg_common.log("  - AI-powered content analysis")
        if enhanced_features.get("content_tags", False):
            spg_common.log("  - Automatic content tagging")
        if enhanced_features.get("quality_scoring", False):
            spg_common.log("  - Quality scoring")
        if enhanced_features.get("face_detection", False):
            spg_common.log("  - Face detection")
        if enhanced_features.get("color_analysis", False):
            spg_common.log("  - Color analysis")


if __name__ == "__main__":
    main()
