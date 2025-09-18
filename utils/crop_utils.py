import cv2
import numpy as np
from PIL import Image

def crop_above_neck(pil_img):
    cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) == 0:
        return pil_img

    x, y, w, h = max(faces, key=lambda rect: rect[2] * rect[3])
    neck_bottom = y + int(1.1 * h)      # 10% below chin, tweak as needed
    neck_bottom = min(neck_bottom, cv_img.shape[0])

    # Crop from top to just below neck, keeping full width
    cropped_cv_img = cv_img[0:neck_bottom, :]
    from PIL import Image
    cropped_pil_img = Image.fromarray(cv2.cvtColor(cropped_cv_img, cv2.COLOR_BGR2RGB))
    return cropped_pil_img