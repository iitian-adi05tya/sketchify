import streamlit as st
from PIL import Image, ImageFilter, ImageOps
import numpy as np
import io

def convert_to_pencil_sketch(image):
    # Convert the image to grayscale
    gray_image = image.convert("L")

    # Invert the grayscale image
    inverted_image = ImageOps.invert(gray_image)

    # Apply Gaussian blur
    blurred_image = inverted_image.filter(ImageFilter.GaussianBlur(21))

    # Create the pencil sketch by dividing the grayscale image by the inverted blurred image
    pencil_sketch = Image.blend(gray_image, blurred_image, alpha=0.5)
    
    return pencil_sketch

# Streamlit app
def main():
    st.title("Pencil Sketch Converter")

    # Upload image
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Read the uploaded image
        image = Image.open(uploaded_file)

        # Convert to pencil sketch
        pencil_sketch = convert_to_pencil_sketch(image)

        # Display original and pencil sketch
        st.image(image, caption='Original Image', use_column_width=True)
        st.image(pencil_sketch, caption='Pencil Sketch', use_column_width=True)

        # Save the pencil sketch to a BytesIO object
        buf = io.BytesIO()
        pencil_sketch.save(buf, format='PNG')
        byte_im = buf.getvalue()

        # Provide a download button
        st.download_button(
            label="Download Sketch",
            data=byte_im,
            file_name="pencil_sketch.png",
            mime="image/png"
        )

if __name__ == "__main__":
    main()



