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
    bbox = detect_face_bbox(bg_removed_img)
    if bbox is None:
        return add_suit(bg_removed_img, suit_path)

    # Load preprocessed suit image with transparent background
    suit_no_bg = Image.open(suit_path).convert("RGBA")

    x, y, w, h = bbox
    suit_width = bg_removed_img.width
    suit_height = int(1.5 * h)
    suit_resized = suit_no_bg.resize((suit_width, suit_height), Image.Resampling.LANCZOS)

    # Position suit collar just below the face bounding box (approx chin)
    position = (0, y + h)
    
    combined = bg_removed_img.copy()
    combined.alpha_composite(suit_resized, position)

    return combined

def add_suit(bg_removed_img, suit_path="suit_overlay.png"):
    suit = Image.open(suit_path).convert("RGBA")
    suit_width = bg_removed_img.width
    suit_ratio = suit_width / suit.width
    suit_height = int(suit.height * suit_ratio)
    suit = suit.resize((suit_width, suit_height), Image.Resampling.LANCZOS)
    position = (0, bg_removed_img.height - suit.height)
    combined = bg_removed_img.copy()
    combined.alpha_composite(suit, position)
    return combined
