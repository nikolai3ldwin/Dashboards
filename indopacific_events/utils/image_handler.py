# image_handler.py
"""
Utilities for handling and processing images in the Indo-Pacific Dashboard.
"""

import os
import requests
from io import BytesIO
from PIL import Image
import streamlit as st

# Cache images to avoid reloading
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_image(image_path_or_url, default_size=(300, 200)):
    """
    Load an image from a URL or local path with caching.
    
    Parameters:
    -----------
    image_path_or_url : str
        URL or local file path to the image
    default_size : tuple
        Default size (width, height) to resize image if needed
    
    Returns:
    --------
    PIL.Image
        Loaded and processed image
    """
    try:
        if image_path_or_url.startswith(('http://', 'https://')):
            # It's a URL, fetch it
            response = requests.get(image_path_or_url, stream=True, timeout=10)
            response.raise_for_status()  # Raise an exception for bad status codes
            img = Image.open(BytesIO(response.content))
        else:
            # It's a local path
            if os.path.exists(image_path_or_url):
                img = Image.open(image_path_or_url)
            else:
                # If file doesn't exist, return a placeholder
                return create_placeholder_image(default_size)
        
        # Convert to RGB if image is in RGBA mode
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        
        # Resize if the image is too large
        if max(img.size) > 1000:
            img.thumbnail((1000, 1000), Image.LANCZOS)
        
        return img
    
    except Exception as e:
        # If anything fails, return a placeholder image
        print(f"Error loading image {image_path_or_url}: {str(e)}")
        return create_placeholder_image(default_size)

def create_placeholder_image(size=(300, 200)):
    """
    Create a simple placeholder image.
    
    Parameters:
    -----------
    size : tuple
        Size (width, height) of the placeholder image
    
    Returns:
    --------
    PIL.Image
        Placeholder image
    """
    # Create a gray placeholder image
    img = Image.new('RGB', size, color=(240, 240, 240))
    return img

def resize_image(img, max_width=800, max_height=600):
    """
    Resize an image while maintaining aspect ratio.
    
    Parameters:
    -----------
    img : PIL.Image
        Image to resize
    max_width : int
        Maximum width
    max_height : int
        Maximum height
    
    Returns:
    --------
    PIL.Image
        Resized image
    """
    if not img:
        return create_placeholder_image((max_width, max_height))
    
    # Calculate the aspect ratio
    width, height = img.size
    aspect_ratio = width / height
    
    # Determine new dimensions
    if width > max_width:
        width = max_width
        height = int(width / aspect_ratio)
    
    if height > max_height:
        height = max_height
        width = int(height * aspect_ratio)
    
    # Resize the image
    return img.resize((width, height), Image.LANCZOS)

def apply_image_effects(img, effect='none'):
    """
    Apply visual effects to an image.
    
    Parameters:
    -----------
    img : PIL.Image
        Image to process
    effect : str
        Effect to apply ('none', 'grayscale', 'sepia', etc.)
    
    Returns:
    --------
    PIL.Image
        Processed image
    """
    if not img:
        return create_placeholder_image()
    
    # Apply selected effect
    if effect == 'grayscale':
        return img.convert('L').convert('RGB')
    elif effect == 'sepia':
        # Simple sepia effect
        grayscale = img.convert('L')
        sepia = Image.merge('RGB', [
            grayscale,
            grayscale.point(lambda x: min(255, int(x * 0.95))),
            grayscale.point(lambda x: min(255, int(x * 0.7)))
        ])
        return sepia
    else:
        # No effect or unknown effect
        return img
