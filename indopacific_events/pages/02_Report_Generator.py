# pages/02_Report_Generator.py
"""
Indo-Pacific Report Generator Page - Redirects to main app for consistency
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path
parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# This page will simply redirect to the main app with reports view
st.set_page_config(
    page_title="Indo-Pacific Report Generator",
    page_icon="📊",
    layout="wide"
)

st.title("Indo-Pacific Report Generator")

st.info("""
This page has been moved to the main dashboard.
Please use the "📑 Reports View" button in the main application.

You will be redirected in a few seconds...
""")

# Add redirect script
st.markdown(
    '''
    <script>
        // Redirect to main app after a short delay
        setTimeout(function() {
            window.location.href = "/";
        }, 3000);
    </script>
    ''',
    unsafe_allow_html=True
)

# Add a button for manual navigation
if st.button("Go to Main Dashboard"):
    st.switch_page("indo_pacific_dashboard.py")
