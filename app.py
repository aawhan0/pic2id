import streamlit as st
from PIL import Image
import io
from rembg import remove
from utils.passport_utils import crop_and_resize
from utils.overlay_suit import add_suit_with_face_align

st.set_page_config(page_title="Pic2ID - Passport Photo Maker", layout="centered")
st.title("📸 Pic2ID - AI Passport Photo Generator")

# Upload input image
uploaded_file = st.file_uploader("Upload your portrait image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="🧍 Uploaded Image", use_container_width=True)

    if st.button("Remove Background"):
        with st.spinner("Removing background..."):
            img_bytes = io.BytesIO()
            image.save(img_bytes, format="PNG")
            result = remove(img_bytes.getvalue())
            bg_removed_img = Image.open(io.BytesIO(result)).convert("RGBA")

            st.image(bg_removed_img, caption="🪄 Background Removed", use_container_width=True)

            # Store for further steps (like adding suit)
            st.session_state['bg_removed'] = bg_removed_img

    if "bg_removed" in st.session_state and st.button("Add Suit & Tie"):
        with st.spinner("Adding Suit..."):
            final_img = add_suit_with_face_align(st.session_state["bg_removed"], suit_path="assets/suit_overlay.png")
            st.image(final_img, caption="Passport Photo Ready!", use_container_width=True)
            st.session_state["final_img"] = final_img

    if "final_img" in st.session_state:
        buf = io.BytesIO()
        st.session_state["final_img"].save(buf, format="PNG")
        st.download_button(
            label="Download Passport Photo",
            data=buf.getvalue(),
            file_name="passport_photo.png",
            mime="image/png"
        )

    if "final_img" in st.session_state and st.button("Format as Passport Photo"):
        with st.spinner("Cropping and resizing..."):
            passport_img = crop_and_resize(st.session_state['final_img'], (600, 600))
            st.image(passport_img, caption="🪪 Passport-Ready Photo", use_container_width=True)
            st.session_state['passport_img'] = passport_img

    if 'passport_img' in st.session_state:
        buf = io.BytesIO()
        st.session_state['passport_img'].save(buf, format="PNG")
        st.download_button(
            label="⬇️ Download Passport Photo",
            data=buf.getvalue(),
            file_name="passport_photo.png",
            mime="image/png"
        )

else:
    st.info("Please upload an image to begin.")
