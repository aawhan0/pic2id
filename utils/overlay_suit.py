from PIL import Image

def add_suit(bg_removed_img, suit_path="suit_overlay.png"):
    suit = Image.open(suit_path).convert("RGBA")

    suit_width = bg_removed_img.width
    suit_ratio = suit_width/suit.width
    suit_height = int(suit.height * suit_ratio)
    suit = suit.resize((suit_width, suit_height), Image.Resampling.LANCZOS)

    position = (0, bg_removed_img.height - suit.height)
    combined = bg_removed_img.copy()
    combined.alpha_composite(suit, position)

    return combined