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
                /* Remove max-width to flex to page */
                /* max-width: 1200px; */
                margin: 0 auto;
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
            .article-title {
                font-size: 1.2rem;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .article-meta {
                font-size: 0.8rem;
                color: #666;
                margin-bottom: 10px;
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
            .tag-container {
                display: flex;
                flex-wrap: wrap;
                margin-top: 10px;
            }
            .tag {
                background-color: #E6E6E6;
                padding: 2px 8px;
                border-radius: 10px;
                font-size: 0.75rem;
                margin-right: 5px;
                margin-bottom: 5px;
            }
            /* Button styling */
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
            
            /* Make sidebar buttons consistent in light mode */
            .sidebar .stButton>button {
                background-color: #FFC107;
                color: #000000;
                font-weight: 600;
            }

            /* Target "Select All" and "Clear All" buttons */
            .sidebar [data-testid="baseButton-secondary"] {
                background-color: #FFC107;
                color: #000000;
                font-weight: 600;
            }
            
            /* Sidebar styling */
            .sidebar .sidebar-content {
                background-color: #F5F5F5;
            }
            .sidebar-content p, .sidebar-content h1, .sidebar-content h2, 
            .sidebar-content h3, .sidebar-content h4, .sidebar-content h5, 
            .sidebar-content h6, .sidebar-content span, .sidebar-content label {
                color: #31333F !important;
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
            
            /* Fix dashboard navigation buttons specifically */
            .sidebar [data-testid="element-container"] button {
                background-color: #FFC107;
                color: #000000;
                font-weight: 600;
            }
        </style>
        """
        
        dark_theme_css = """
        <style>
            /* Dark mode styling - EXPANDED */
            .main {
                background-color: #121212 !important;
                color: #E0E0E0 !important;
            }
            .stApp {
                background-color: #121212 !important;
                /* Remove max-width to flex to page */
                /* max-width: 1200px; */
                margin: 0 auto;
            }
            .css-1v3fvcr {
                background-color: #121212 !important;
            }
            .css-18e3th9 {
                background-color: #121212 !important;
            }
            .css-1d391kg {
                background-color: #121212 !important;
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
            .article-title {
                font-size: 1.2rem;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .article-meta {
                font-size: 0.8rem;
                color: #BFBFBF !important;
                margin-bottom: 10px;
            }
            
            /* Text and elements */
            p, h1, h2, h3, h4, h5, h6, span {
                color: #E0E0E0 !important;
            }
            
            /* Tags */
            .tag-container {
                display: flex;
                flex-wrap: wrap;
                margin-top: 10px;
            }
            .tag {
                background-color: #444444 !important;
                color: #FFFFFF !important;
                padding: 2px 8px;
                border-radius: 10px;
                font-size: 0.75rem;
                margin-right: 5px;
                margin-bottom: 5px;
            }
            
            /* Importance indicators */
            .importance-indicator {
                color: #FFC107 !important;
            }
            
            /* Links with better contrast */
            .stMarkdown a {
                color: #6BBAFF !important;
                font-weight: 500 !important;
            }
            
            /* Tab styling */
            .stTabs [data-baseweb="tab-list"] {
                background-color: #2D2D2D !important;
            }
            .stTabs [data-baseweb="tab"] {
                color: #FFFFFF !important;
            }
            .stTabs [aria-selected="true"] {
                background-color: #3D3D3D !important;
            }
            
            /* Form elements with better contrast */
            .stTextInput>div>div>input, 
            .stSelectbox>div>div>div,
            .stNumberInput>div>div>input {
                background-color: #2D2D2D !important;
                color: #FFFFFF !important;
                border: 1px solid #4D4D4D !important;
            }
            
            /* Checkboxes and radio buttons */
            .stCheckbox>div>div>div, 
            .stRadio>div>div>div {
                color: #FFFFFF !important;
            }
            
            /* Buttons - Fixed button text styling */
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
            
            /* Yellow buttons with black text - with high specificity */
            .sidebar .stButton>button,
            div[data-testid="stSidebar"] .stButton>button,
            div[data-testid="stSidebar"] button,
            .sidebar button[kind="secondary"],
            .sidebar [data-testid="baseButton-secondary"],
            .sidebar [data-testid="element-container"] button {
                background-color: #FFC107 !important;
                color: #000000 !important;
                font-weight: 600 !important;
            }

            /* Extra specificity for yellow buttons */
            div[data-testid="stSidebar"] [data-testid="stButton"] > button {
                background-color: #FFC107 !important;
                color: #000000 !important;
                font-weight: 600 !important;
            }
            
            /* Sidebar styling - improved */
            div[data-testid="stSidebar"] {
                background-color: #1E1E1E !important;
            }
            
            div[data-testid="stSidebar"] p, 
            div[data-testid="stSidebar"] h1, 
            div[data-testid="stSidebar"] h2, 
            div[data-testid="stSidebar"] h3, 
            div[data-testid="stSidebar"] h4, 
            div[data-testid="stSidebar"] h5, 
            div[data-testid="stSidebar"] h6, 
            div[data-testid="stSidebar"] span, 
            div[data-testid="stSidebar"] label,
            div[data-testid="stSidebar"] div {
                color: #E0E0E0 !important;
            }
            
            /* Expanders and other containers */
            .streamlit-expanderHeader {
                background-color: #2D2D2D !important;
                color: #FFFFFF !important;
            }
            
            /* Sliders and progress bars */
            .stSlider>div>div {
                background-color: #3D3D3D !important;
            }
            
            /* DataFrames and tables */
            .stDataFrame {
                color: #FFFFFF !important;
            }
            .stDataFrame [data-testid="stTable"] {
                color: #FFFFFF !important;
            }
            
            /* Pagination controls */
            .pagination {
                color: #FFFFFF !important;
                font-weight: 500 !important;
            }
            
            /* Metrics */
            [data-testid="stMetricValue"] {
                color: #FFFFFF !important;
                font-weight: bold !important;
            }
            
            /* Sidebar toggle indicator */
            [data-testid="collapsedControl"] {
                background-color: #FFC107 !important;
                color: #000000 !important;  /* Black text for yellow button */
                border-radius: 50% !important;
                width: 36px !important;
                height: 36px !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                box-shadow: 0 2px 5px rgba(0,0,0,0.3) !important;
            }
            
            /* Fix navigation buttons */
            [data-testid="baseButton-primary"] {
                background-color: #FFC107 !important;
                color: #000000 !important;  /* Black text for yellow buttons */
            }
            
            /* Fix any other yellow UI elements */
            .stProgress .st-bo {
                background-color: #FFC107 !important;
                color: #000000 !important;
            }
            
            /* Additional selectors for sidebar text */
            div[data-testid="stSidebar"] .stCheckbox label,
            div[data-testid="stSidebar"] .stCheckbox label span,
            div[data-testid="stSidebar"] .stRadio label,
            div[data-testid="stSidebar"] .stRadio label span {
                color: #E0E0E0 !important;
                opacity: 1 !important;
            }
            
            /* Fix for all sidebar labels and text in dark mode */
            div[data-testid="stSidebar"] * {
                color: #E0E0E0 !important;
            }
            
            /* Restore button text to black for yellow buttons in sidebar */
            div[data-testid="stSidebar"] button,
            div[data-testid="stSidebar"] .stButton > button {
                color: #000000 !important;
            }
            
            /* Fix opacity issues in sidebar */
            div[data-testid="stSidebar"] label,
            div[data-testid="stSidebar"] p,
            div[data-testid="stSidebar"] span,
            div[data-testid="stSidebar"] div {
                opacity: 1 !important;
            }
            
            /* Target the expandable sections in sidebar */
            div[data-testid="stSidebar"] .streamlit-expanderHeader,
            div[data-testid="stSidebar"] .streamlit-expanderHeader span p,
            div[data-testid="stSidebar"] [data-testid="stExpander"] div {
                color: #E0E0E0 !important;
                opacity: 1 !important;
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
