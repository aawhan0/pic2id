from PIL import Image

def crop_and_resize(image, output_size=(600, 600), margin=0.25):
    """
    Crops the center of the image (head & shoulders) and resizes to passport size.

    Parameters:
        image: PIL.Image object
        output_size: tuple (width, height)
        margin: float, percentage of extra height above head for proper framing

    Returns:
        PIL.Image object resized to output_size
    """
    w, h = image.size

    # Define cropping box (simple center crop for now)
    left = 0
    right = w
    top = int(h * margin)
    bottom = h
    cropped = image.crop((left, top, right, bottom))

    # Resize to desired passport size
    resized = cropped.resize(output_size, Image.Resampling.LANCZOS)
    return resized
