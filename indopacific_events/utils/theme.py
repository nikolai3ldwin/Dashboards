# utils/theme.py
"""
Theme manager for the Indo-Pacific Dashboard.
Provides functionality to switch between light and dark mode with improved contrast.
"""

import streamlit as st
import logging

# Get logger
logger = logging.getLogger("indo_pacific_dashboard")

def set_theme_config():
    """
    Set up the theme configuration for the dashboard.
    Should be called at the beginning of the app.
    """
    # Initialize theme state if not already set
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'

st.markdown("""
<style>
    [data-testid="stSidebarNav"] ul li:has(div:contains("main")),
    [data-testid="stSidebarNav"] ul li:has(div:contains("report generator")) {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

def toggle_theme():
    """
    Toggle between light and dark mode.
    """
    try:
        if st.session_state.theme == 'light':
            st.session_state.theme = 'dark'
        else:
            st.session_state.theme = 'light'
    except Exception as e:
        # Ensure theme is always set to something valid
        st.session_state.theme = 'light'

def apply_theme():
    """
    Apply the current theme using custom CSS.
    This function should only be called AFTER st.set_page_config()
    """
    try:
        # Define CSS for light and dark themes
        light_theme_css = """
        <style>
            .main {
                background-color: #FFFFFF;
                color: #31333F;
            }
            .stApp {
                background-color: #FFFFFF;
                margin: 0 auto;
            }
            .article-card {
                background-color: #F9F9F9;
                border: 1px solid #EEEEEE;
                border-radius: 5px;
                padding: 15px;
                margin-bottom: 20px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                border-left: 5px solid #4F8BF9;
            }
            .importance-high {
                border-left: 5px solid #FF4B4B;
            }
            .importance-medium {
                border-left: 5px solid #FFA64B;
            }
            .importance-low {
                border-left: 5px solid #4F8BF9;
            }
            button, .stButton>button {
                background-color: #4F8BF9;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                cursor: pointer;
                transition: background-color 0.3s;
                font-weight: 500;
            }
            button:hover, .stButton>button:hover {
                background-color: #2D68D8;
            }
            
            /* Sidebar buttons in light mode */
            .sidebar .stButton>button {
                background-color: #FFC107;
                color: #000000;
                font-weight: 600;
            }
        </style>
        """
        
        dark_theme_css = """
        <style>
            /* Dark mode styling */
            .main {
                background-color: #121212 !important;
                color: #E0E0E0 !important;
            }
            .stApp {
                background-color: #121212 !important;
                margin: 0 auto;
            }
            
            /* Article cards and containers */
            .article-card {
                background-color: #1E1E1E !important;
                border-radius: 5px;
                padding: 15px;
                margin-bottom: 20px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.3) !important;
                border-left: 5px solid #4F8BF9;
            }
            .importance-high {
                border-left: 5px solid #FF4B4B !important;
            }
            .importance-medium {
                border-left: 5px solid #FFA64B !important;
            }
            .importance-low {
                border-left: 5px solid #4F8BF9 !important;
            }
            
            /* Text and elements */
            p, h1, h2, h3, h4, h5, h6, span {
                color: #E0E0E0 !important;
            }
            
            /* Links with better contrast */
            .stMarkdown a {
                color: #6BBAFF !important;
                font-weight: 500 !important;
            }
            
            /* Buttons */
            button, .stButton>button {
                background-color: #4F8BF9 !important;
                color: white !important;
                border: none !important;
                border-radius: 5px !important;
                padding: 8px 16px !important;
                cursor: pointer !important;
                transition: background-color 0.3s !important;
                font-weight: 600 !important;
                box-shadow: 0 2px 5px rgba(0,0,0,0.3) !important;
            }
            button:hover, .stButton>button:hover {
                background-color: #2D68D8 !important;
            }
            
            /* Sidebar styling */
            div[data-testid="stSidebar"] * {
                color: #FFFFFF !important;
                opacity: 1 !important;
            }
            
            div[data-testid="stSidebar"], 
            section[data-testid="stSidebar"] {
                background-color: #1E1E1E !important;
            }
            
            /* Restore button text to black for yellow buttons in sidebar */
            div[data-testid="stSidebar"] button,
            div[data-testid="stSidebar"] .stButton > button {
                background-color: #FFC107 !important;
                color: #000000 !important;
                font-weight: 600 !important;
            }
        </style>
        """
        
        # Apply the appropriate theme
        theme = st.session_state.get('theme', 'light')
        if theme == 'light':
            st.markdown(light_theme_css, unsafe_allow_html=True)
        else:
            st.markdown(dark_theme_css, unsafe_allow_html=True)
    except Exception:
        # Apply a minimal fallback CSS to ensure readability
        fallback_css = """
        <style>
            .main { color: #000000; }
            .stApp { background-color: #FFFFFF; }
        </style>
        """
        st.markdown(fallback_css, unsafe_allow_html=True)

def create_theme_toggle():
    """
    Create a button to toggle between light and dark mode.
    """
    try:
        current_theme = st.session_state.theme
        icon = "🌙" if current_theme == 'light' else "☀️"
        label = f"{icon} Switch to {'Dark' if current_theme == 'light' else 'Light'} Mode"
        
        if st.button(label, key="theme-toggle", on_click=toggle_theme):
            st.rerun()
    except Exception:
        # Create a fallback button that hopefully works
        if st.button("Toggle Theme", key="theme-toggle-fallback"):
            # Simple toggle
            st.session_state.theme = 'dark' if st.session_state.get('theme') == 'light' else 'light'
            st.rerun()
