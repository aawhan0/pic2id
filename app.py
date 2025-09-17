import streamlit as st
from PIL import Image
import io
from rembg import remove

st.set_page_config(page_title="Pic2ID - Passport Photo Maker", layout="centered")
st.title("📸 Pic2ID - AI Passport Photo Generator")

# Upload input image
uploaded_file = st.file_uploader("Upload your portrait image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="🧍 Uploaded Image", use_container_width=True)

    if st.button("🧼 Remove Background"):
        with st.spinner("Removing background..."):
            img_bytes = io.BytesIO()
            image.save(img_bytes, format="PNG")
            result = remove(img_bytes.getvalue())
            bg_removed_img = Image.open(io.BytesIO(result)).convert("RGBA")

            st.image(bg_removed_img, caption="🪄 Background Removed", use_container_width=True)

            # Store for further steps (like adding suit)
            st.session_state['bg_removed'] = bg_removed_img
else:
    st.info("Please upload an image to begin.")
