from PIL import Image

# Constants
CONSTANT_1024 = 1024
CONSTANT_1536 = 1536


# Function to resize and add a black border to an image
def resize_and_add_border(image, target_size, border_size):
    """resize_and_add_border function."""

    resized_image = Image.new("RGB", target_size, "black")
    resized_image.paste(
        image,
        ((target_size[0] - image.width) // 2, (target_size[1] - image.height) // 2),
    )
    return resized_image

    """create_strip function."""


def create_strip(images):
    # Desired grid size
    columns, rows = 2, 3

    # Calculate the size of the output image
    output_width = (
        columns * images[0].width + (columns - 1) * 10
    )  # 10 is the black border width
    output_height = (
        rows * images[0].height + (rows - 1) * 10
    )  # 10 is the black border width

    # Create a new image with the calculated size
    result_image = Image.new("RGB", (output_width, output_height), "white")

    # Combine images into a grid with black borders
    for i, img in enumerate(images):
        x = (i % columns) * (img.width + 10)  # 10 is the black border width
        y = (i // columns) * (img.height + 10)  # 10 is the black border width

        resized_img = resize_and_add_border(
            img, (images[0].width, images[0].height), 10
        )
        result_image.paste(resized_img, (x, y))

    return result_image.resize((CONSTANT_1024, CONSTANT_1536))
