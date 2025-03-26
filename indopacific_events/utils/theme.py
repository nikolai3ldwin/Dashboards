# utils/theme.py
"""
Fixed theme manager for the Indo-Pacific Dashboard.
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
        logger.info("Initialized theme state to 'light'")

def toggle_theme():
    """
    Toggle between light and dark mode.
    """
    try:
        if st.session_state.theme == 'light':
            st.session_state.theme = 'dark'
            logger.info("Theme changed to dark mode")
        else:
            st.session_state.theme = 'light'
            logger.info("Theme changed to light mode")
    except Exception as e:
        logger.error(f"Error toggling theme: {str(e)}")
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
            }
            .css-1v3fvcr {
                background-color: #FFFFFF;
            }
            .css-18e3th9 {
                background-color: #FFFFFF;
            }
            .css-1d391kg {
                background-color: #FFFFFF;
            }
            .article-card {
                background-color: #F9F9F9;
                border: 1px solid #EEEEEE;
            }
            .importance-indicator {
                color: #FFD700;
            }
            .css-hxt7ib {
                padding-top: 1rem;
            }
            .stMarkdown a {
                color: #0366d6;
            }
            /* Improved button styling */
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
            /* Sidebar toggle indicator */
            [data-testid="collapsedControl"] {
                background-color: #4F8BF9;
                color: white;
                border-radius: 50%;
                width: 36px;
                height: 36px;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            }
        </style>
        """
        
        dark_theme_css = """
        <style>
            .main {
                background-color: #1E1E1E;
                color: #FFFFFF;  /* Improved text contrast */
            }
            .stApp {
                background-color: #1E1E1E;
            }
            .css-1v3fvcr {
                background-color: #1E1E1E;
            }
            .css-18e3th9 {
                background-color: #1E1E1E;
            }
            .css-1d391kg {
                background-color: #1E1E1E;
            }
            .article-card {
                background-color: #2D2D2D;
                border: 1px solid #3D3D3D;
            }
            .importance-indicator {
                color: #FFC107;
            }
            .css-hxt7ib {
                padding-top: 1rem;
            }
            /* Higher contrast for links */
            .stMarkdown a {
                color: #6BBAFF;
                font-weight: 500;
            }
            .stTabs [data-baseweb="tab-list"] {
                background-color: #2D2D2D;
            }
            .stTabs [data-baseweb="tab"] {
                color: #FFFFFF;
            }
            .stTabs [aria-selected="true"] {
                background-color: #3D3D3D;
            }
            /* Improved button styling for dark mode with higher contrast */
            button, .stButton>button {
                background-color: #FFC107;
                color: #000000;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                cursor: pointer;
                transition: background-color 0.3s;
                font-weight: 600;
                box-shadow: 0 2px 5px rgba(0,0,0,0.3);
            }
            button:hover, .stButton>button:hover {
                background-color: #FFCA28;
            }
            /* Sidebar toggle indicator */
            [data-testid="collapsedControl"] {
                background-color: #FFC107;
                color: #000000;
                border-radius: 50%;
                width: 36px;
                height: 36px;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 2px 5px rgba(0,0,0,0.3);
            }
            /* Better contrast for general text */
            p, h1, h2, h3, h4, h5, h6, span, div {
                color: #FFFFFF;
            }
            /* Improved metrics */
            [data-testid="stMetricValue"] {
                color: #FFFFFF;
                font-weight: bold;
            }
            /* Form elements with better contrast */
            .stTextInput>div>div>input, .stSelectbox>div>div>div {
                background-color: #2D2D2D;
                color: #FFFFFF;
                border: 1px solid #4D4D4D;
            }
            /* Checkbox and radio buttons with better contrast */
            .stCheckbox>div>div>div, .stRadio>div>div>div {
                color: #FFFFFF;
            }
            /* Better contrast for expanders */
            .streamlit-expanderHeader {
                color: #FFFFFF;
                background-color: #2D2D2D;
            }
            /* Improved contrast for dataframes and tables */
            .stDataFrame {
                color: #FFFFFF;
            }
            .stDataFrame [data-testid="stTable"] {
                color: #FFFFFF;
            }
            /* Fix pagination text */
            .pagination {
                color: #FFFFFF !important;
                font-weight: 500 !important;
            }
        </style>
        """
        
        # Apply the appropriate theme
        theme = st.session_state.get('theme', 'light')
        if theme == 'light':
            st.markdown(light_theme_css, unsafe_allow_html=True)
        else:
            st.markdown(dark_theme_css, unsafe_allow_html=True)
    except Exception as e:
        logger.error(f"Error applying theme: {str(e)}")
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
            st.rerun()  # Use rerun instead of experimental_rerun
    except Exception as e:
        logger.error(f"Error creating theme toggle: {str(e)}")
        # Create a fallback button that hopefully works
        if st.button("Toggle Theme", key="theme-toggle-fallback"):
            # Simple toggle
            st.session_state.theme = 'dark' if st.session_state.get('theme') == 'light' else 'light'
            st.rerun()
