import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

def convert_to_pencil_sketch(image):
    # Convert the PIL Image to an OpenCV image (numpy array)
    img = np.array(image)

    # Convert to grayscale
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Invert the grayscale image
    inverted_gray_image = 255 - gray_image

    # Blur the inverted image
    blurred_image = cv2.GaussianBlur(inverted_gray_image, (21, 21), 0)

    # Invert the blurred image
    inverted_blurred_image = 255 - blurred_image

    # Create the pencil sketch by dividing the grayscale image by the inverted blurred image
    pencil_sketch = cv2.divide(gray_image, inverted_blurred_image, scale=256.0)

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
        output_image = Image.fromarray(pencil_sketch)
        buf = io.BytesIO()
        output_image.save(buf, format='PNG')
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
