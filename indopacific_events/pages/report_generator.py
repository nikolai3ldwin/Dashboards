# pages/report_generator.py
"""
Report generator page for the Indo-Pacific Dashboard.
This page allows users to generate comprehensive reports based on article data.
"""

import streamlit as st
import sys
import os
import datetime
from pathlib import Path

# Add the parent directory to the path to import from the main app
parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Import components from the main app
from components.report_generator import ReportGenerator
from utils.feed_parser import cached_fetch_rss_feeds
from data.rss_sources import RSS_FEEDS

# Set page config
st.set_page_config(
    page_title="Indo-Pacific Report Generator",
    page_icon="📊",
    layout="wide"
)

# Initialize session state for report generation
if 'generated_report' not in st.session_state:
    st.session_state.generated_report = None
if 'all_articles' not in st.session_state:
    st.session_state.all_articles = []

def main():
    """Main function to render the report generator page"""
    st.title("Indo-Pacific Region Report Generator")
    st.markdown("""
    Generate comprehensive analytical reports from the aggregated news data.
    These reports include sentiment analysis, key developments, and regional trends.
    """)
    
    # Sidebar for fetching data
    with st.sidebar:
        st.header("Data Options")
        
        # Option to reload data
        if st.button("Refresh Data"):
            with st.spinner("Fetching latest news data..."):
                # Clear the cache to force refresh
                st.cache_data.clear()
                fetch_latest_data()
                st.success("Data refreshed successfully!")
        
        # Show data stats
        st.subheader("Current Data")
        st.info(f"Articles loaded: {len(st.session_state.all_articles)}")
        if st.session_state.all_articles:
            dates = [a['date'] for a in st.session_state.all_articles]
            min_date = min(dates)
            max_date = max(dates)
            st.text(f"Date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")
        
        # About section
        st.markdown("---")
        st.markdown("""
        ### About Reports
        
        Reports are generated using all available article data and provide:
        
        - Comprehensive analysis
        - Sentiment evaluation
        - Regional trend identification
        - Key development highlights
        
        Reports can be downloaded in Markdown or HTML format.
        """)
    
    # Main content - Report Generator
    report_generator = ReportGenerator(st.session_state.all_articles)
    
    # Check if we have articles
    if not st.session_state.all_articles:
        st.warning("No articles loaded. Please fetch data using the sidebar button.")
        fetch_latest_data()  # Try to fetch initially
        
        if not st.session_state.all_articles:
            st.error("Unable to load articles. Please try refreshing.")
            return
    
    # Create UI for report generator
    report_generator.create_report_ui()
    
def fetch_latest_data():
    """Fetch and process the latest news data for reports"""
    try:
        # Get all feed sources
        feeds_data = cached_fetch_rss_feeds(RSS_FEEDS)
        
        # Process into articles
        all_articles = []
        
        for source_name, feed in feeds_data.items():
            if not feed or 'entries' not in feed:
                continue
                
            for entry in feed.get('entries', []):
                try:
                    # Basic processing only - we'll rely on the dashboard's full processing
                    # for sentiment, tags, etc.
                    
                    # Convert time tuple to datetime safely
                    try:
                        pub_date = datetime.datetime(*entry['published_parsed'][:6]) if entry.get('published_parsed') else datetime.datetime.now()
                    except (TypeError, ValueError):
                        pub_date = datetime.datetime.now()
                    
                    article = {
                        'title': entry.get('title', 'No Title'),
                        'link': entry.get('link', ''),
                        'date': pub_date,
                        'summary': entry.get('summary', 'No summary available.'),
                        'source': source_name,
                        'importance': 1,  # Default importance
                        'sentiment': {},  # Empty sentiment
                        'categories': {}  # Empty categories
                    }
                    
                    all_articles.append(article)
                except Exception as e:
                    st.error(f"Error processing article: {str(e)}")
                    continue
                
        # Store in session state
        st.session_state.all_articles = all_articles
        
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return []

if __name__ == "__main__":
    main()
