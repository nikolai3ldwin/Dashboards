# Example integration into your indo_pacific_dashboard.py file

import streamlit as st
import datetime
import os
import sys

# Ensure the necessary directories exist
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(SCRIPT_DIR, "data", "static", "images"), exist_ok=True)

# Add current directory to path if needed
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

# Initialize the theme state before any st commands
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

# This MUST be the first Streamlit command
st.set_page_config(
    page_title="Indo-Pacific Current Events", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Now import utilities AFTER st.set_page_config
try:
    from utils.feed_parser import fetch_rss_feeds, process_entry
    from utils.image_handler import get_image
    from utils.sentiment import analyze_sentiment
    from utils.text_processor import generate_tags, generate_summary
    from utils.theme import apply_theme, toggle_theme
    from utils.logger import get_dashboard_logger
    
    # Initialize the logger
    dashboard_logger = get_dashboard_logger(SCRIPT_DIR)
    logger = dashboard_logger.get_logger()
    
    # Import data sources
    from data.keywords import IMPORTANT_KEYWORDS, CATEGORY_WEIGHTS
    from data.rss_sources import RSS_FEEDS
    
    # Import UI components
    from components.filters import create_sidebar_filters
    from components.article_card import display_article
    
    # Apply theme right after st.set_page_config
    apply_theme()
    
    # Constants
    FILLER_IMAGE_PATH = os.path.join(SCRIPT_DIR, "data", "static", "images", "indo_pacific_filler_pic.jpg")
    
except Exception as e:
    st.error(f"Error during initialization: {str(e)}")
    st.info("Please make sure all required modules and directories exist.")
    st.stop()

# ... [rest of your existing code] ...

def main():
    # Add header
    header_cols = st.columns([3, 1])
    with header_cols[0]:
        st.title("Indo-Pacific Current Events Dashboard")
    with header_cols[1]:
        # Add theme toggle button
        current_theme = st.session_state.theme
        theme_label = "🌙 Dark Mode" if current_theme == 'light' else "☀️ Light Mode"
        st.button(theme_label, on_click=toggle_theme)
    
    # Create sidebar filters
    filters = create_sidebar_filters(RSS_FEEDS)
    
    # Fetch and process articles
    with st.spinner('Loading articles...'):
        all_articles = []
        
        # Only fetch from selected sources or all if none selected
        selected_feeds = [(url, name) for url, name in RSS_FEEDS 
                         if name in filters['selected_sources'] or not filters['selected_sources']]
        
        try:
            # Fetch RSS feeds
            feeds_data = fetch_rss_feeds(selected_feeds)
            
            # Process each entry
            for source_name, feed in feeds_data.items():
                if not feed or 'entries' not in feed:
                    # Use logger instead of st.warning
                    logger.warning(f"Could not fetch feed from {source_name}")
                    continue
                    
                for entry in feed['entries']:
                    try:
                        # Process the entry
                        content = entry.get('summary', '')
                        
                        # Skip mock entries if we're not in debug mode
                        if 'Unable to fetch content' in entry.get('title', '') and not st.session_state.get('debug_mode', False):
                            continue
                            
                        # Process article...
                        # [rest of your article processing code...]
                        
                        article = {
                            'title': entry['title'],
                            'link': entry['link'],
                            'date': pub_date,
                            'summary': summary,
                            'tags': tags,
                            'importance': importance,
                            'sentiment': sentiment,
                            'source': source_name,
                            'image_url': entry['media_content'][0]['url'] if entry.get('media_content') and entry['media_content'] else None,
                            'categories': categories
                        }
                        all_articles.append(article)
                    except Exception as e:
                        # Use logger instead of st.warning
                        dashboard_logger.log_article_error(source_name, e)
                        continue
        except Exception as e:
            # Use logger instead of st.error
            logger.error(f"Error fetching feeds: {str(e)}")

        # [rest of your code...]

    # Debug mode toggle and log viewer
    with st.expander("Advanced Options"):
        debug_mode = st.checkbox("Debug Mode", value=st.session_state.get('debug_mode', False))
        st.session_state.debug_mode = debug_mode
        
        if debug_mode:
            # Display log viewer using the dashboard logger
            dashboard_logger.create_log_viewer()
            
            st.write("Feed Sources:")
            for url, name in RSS_FEEDS:
                st.write(f"- {name}: {url}")
            
            if st.button("Reset All Settings"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.experimental_rerun()

if __name__ == "__main__":
    main()
