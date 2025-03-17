import streamlit as st
import numpy as np
import cv2
from PIL import Image
import streamlit_image_coordinates

st.title("RGB Color Viewer")

def rgb_to_hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

option = st.radio("Choose input method:", ("Enter RGB Values (Slider)", "Enter RGB Values (Type in)", "Upload an Image"))

if option == "Enter RGB Values (Slider)":
    r = st.slider("Red", 0, 255, 255)
    g = st.slider("Green", 0, 255, 255)
    b = st.slider("Blue", 0, 255, 255)
    
    hex_color = rgb_to_hex(r, g, b)
    
    color_block = np.zeros((300, 800, 3), dtype=np.uint8)
    color_block[:] = (b, g, r)  # OpenCV uses BGR format
    
    st.image(color_block, channels="BGR")
    st.write(f"**RGB({r}, {g}, {b})**")
    st.write(f"**Hex: {hex_color}**")

elif option == "Upload an Image":
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")  # Ensure image is always RGB
        image_cv = np.array(image)
        
        # Resize image for better display
        max_width = 700  # Set a reasonable width for display
        scale_factor = max_width / image.width
        new_height = int(image.height * scale_factor)
        resized_image = image.resize((max_width, new_height))
        
        st.markdown("Click on the image to see the corresponding RGB values:")
        # Display only the clickable image
        coords = streamlit_image_coordinates.streamlit_image_coordinates(
            resized_image,
            key="image_coords"
        )
        
        if coords is not None:
            x, y = int(coords["x"]), int(coords["y"])
            
            # Scale coordinates back to original image size
            orig_x = int(x / scale_factor)
            orig_y = int(y / scale_factor)

            # Ensure coordinates are within bounds
            orig_x = min(orig_x, image_cv.shape[1] - 1)
            orig_y = min(orig_y, image_cv.shape[0] - 1)

            # Extract the correct pixel values
            r, g, b = image_cv[orig_y, orig_x]
            hex_color = rgb_to_hex(r, g, b)
            
            st.write(f"**RGB({r}, {g}, {b})**")
            st.write(f"**Hex: {hex_color}**")
            
            color_block = np.zeros((150, 400, 3), dtype=np.uint8)
            color_block[:] = (b, g, r)  # Convert to BGR for OpenCV display
            st.image(color_block, channels="BGR")

elif option == "Enter RGB Values (Type in)":
    rgb_input = st.text_input("Enter RGB values manually (R,G,B):", "255,255,255")
    
    try:
        r, g, b = map(int, rgb_input.split(","))
        if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
            hex_color = rgb_to_hex(r, g, b)
            
            color_block = np.zeros((300, 800, 3), dtype=np.uint8)
            color_block[:] = (b, g, r)
            
            st.image(color_block, channels="BGR")
            st.write(f"**RGB({r}, {g}, {b})**")
            st.write(f"**Hex: {hex_color}**")
        else:
            st.error("RGB values must be between 0 and 255.")
    except ValueError:
        st.error("Invalid input format. Please enter values as R,G,B.")
