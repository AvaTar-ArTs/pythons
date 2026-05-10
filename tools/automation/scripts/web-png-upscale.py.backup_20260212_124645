import os

from PIL import Image


def convert_and_upscale_images(directory):
    # Walk through all directories and files within the specified directory
    for root, _, files in os.walk(directory):
        print(f"Checking directory: {root}")  # Debug statement
        for filename in files:
            print(f"Found file: {filename}")  # Debug statement
            if filename.lower().endswith(".webp") or filename.lower().endswith(".webp"):
                print(f"Processing file: {filename}")  # Debug statement
                # Construct full file path
                file_path = os.path.join(root, filename)
                try:
                    # Open the .tiff image
                    with Image.open(file_path) as img:
                        # Upscale the image by 2x
                        img = img.resize((img.width * 2, img.height * 2), Image.LANCZOS)
                        # Set DPI to 300
                        img.info["dpi"] = (300, 300)
                        # Convert the image mode to RGB (if not already in that mode)
                        if img.mode != "RGB":
                            img = img.convert("RGB")
                        # Save the image as .png with the same name but different extension
                        new_filename = os.path.splitext(filename)[0] + ".jpg"
                        new_file_path = os.path.join(root, new_filename)
                        img.save(new_file_path, "JPEG", dpi=(300, 300))
                        print(
                            f"Converted {filename} to {new_filename} and set DPI to 300"
                        )
                    # Remove the original .tiff file
                    os.remove(file_path)
                    print(f"Removed original file {filename}")
                except Exception as e:
                    print(f"Error processing file {filename}: {e}")


if __name__ == "__main__":
    # Specify the directory containing the images
    image_directory = "/Users/steven/Music/nocTurneMeLoDieS/img/webp"
    convert_and_upscale_images(image_directory)
