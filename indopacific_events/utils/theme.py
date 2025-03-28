# utils/theme.py
# Update this file with the expanded dark mode styling

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
            /* Dark mode styling - EXPANDED */
            .main {
                background-color: #121212 !important;
                color: #E0E0E0 !important;
            }
            .stApp {
                background-color: #121212 !important;
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
            
            /* Text and elements */
            p, h1, h2, h3, h4, h5, h6, span {
                color: #E0E0E0 !important;
            }
            
            /* Article cards and containers */
            .article-card {
                background-color: #1E1E1E !important;
                border: 1px solid #3D3D3D !important;
                box-shadow: 0 2px 5px rgba(0,0,0,0.3) !important;
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
            
            /* Buttons */
            button, .stButton>button {
                background-color: #FFC107 !important;
                color: #000000 !important;
                border: none !important;
                border-radius: 5px !important;
                padding: 8px 16px !important;
                cursor: pointer !important;
                transition: background-color 0.3s !important;
                font-weight: 600 !important;
                box-shadow: 0 2px 5px rgba(0,0,0,0.3) !important;
            }
            button:hover, .stButton>button:hover {
                background-color: #FFCA28 !important;
            }
            
            /* Sidebar styling */
            .sidebar .sidebar-content {
                background-color: #1E1E1E !important;
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
                color: #000000 !important;
                border-radius: 50% !important;
                width: 36px !important;
                height: 36px !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                box-shadow: 0 2px 5px rgba(0,0,0,0.3) !important;
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
