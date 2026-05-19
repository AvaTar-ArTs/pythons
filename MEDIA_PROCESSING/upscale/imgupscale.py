"""
Summary of imgupscale.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

import os

from PIL import Image, UnidentifiedImageError


# Function to convert and upscale PNG and JPEG images by 200% with 300 DPI
def convert_and_upscale_images(source_directory, destination_directory, max_size_mb=8):
    # Create the destination directory if it doesn't exist
    os.makedirs(destination_directory, exist_ok=True)

    for filename in os.listdir(source_directory):
        if filename.lower().endswith((".png", ".jpeg", ".jpg")):
            source_file = os.path.join(source_directory, filename)
            filename_no_ext = os.path.splitext(filename)[0]
            ext = filename.split(".")[-1].lower()
            destination_file = os.path.join(
                destination_directory, f"{filename_no_ext}.{ext}"
            )

            try:
                # Convert and upscale PNG or JPEG
                with Image.open(source_file) as im:
                    width, height = im.size
                    upscale_width = width * 2
                    upscale_height = height * 2
                    im_resized = im.resize((upscale_width, upscale_height))

                    # Save the image and ensure it doesn't exceed the max size
                    im_resized.save(destination_file, format=im.format, dpi=(300, 300))

                    # Check file size and reduce quality if needed
                    file_size = os.path.getsize(destination_file) / (
                        1024 * 1024
                    )  # size in MB
                    if file_size > max_size_mb:
                        for quality in range(95, 10, -5):  # Reduce quality in steps
                            im_resized.save(
                                destination_file,
                                format=im.format,
                                dpi=(300, 300),
                                quality=quality,
                            )
                            file_size = os.path.getsize(destination_file) / (
                                1024 * 1024
                            )
                            if file_size <= max_size_mb:
                                break

                print(
                    f"Converted, upscaled, and saved: {filename} -> {filename_no_ext}.{ext}"
                )
            except (UnidentifiedImageError, OSError) as e:
                print(f"Error processing {filename}: {e}")


# Main function
def main():
    # Prompt for the source directory containing PNG and JPEG images
    source_directory = input(
        "Enter the path to the source directory containing PNG and JPEG images: "
    )

    # Check if the source directory exists
    if not os.path.isdir(source_directory):
        print("Source directory does not exist.")
        return

    # Prompt for the destination directory
    destination_directory = input("Enter the path for the destination directory: ")

    convert_and_upscale_images(source_directory, destination_directory)


# Run the main function
if __name__ == "__main__":
    main()
