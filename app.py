import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Konfigurasi Halaman
st.set_page_config(page_title="Color Detective", layout="wide")
st.title("🎨 Color Detective (Online Version)")
st.write("Upload a photo of a colored object, then adjust the sliders on the left to detect it!")

# --- Sidebar for Sliders ---
st.sidebar.header("Adjust HSV Sliders")
h_min = st.sidebar.slider("H Min (Color Type)", 0, 180, 100)
h_max = st.sidebar.slider("H Max (Color Type)", 0, 180, 130)
s_min = st.sidebar.slider("S Min (Saturation)", 0, 255, 50)
v_min = st.sidebar.slider("V Min (Brightness)", 0, 255, 50)

# --- Image Upload Area ---
uploaded_file = st.file_uploader("Choose an image (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read image
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    
    # Convert RGB (PIL) to BGR (OpenCV)
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    
    # Color detection process
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, 255, 255])
    
    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(img_bgr, img_bgr, mask=mask)
    
    # Convert back to RGB for web display
    result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    
    # Display Images Side by Side
    col1, col2 = st.columns(2)
    with col1:
        st.image(image, caption="Original Image", use_column_width=True)
    with col2:
        st.image(result_rgb, caption="Detection Result", use_column_width=True)
        
    st.success("Adjust the sliders on the left to change the detection result!")
else:
    st.info("Please upload an image first.")
