# utils/theme.py
"""
Theme manager for the Indo-Pacific Dashboard.
Provides functionality to switch between light and dark mode.
"""

import streamlit as st  # Must import streamlit at the top

def set_theme_config():
    """
    Set up the theme configuration for the dashboard.
    Should be called at the beginning of the app.
    """
    # Initialize theme state if not already set
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'

def toggle_theme():
    """
    Toggle between light and dark mode.
    """
    if st.session_state.theme == 'light':
        st.session_state.theme = 'dark'
    else:
        st.session_state.theme = 'light'

def apply_theme():
    """
    Apply the current theme using custom CSS.
    This function should only be called AFTER st.set_page_config()
    """
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
        [data-testid="collapsedControl"]:after {
            content: "Filters";
            position: absolute;
            right: 45px;
            background: #4F8BF9;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 12px;
            white-space: nowrap;
            transform: translateY(-50%);
            top: 50%;
            opacity: 0;
            transition: opacity 0.3s;
        }
        [data-testid="collapsedControl"]:hover:after {
            opacity: 1;
        }
    </style>
    """
    
    dark_theme_css = """
    <style>
        .main {
            background-color: #1E1E1E;
            color: #E0E0E0;
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
        .stMarkdown a {
            color: #58A6FF;
        }
        .stTabs [data-baseweb="tab-list"] {
            background-color: #2D2D2D;
        }
        .stTabs [data-baseweb="tab"] {
            color: #E0E0E0;
        }
        .stTabs [aria-selected="true"] {
            background-color: #3D3D3D;
        }
        /* Improved button styling for dark mode */
        button, .stButton>button {
            background-color: #FFC107;
            color: #1E1E1E;
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
            color: #1E1E1E;
            border-radius: 50%;
            width: 36px;
            height: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.3);
        }
        [data-testid="collapsedControl"]:after {
            content: "Filters";
            position: absolute;
            right: 45px;
            background: #FFC107;
            color: #1E1E1E;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 12px;
            white-space: nowrap;
            transform: translateY(-50%);
            top: 50%;
            opacity: 0;
            transition: opacity 0.3s;
        }
        [data-testid="collapsedControl"]:hover:after {
            opacity: 1;
        }
        /* Better contrast for pagination and other elements */
        .pagination {
            color: #FFFFFF;
            font-weight: 500;
        }
        .stTextInput>div>div>input {
            color: #FFFFFF;
            background-color: #2D2D2D;
        }
        .stSelectbox>div>div>div {
            background-color: #2D2D2D;
            color: #FFFFFF;
        }
    </style>
    """
    
    # Apply the appropriate theme
    if st.session_state.theme == 'light':
        st.markdown(light_theme_css, unsafe_allow_html=True)
    else:
        st.markdown(dark_theme_css, unsafe_allow_html=True)

def create_theme_toggle():
    """
    Create a button to toggle between light and dark mode.
    """
    current_theme = st.session_state.theme
    icon = "🌙" if current_theme == 'light' else "☀️"
    label = f"{icon} Switch to {'Dark' if current_theme == 'light' else 'Light'} Mode"
    
    # Create HTML button with the appropriate styling
    button_html = f"""
    <button class="theme-toggle-button" onclick="document.getElementById('theme-toggle-button').click()">
        {label}
    </button>
    <button id="theme-toggle-button" style="display: none;"></button>
    """
    
    # Create an empty container for the button
    button_container = st.container()
    
    # Display the HTML button
    button_container.markdown(button_html, unsafe_allow_html=True)
    
    # Create a Streamlit button to capture the click event
    if button_container.button("Toggle Theme", key="theme-toggle", on_click=toggle_theme):
        st.experimental_rerun()
        
def get_moon_svg():
    """Get moon SVG icon for dark mode toggle."""
    return """
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-moon">
        <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
    </svg>
    """

def get_sun_svg():
    """Get sun SVG icon for light mode toggle."""
    return """
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-sun">
        <circle cx="12" cy="12" r="5"></circle>
        <line x1="12" y1="1" x2="12" y2="3"></line>
        <line x1="12" y1="21" x2="12" y2="23"></line>
        <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
        <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
        <line x1="1" y1="12" x2="3" y2="12"></line>
        <line x1="21" y1="12" x2="23" y2="12"></line>
        <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
        <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
    </svg>
    """
