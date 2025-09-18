import os
from rembg import remove
from PIL import Image
import io

def remove_background_from_suit_image(input_path, output_path):
    """
    Removes the background from the suit image using rembg,
    saves the result as a transparent PNG.

    Parameters:
      input_path (str): Path to the original suit image file.
      output_path (str): Path where the background removed image will be saved.
    """
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Read input image bytes
    with open(input_path, 'rb') as f:
        input_bytes = f.read()

    # Remove background using rembg
    output_bytes = remove(input_bytes)

    # Load result as PIL image with alpha channel (RGBA)
    img_no_bg = Image.open(io.BytesIO(output_bytes)).convert("RGBA")

    # Save the processed image
    img_no_bg.save(output_path)
    print(f"Saved suit background removed image to {output_path}")
