import csv
import logging
import os
import time
from datetime import datetime
from pathlib import Path
from pathlib import Path as PathLib

from PIL import Image, UnidentifiedImageError
from dotenv import load_dotenv


def load_env_d():
    """Load all .env files from ~/.env.d directory (sophisticated pattern from youtube-load.py)"""
    env_d_path = PathLib.home() / ".env.d"
    if env_d_path.exists():
        for env_file in env_d_path.glob("*.env"):
            try:
                with open(env_file) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            # Handle export statements
                            line = line.removeprefix("export ")
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            # Skip source statements
                            if not key.startswith("source"):
                                os.environ[key] = value
            except Exception as e:
                # Logger not initialized yet, use print
                print(f"Warning: Error loading {env_file}: {e}")


load_env_d()

# Also load from ~/.env as fallback using dotenv
try:
    load_dotenv(os.path.expanduser("~/.env"))
except ImportError:

    # Load API keys from ~/.env.d/

    for env_file in env_dir.glob("*.env"):
        load_dotenv(env_file)


logger = logging.getLogger(__name__)


# Constants
CONSTANT_300 = 300
CONSTANT_720 = 720
CONSTANT_1024 = 1024
CONSTANT_1080 = 1080
CONSTANT_1280 = 1280
CONSTANT_1920 = 1920
CONSTANT_4500 = 4500
CONSTANT_5400 = 5400


# Load environment variables
env_path = Path(str(Path.home()) + "/.env")
load_dotenv(dotenv_path=env_path)

# Initialize OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise OSError("OpenAI API key not found. Please check your .env file.")

# Constants
MAX_WIDTH, MAX_HEIGHT = CONSTANT_4500, CONSTANT_5400
TARGET_DPI = CONSTANT_300
BATCH_SIZE = 50
PAUSE_DURATION = 5
ASPECT_RATIO_MINIMUMS = {
    "16:9": (CONSTANT_720, CONSTANT_1280),  # Landscape
    "9:16": (CONSTANT_1080, CONSTANT_1920),  # Portrait
    "1:1": (CONSTANT_1024, CONSTANT_1024),  # Square
}


# Function to sanitize filenames
def sanitize_filename(filename, file_ext):
    """Function."""
    filename = filename.strip('"').replace(" ", "_").replace("/", "_").replace(":", "_")
    filename = os.path.splitext(filename)[0]  # Remove any existing extension
    return f"{filename}.{file_ext}"


# Function to get the closest aspect ratio
def get_closest_aspect_ratio(width, height):
    aspect_ratios = {
        "16:9": 16 / 9,
        "9:16": 9 / 16,
        "1:1": 1 / 1,
    }
    current_ratio = width / height
    closest_ratio = min(
        aspect_ratios,
        key=lambda ar: abs(current_ratio - aspect_ratios[ar]),
    )
    return closest_ratio, ASPECT_RATIO_MINIMUMS[closest_ratio]


# Function to resize images
def resize_image(im, output_path):
    width, height = im.size
    closest_ratio, (min_width, min_height) = get_closest_aspect_ratio(width, height)
    aspect_ratio = width / height

    logger.info(f"🎨 Detected Aspect Ratio: {closest_ratio} ({aspect_ratio:.2f})")

    if width < min_width or height < min_height:
        if closest_ratio == "16:9":
            new_width, new_height = min_width, int(min_width / aspect_ratio)
        elif closest_ratio == "9:16":
            new_height, new_width = min_height, int(min_height * aspect_ratio)
        elif closest_ratio == "1:1":
            new_width, new_height = max(min_width, min_height), max(
                min_width,
                min_height,
            )
    elif width > MAX_WIDTH or height > MAX_HEIGHT:
        if width / MAX_WIDTH > height / MAX_HEIGHT:
            new_width, new_height = MAX_WIDTH, int(MAX_WIDTH / aspect_ratio)
        else:
            new_height, new_width = MAX_HEIGHT, int(MAX_HEIGHT * aspect_ratio)
    else:
        new_width, new_height = width, height

    logger.info(
        f"🔄 Resizing to: {new_width}x{new_height} for aspect ratio {closest_ratio}",
    )
    im = im.resize((new_width, new_height), Image.LANCZOS)
    im.save(output_path, dpi=(TARGET_DPI, TARGET_DPI), quality=85, format="JPEG")
    return im


