from PIL import Image
import os

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_2000 = 2000



def create_contact_sheet(
        source_folder,
        output_size=(
            CONSTANT_2000,
            CONSTANT_2000),
        images_per_row=2):
    # List all the image files in the source folder with the correct extension
    image_files = [
        os.path.join(source_folder, f)
        for f in os.listdir(source_folder)
        if f.endswith((".png", ".jpg", ".jpeg"))
    ]

    # Create a new blank white image to serve as the contact sheet
    contact_sheet = Image.new("RGB", output_size, "white")

    # Define the new width and height for each image
    new_width = output_size[0] // images_per_row
    # Calculate the height while maintaining aspect ratio
    new_height = int(new_width / (16 / 9))

    # Loop through the images and paste them into the contact sheet
    for i, image_file in enumerate(image_files):
        if i >= images_per_row * images_per_row:
            # Only process as many images as will fit in our grid
            break

        # Open the image
        with Image.open(image_file) as img:
            # Resize the image to fit in the contact sheet
            img = img.resize((new_width, new_height), Image.ANTIALIAS)

            # Calculate the position where the image will be placed in the
            # contact sheet
            x = (i % images_per_row) * new_width
            y = (i // images_per_row) * new_height

            # Paste the image into the contact sheet
            contact_sheet.paste(img, (x, y))

    # Save the contact sheet in the source folder with a predefined name
    contact_sheet_path = os.path.join(source_folder, "contact_sheet.jpg")
    contact_sheet.save(contact_sheet_path)
    logger.info(f"Contact sheet created and saved to {contact_sheet_path}")


# Usage
source_folder_path = input(
    "Enter the path to the folder containing the images: ")
create_contact_sheet(source_folder_path)
