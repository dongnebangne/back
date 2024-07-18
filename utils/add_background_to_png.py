import base64
from io import BytesIO
from PIL import Image
from .data_uri_to_buffer import data_uri_to_buffer

def add_background_to_png(data_url):
    # Convert data URL to buffer
    buffer = data_uri_to_buffer(data_url)

    # Open the image from the buffer
    with BytesIO(buffer) as buf:
        image = Image.open(buf)

        # Create a new image with a white background
        new_image = Image.new("RGBA", image.size, "WHITE")
        new_image.paste(image, (0, 0), image)

        # Save the new image to a buffer
        with BytesIO() as output:
            new_image.save(output, format="PNG")
            new_buffer = output.getvalue()

    # Convert buffer to data URL
    new_data_url = "data:image/png;base64," + base64.b64encode(new_buffer).decode("ascii")

    return new_data_url