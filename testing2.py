import cv2
import streamlit as st
import numpy as np
import os

st.title("Crack Length and Margin Calculator")

col1, col2 = st.columns(2)

def show_image(original_image):
    # Get the dimensions of the original image
    height, width = original_image.shape[:2]

    # Define the desired window size
    window_width = 800
    window_height = 600

    # Calculate the aspect ratio
    aspect_ratio = width / height

    # Calculate the new dimensions to fit the window while maintaining the aspect ratio
    if aspect_ratio > 1:
        new_width = window_width
        new_height = int(window_width / aspect_ratio)
    else:
        new_height = window_height
        new_width = int(window_height * aspect_ratio)

    # Resize the original image to fit the window
    resized_image = cv2.resize(original_image, (new_width, new_height))

    with col2:
        st.image(resized_image, caption='Cracks of the Gem', use_container_width=True)

    return


def calculate_crack_length_and_margin(original_image, scale_length_pixels, scale_length_mm, canny_low_threshold, canny_high_threshold, margin_size):
    # Convert the resized image to grayscale
    gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

    with col1:
        st.image(original_image, caption='Original Image', use_container_width=True)

    # Apply Canny edge detection
    edges = cv2.Canny(gray, canny_low_threshold, canny_high_threshold)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize variables to store the length of the longest contour
    max_length = 0
    max_contour = None

    # Iterate through the contours
    for contour in contours:
        # Calculate the length of the contour in pixels
        length_pixels = cv2.arcLength(contour, closed=True)

        # Convert the length from pixels to millimeters
        length_mm = (length_pixels / scale_length_pixels) * scale_length_mm

        # Update the maximum length and corresponding contour
        if length_mm > max_length:
            max_length = length_mm
            max_contour = contour

        # Draw the contour with red color
        cv2.drawContours(original_image, [contour], -1, (0, 0, 255), 2)

        # Draw margin around the contour
        # margin = draw_margin(original_image, contour, margin_size)

    # Display the image with the detected cracks and margins
    show_image(original_image)

    # Return the length of the longest crack in millimeters
    return max_length




# Main Streamlit app
def main():
    # Get list of files in the current directory
    current_directory = os.getcwd()
    files_in_directory = os.listdir(current_directory)

    # Check if there are any image files in the directory
    image_files = [f for f in files_in_directory if f.endswith(('.jpg', '.jpeg', '.png'))]

    if len(image_files) == 0:
        st.write("No image files found in the directory.")
    else:
        # Select the first image file found in the directory
        image_path = os.path.join(current_directory, image_files[0])

        # Convert the file to an OpenCV image
        original_image = cv2.imread(image_path)

        # Scale length in pixels and millimeters (you need to measure this from your image)
        scale_length_pixels = 232
        scale_length_mm = 25

        # Add sliders for Canny thresholds and margin size
        canny_low_threshold = st.slider('Canny Low Threshold', 0, 250, 60)
        canny_high_threshold = st.slider('Canny High Threshold', 250, 500, 480)
        margin_size = st.slider('Margin Size', 1, 50, 10)

        # Calculate crack length and draw margins around cracks
        crack_length_mm = calculate_crack_length_and_margin(original_image, scale_length_pixels, scale_length_mm, canny_low_threshold, canny_high_threshold, margin_size)
        st.write("Length of the longest crack (mm):", crack_length_mm)

# Run the Streamlit app
if __name__ == "__main__":
    main()
