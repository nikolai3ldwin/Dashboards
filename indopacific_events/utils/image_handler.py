# image_handler.py
"""
Enhanced utilities for handling and processing images in the Indo-Pacific Dashboard.
"""

import os
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import streamlit as st
import random

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
                print(f"Error loading image from URL {image_path_or_url}: {str(e)}")
                return create_placeholder_image(default_size)
        else:
            # It's a local path
            if os.path.exists(image_path_or_url):
                img = Image.open(image_path_or_url)
            else:
                # If file doesn't exist, create a placeholder
                print(f"Local image not found: {image_path_or_url}")
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
    # Create a gradient background for the placeholder
    colors = [
        # Blue ocean-themed gradients
        ((70, 130, 180), (100, 149, 237)),  # Steel Blue to Cornflower Blue
        ((0, 119, 182), (0, 180, 216)),     # Blue to Light Blue
        ((25, 25, 112), (65, 105, 225)),    # Midnight Blue to Royal Blue
        ((30, 144, 255), (135, 206, 250)),  # Dodger Blue to Light Sky Blue
        
        # Asia Pacific inspired colors
        ((255, 105, 97), (249, 131, 166)),  # Coral to Pink
        ((34, 139, 34), (124, 252, 0)),     # Forest Green to Lawn Green
        ((255, 165, 0), (255, 215, 0)),     # Orange to Gold
        ((139, 69, 19), (210, 105, 30))     # Saddle Brown to Chocolate
    ]
    
    # Select a random color pair
    color1, color2 = random.choice(colors)
    
    # Create a gradient image
    img = Image.new('RGB', size, color=color1)
    draw = ImageDraw.Draw(img)
    
    # Draw a simple gradient by using polygons
    width, height = size
    for i in range(height):
        # Calculate color for this line
        ratio = i / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        
        # Draw a line with this color
        draw.line([(0, i), (width, i)], fill=(r, g, b))
    
    # Add text to the image
    try:
        # Try to load a font, fall back to default
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        # Draw text
        text = "Indo-Pacific"
        text_width, text_height = draw.textsize(text, font=font) if hasattr(draw, 'textsize') else (100, 20)
        position = ((width - text_width) // 2, (height - text_height) // 2)
        
        # Draw text with shadow for better visibility
        draw.text((position[0]+2, position[1]+2), text, font=font, fill=(0, 0, 0, 128))
        draw.text(position, text, font=font, fill=(255, 255, 255))
    except Exception as e:
        # If text rendering fails, just return the gradient
        print(f"Error adding text to placeholder: {str(e)}")
    
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
