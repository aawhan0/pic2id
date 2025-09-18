import os
import cv2
import mediapipe as mp
import numpy as np
from PIL import Image
import streamlit as st
import io

mp_face_mesh = mp.solutions.face_mesh


def crop_above_neck(pil_img):
    cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    if len(faces) == 0:
        return pil_img
    x, y, w, h = max(faces, key=lambda rect: rect[2] * rect[3])
    neck_bottom = y + int(1.4 * h)       # crop slightly below chin; tweak if needed
    neck_bottom = min(neck_bottom, cv_img.shape[0])
    cropped_cv_img = cv_img[0:neck_bottom, :]
    cropped_pil_img = Image.fromarray(cv2.cvtColor(cropped_cv_img, cv2.COLOR_BGR2RGB))
    return cropped_pil_img


def get_neck_landmarks(pil_img):
    img = np.array(pil_img.convert("RGB"))
    with mp_face_mesh.FaceMesh(static_image_mode=True) as face_mesh:
        results = face_mesh.process(img)
        if not results.multi_face_landmarks:
            return None
        face_landmarks = results.multi_face_landmarks[0]
        h, w, _ = img.shape
        chin_idx = 152
        jaw_left_idx = 234
        jaw_right_idx = 454
        chin = face_landmarks.landmark[chin_idx]
        jaw_left = face_landmarks.landmark[jaw_left_idx]
        jaw_right = face_landmarks.landmark[jaw_right_idx]
        chin_point = (int(chin.x * w), int(chin.y * h))
        jaw_left_point = (int(jaw_left.x * w), int(jaw_left.y * h))
        jaw_right_point = (int(jaw_right.x * w), int(jaw_right.y * h))
        neck_y = chin_point[1]
        neck_width = jaw_right_point[0] - jaw_left_point[0]
        return neck_y, neck_width


def merge_head_and_suit_scaled(cropped_img, suit_path, overlap_px=120):
    cropped_img = cropped_img.convert("RGBA")
    suit_img = Image.open(suit_path).convert("RGBA")
    neck_detect = get_neck_landmarks(cropped_img)
    if neck_detect is None:
        suit_width = cropped_img.width
        suit_scale = suit_width / suit_img.width
        suit_height = int(suit_img.height * suit_scale)
        suit_resized = suit_img.resize((suit_width, suit_height), Image.Resampling.LANCZOS)
        neck_y = cropped_img.height
        neck_width = suit_width
    else:
        neck_y, neck_width = neck_detect
        suit_scale = neck_width / suit_img.width
        suit_height = int(suit_img.height * suit_scale)
        suit_resized = suit_img.resize((neck_width, suit_height), Image.Resampling.LANCZOS)
    target_head_to_suit_ratio = 0.6
    if cropped_img.width < target_head_to_suit_ratio * suit_resized.width:
        scale_factor = (target_head_to_suit_ratio * suit_resized.width) / cropped_img.width
        new_width = int(cropped_img.width * scale_factor)
        new_height = int(cropped_img.height * scale_factor)
        cropped_img = cropped_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    head_height = cropped_img.height
    paste_y = head_height - overlap_px
    canvas_height = max(head_height, paste_y + suit_resized.height)
    final_img = Image.new("RGBA", (suit_resized.width, canvas_height), (0, 0, 0, 255))
    final_img.paste(cropped_img, (0, 0), cropped_img)
    final_img.alpha_composite(suit_resized, (0, paste_y))
    os.makedirs("output_img", exist_ok=True)
    output_path = os.path.join("output_img", "merged_output.png")
    final_img.save(output_path)
    print(f"Saved merged image at {output_path}")
    return final_img


# Streamlit app main
st.title("Suit and Head Merger")

uploaded_file = st.file_uploader("Upload your photo", type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    image_bytes = uploaded_file.read()
    pil_img = Image.open(io.BytesIO(image_bytes))

    cropped_head = crop_above_neck(pil_img)
    merged_img = merge_head_and_suit_scaled(cropped_head, "assets/suit_overlay.png", overlap_px=120)

    st.image(merged_img)

    # Provide download button
    from io import BytesIO
    buf = BytesIO()
    merged_img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    st.download_button(label="Download Merged Image", data=byte_im, file_name="merged_output.png", mime="image/png")
