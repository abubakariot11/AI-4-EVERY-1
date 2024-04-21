import streamlit as st
from PIL import Image
from removebg import RemoveBg

# Set up RemoveBg
removebg = RemoveBg("hSWrXGtstNLV3Sog5rFGfzTv", "error.log")  # Insert your Remove.bg API key here

def main():
    st.title("Background Remover App")
    st.write(
        "This is a simple web app to remove the background from images using Remove.bg."
    )

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Original Image", use_column_width=True)

        if st.button("Remove Background"):
            with st.spinner("Removing background..."):
                try:
                    removebg.remove_background_from_img_file(uploaded_file.name)
                    processed_img = Image.open("no_bg.png")
                    st.image(processed_img, caption="Background Removed", use_column_width=True)
                except Exception as e:
                    st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