# Function to process a batch of images
def process_batch(batch, root, csv_rows):
    for file in batch:
        file_path = os.path.join(root, file)
        file_ext = file.lower().split(".")[-1]

        if file_ext not in ("jpg", "jpeg", "png"):
            logger.info(f"⚠️ Skipping {file}: Unsupported file format.")
            continue

        try:
            im = Image.open(file_path)
            width, height = im.size
            logger.info(f"\n🖼️ Processing {file}: Original size: {width}x{height}")

            if file_ext in ("jpg", "jpeg") and im.mode != "RGB":
                im = im.convert("RGB")
                logger.info(f"Converted {file} to RGB format.")

            sanitized_filename = sanitize_filename(os.path.splitext(file)[0], file_ext)
            temp_file = os.path.join(root, f"{sanitized_filename}_temp.{file_ext}")
            resize_image(im, temp_file)

            new_file_path = os.path.join(root, sanitized_filename)
            os.remove(file_path)
            os.rename(temp_file, new_file_path)
            resized_size = os.path.getsize(new_file_path)

            creation_date = datetime.fromtimestamp(
                os.path.getctime(new_file_path),
            ).strftime("%m-%d-%y")
            csv_rows.append(
                [
                    sanitized_filename,
                    f"{resized_size / (CONSTANT_1024 ** 2):.2f} MB",
                    creation_date,
                    width,
                    height,
                    TARGET_DPI,
                    TARGET_DPI,
                    new_file_path,
                ],
            )
            logger.info(f"✅ Successfully resized {file} and saved to {new_file_path}")

        except UnidentifiedImageError:
            logger.info(f"⚠️ Skipping {file}: Cannot identify image.")
        except Exception as e:
            logger.info(f"⚠️ Error processing {file}: {e}")


# Function to process images and generate metadata
def process_images_and_generate_csv(source_directory, csv_path):
    rows = []
    batch = []

    for root, _, files in os.walk(source_directory):
        for file in files:
            batch.append(file)
            if len(batch) >= BATCH_SIZE:
                logger.info(f"🔄 Processing batch of {BATCH_SIZE} images in {root}...")
                process_batch(batch, root, rows)
                batch = []
                logger.info(f"⏸️ Pausing for {PAUSE_DURATION} seconds...")
                time.sleep(PAUSE_DURATION)

        if batch:
            logger.info(f"🔄 Processing remaining {len(batch)} images in {root}...")
            process_batch(batch, root, rows)
            batch = []

    write_csv(csv_path, rows)
    logger.info(f"📄 CSV metadata saved to: {csv_path}")


# Function to write rows to CSV
def write_csv(csv_path, rows):
    with open(csv_path, "w", newline="") as csvfile:
        fieldnames = [
            "Filename",
            "File Size",
            "Creation Date",
            "Width",
            "Height",
            "DPI_X",
            "DPI_Y",
            "Original Path",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "Filename": row[0],
                    "File Size": row[1],
                    "Creation Date": row[2],
                    "Width": row[3],
                    "Height": row[4],
                    "DPI_X": row[5],
                    "DPI_Y": row[6],
                    "Original Path": row[7],
                },
            )


# Main function
def main():
    source_directory = input(
        "Enter the path to the source directory containing images: ",
    ).strip()
    if not os.path.isdir(source_directory):
        logger.info("Source directory does not exist.")
        return

    current_date = datetime.now().strftime("%m-%d-%y")
    csv_output_path = os.path.join(source_directory, f"image_data-{current_date}.csv")
    process_images_and_generate_csv(source_directory, csv_output_path)


if __name__ == "__main__":
    main()
