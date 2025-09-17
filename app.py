import streamlit as st
from PIL import Image
import cv2
import numpy as np
from rembg import remove
import io

st.set_page_config(page_title="Pic2ID", layout= "centered")

st.title("Pic2ID - Image to Identification")

uploaded_file = st.file_uploader("Upload an Image", type=["jpg", 'png', 'jpeg'])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Image", use_column_width=True)

    if st.button("Remove Background"):
        with st.spinner("Processing.."):
            input_image_bytes= io.BytesIO()
            image.save(input_image_bytes, format="PNG")
            result = remove(input_image_bytes.getvalue())
            result_image = Image.open(io.BytesIO(result))
            st.image(result_image, caption="Background Removed", use_column_width=True)
            st.success("Done!")

    