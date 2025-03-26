# utils/image_handler.py
"""
Fixed utilities for handling and processing images in the Indo-Pacific Dashboard.
"""

import os
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import streamlit as st
import logging

# Get logger
logger = logging.getLogger("indo_pacific_dashboard")

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
        if not image_path_or_url:
            # No image provided, return a placeholder
            return create_placeholder_image(default_size)
            
        if image_path_or_url.startswith(('http://', 'https://')):
            # It's a URL, fetch it
            try:
                response = requests.get(image_path_or_url, stream=True, timeout=10)
                response.raise_for_status()  # Raise an exception for bad status codes
                img = Image.open(BytesIO(response.content))
            except Exception as e:
                # If URL fetch fails, create a placeholder
                logger.warning(f"Error loading image from URL {image_path_or_url}: {str(e)}")
                return create_placeholder_image(default_size)
        else:
            # It's a local path
            if os.path.exists(image_path_or_url):
                img = Image.open(image_path_or_url)
            else:
                # If file doesn't exist, create a placeholder
                logger.warning(f"Local image not found: {image_path_or_url}")
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
        logger.warning(f"Error loading image {image_path_or_url}: {str(e)}")
        return create_placeholder_image(default_size)

def create_placeholder_image(size=(300, 200)):
    """
    Create a placeholder image for the Indo-Pacific Dashboard.
    
    Parameters:
    -----------
    size : tuple
        Size (width, height) of the placeholder image
    
    Returns:
    --------
    PIL.Image
        Placeholder image
    """
    # Create a blue gradient background for the placeholder
    try:
        # Create a simple blue image
        img = Image.new('RGB', size, color=(70, 130, 180))
        draw = ImageDraw.Draw(img)
        
        # Try to add text
        try:
            # Try to load a font, fall back to default
            font = ImageFont.load_default()
            
            # Draw text
            text = "Indo-Pacific"
            # Estimate text size based on font properties
            text_width = len(text) * 7  # Rough estimate
            text_height = 12  # Rough estimate
            position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)
            
            # Draw text with shadow for better visibility
            draw.text((position[0]+2, position[1]+2), text, font=font, fill=(0, 0, 0))
            draw.text(position, text, font=font, fill=(255, 255, 255))
        except Exception as e:
            # If text rendering fails, just return the gradient
            logger.warning(f"Error adding text to placeholder: {str(e)}")
        
        return img
    except Exception as e:
        logger.error(f"Error creating placeholder image: {str(e)}")
        # Last resort - create a very basic image
        return Image.new('RGB', size, color=(70, 130, 180))

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
    
    try:
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
    except Exception as e:
        logger.error(f"Error resizing image: {str(e)}")
        return create_placeholder_image((max_width, max_height))
