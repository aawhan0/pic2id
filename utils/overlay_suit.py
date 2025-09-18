import os
from rembg import remove
from PIL import Image
import numpy as np
import cv2
import io

def detect_face_bbox(pil_img):
    cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    return faces[0] if len(faces) > 0 else None

def add_suit_with_face_align(bg_removed_img, suit_path="output_img/suit_no_bg.png"):
    bg_removed_img = bg_removed_img.convert("RGBA")

    suit_no_bg = Image.open(suit_path).convert("RGBA")
    suit_width = bg_removed_img.width
    suit_scale = suit_width / suit_no_bg.width
    suit_height = int(suit_no_bg.height * suit_scale)
    suit_resized = suit_no_bg.resize((suit_width, suit_height), Image.Resampling.LANCZOS)

    # Position suit just below bottom of neck (image bottom)
    combined_height = bg_removed_img.height + suit_resized.height
    final_img = Image.new("RGBA", (suit_width, combined_height), (0, 0, 0, 255))

    final_img.paste(bg_removed_img, (0, 0), bg_removed_img)
    final_img.alpha_composite(suit_resized, (0, bg_removed_img.height))

    return final_img

def add_suit(bg_removed_img, suit_path="suit_overlay.png"):
    bg_removed_img = bg_removed_img.convert("RGBA")  # Ensure RGBA
    suit = Image.open(suit_path).convert("RGBA")
    suit_width = bg_removed_img.width
    suit_ratio = suit_width / suit.width
    suit_height = int(suit.height * suit_ratio)
    suit = suit.resize((suit_width, suit_height), Image.Resampling.LANCZOS)
    position = (0, bg_removed_img.height - suit.height)
    combined = bg_removed_img.copy()
    combined.alpha_composite(suit, position)
    return combined

def merge_head_and_suit_face_behind(cropped_img, suit_path, overlap_px=40):
    cropped_img = cropped_img.convert("RGBA")
    suit_img = Image.open(suit_path).convert("RGBA")

    suit_width = cropped_img.width
    suit_scale = suit_width / suit_img.width
    suit_height = int(suit_img.height * suit_scale)
    suit_resized = suit_img.resize((suit_width, suit_height), Image.Resampling.LANCZOS)

    final_height = cropped_img.height + suit_resized.height - overlap_px
    final_img = Image.new("RGBA", (suit_width, final_height), (0, 0, 0, 255))

    # Paste cropped face first (background)
    final_img.paste(cropped_img, (0, 0), cropped_img)
    # Paste suit overlay on top (foreground) with overlap position
    final_img.alpha_composite(suit_resized, (0, cropped_img.height - overlap_px))
    print(f"Using suit_offset: {overlap_px}")
    print(f"Cropped image size: {cropped_img.size}")
    print(f"Suit resized size: {suit_resized.size}")
    print(f"Overlap pixels: {overlap_px}")
    print(f"Suit paste position: {(0, cropped_img.height - overlap_px)}")



    return final_img
