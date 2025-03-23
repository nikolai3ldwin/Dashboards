# indo_pacific_dashboard.py
"""
Improved Indo-Pacific Dashboard with better UI and UX
"""

# Third-party imports
import streamlit as st # import first
import pandas as pd

# Standard library imports
import os
import sys
import time
import logging
import datetime
import hashlib

# Ensure the necessary directories exist
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(SCRIPT_DIR, "data", "static", "images"), exist_ok=True)
os.makedirs(os.path.join(SCRIPT_DIR, "reports"), exist_ok=True)

# Add current directory to path if needed
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

# Initialize the theme state before any st commands
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

# Initialize the current view state
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'dashboard'

# Initialize loading state
if 'initialization_complete' not in st.session_state:
    st.session_state.initialization_complete = False

# This MUST be the first Streamlit command
st.set_page_config(
    page_title="Indo-Pacific Current Events", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add CSS to ensure hamburger menu always shows and is properly styled
st.markdown("""
<style>
/* Always show hamburger menu with proper styling */
[data-testid="collapsedControl"] {
    display: block !important;
    visibility: visible !important;
}

/* Hamburger menu style - 3 lines instead of arrow */
[data-testid="collapsedControl"] {
    border: none !important;
    background-color: transparent !important;
}

/* Dark mode improvements */
@media (prefers-color-scheme: dark) {
    .stButton>button {
        background-color: #4F8BF9 !important;
        color: white !important;
    }
    
    .stSelectbox>div>div>div {
        background-color: #2D2D2D !important;
        color: white !important;
        border: 1px solid #4D4D4D !important;
    }
    
    /* Make sidebar buttons more visible in dark mode */
    .sidebar .stButton>button {
        background-color: #FFC107 !important;
        color: black !important;
    }
}

/* Remove fixed sidebar height to allow scrolling */
section[data-testid="stSidebar"] {
    height: auto !important;
    max-height: none !important;
    overflow: visible !important;
}

/* Improve sentiment analysis display - make it always visible */
.sentiment-section {
    margin-top: 10px;
    margin-bottom: 10px;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #ddd;
}

/* Improved filter section */
.filter-section {
    margin-bottom: 20px;
    padding: 10px;
    border-radius: 5px;
    background-color: #f9f9f9;
}

/* Dark mode filter section */
@media (prefers-color-scheme: dark) {
    .filter-section {
        background-color: #2D2D2D;
    }
}
</style>
""", unsafe_allow_html=True)

# Set up a basic logger
log_dir = os.path.join(SCRIPT_DIR, "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"dashboard_{datetime.datetime.now().strftime('%Y-%m-%d')}.log")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()  # Output to console for debugging
    ]
)
logger = logging.getLogger("indo_pacific_dashboard")

# Render early header to prevent blank screen
try:
    # Create a container for early rendering to prevent blank screen
    with st.container():
        st.title("Indo-Pacific Current Events Dashboard")
        if not st.session_state.initialization_complete:
            st.info("Loading dashboard components and fetching articles...")
except Exception as e:
    st.error(f"Error during early UI rendering: {str(e)}")
    logger.error(f"Error during early UI rendering: {str(e)}")

# Now import utilities
try:
    # Import UI theme functionality
    from utils.theme import apply_theme, toggle_theme
    
    # Apply theme immediately
    apply_theme()
    
    # Import other utilities
    from utils.feed_parser import cached_fetch_rss_feeds, process_entry
    from utils.image_handler import get_image
    from utils.sentiment import analyze_sentiment
    from utils.text_processor import generate_tags, generate_summary
    
    # Import data sources
    from data.keywords import IMPORTANT_KEYWORDS, CATEGORY_WEIGHTS
    from data.rss_sources import RSS_FEEDS
    
    # Import UI components - we'll use a modified version
    from components.article_card import display_article
    
    # Modified version of sidebar filters to match requirements
    def create_sidebar_filters(rss_feeds):
        """
        Create and handle all sidebar filters for the dashboard with improved UI.
        """
        st.sidebar.title("Dashboard Filters")
        
        # Source selection with categorized layout
        from data.rss_sources import SOURCE_CATEGORIES
        
        # Show expand/collapse all option
        st.sidebar.markdown("### News Sources")
        
        all_sources = [source for _, source in rss_feeds]
        
        # Initialize with empty list if state doesn't exist
        if 'selected_sources' not in st.session_state:
            st.session_state.selected_sources = []
        
        # Add Select All / Clear All buttons
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("Select All", key="select_all_sources"):
                st.session_state.selected_sources = all_sources.copy()
        with col2:
            if st.button("Clear All", key="clear_all_sources"):
                st.session_state.selected_sources = []
        
        # Display source categories as expandable sections
        selected_sources = []
        for category, sources in SOURCE_CATEGORIES.items():
            with st.sidebar.expander(f"{category} ({len(sources)})"):
                for source in sources:
                    if source in all_sources:
                        is_selected = st.checkbox(
                            source,
                            value=source in st.session_state.selected_sources
                        )
                        if is_selected and source not in selected_sources:
                            selected_sources.append(source)
        
        # Update session state
        st.session_state.selected_sources = selected_sources
        
        # Topic filter with new categories
        st.sidebar.markdown("### Topic Filters")
        
        topics = [
            "All", 
            "Political", 
            "Military", 
            "Civil Affairs", 
            "Drug Proliferation",
            "CWMD", 
            "Business"
        ]
        
        selected_topic = st.sidebar.selectbox(
            "Select Topic Category",
            topics
        )
        
        # Country filter
        countries = [
            "All", 
            "New Caledonia", 
            "Wallis and Futuna", 
            "China", 
            "United States",
            "Japan", 
            "Australia", 
            "India", 
            "Indonesia", 
            "Philippines", 
            "Malaysia",
            "Vietnam", 
            "South Korea", 
            "Taiwan", 
            "Thailand",
            "Cambodia", 
            "Myanmar", 
            "Papua New Guinea", 
            "Fiji", 
            "Solomon Islands",
            "Vanuatu", 
            "Samoa", 
            "Tonga", 
            "Cook Islands"
        ]
        
        selected_country = st.sidebar.selectbox(
            "Select Country/Region",
            countries
        )
        
        # Importance filter
        st.sidebar.markdown("### Content Filters")
        
        min_importance = st.sidebar.slider(
            "Minimum Importance Rating",
            min_value=1,
            max_value=5,
            value=1,
            help="Filter articles by their importance rating (1-5)"
        )
        
        # Improved sentiment filter with generic country options
        sentiment_options = [
            "All", 
            "Positive sentiment", 
            "Negative sentiment",
            "Neutral sentiment"
        ]
        
        # Add dynamically generated country filters based on the most common entities
        # in the sentiment analysis of recent articles
        common_sentiment_entities = ["Regional", "Overall"]  # Default entities
        
        # This will be expanded dynamically as articles are processed
        sentiment_filter = st.sidebar.selectbox(
            "Sentiment Analysis",
            sentiment_options
        )
        
        # Sort options
        sort_options = ["Date", "Importance", "Relevance"]
        sort_by = st.sidebar.selectbox(
            "Sort Results By",
            sort_options
        )
        
        # Keyword search
        search_term = st.sidebar.text_input(
            "Search for keywords",
            help="Enter keywords to search across all articles"
        )
        
        # Time period filter
        time_periods = [
            "All Time",
            "Today",
            "Past Week",
            "Past Month",
            "Past 3 Months"
        ]
        
        time_filter = st.sidebar.selectbox(
            "Time Period",
            time_periods
        )
        
        # Advanced options expander
        with st.sidebar.expander("Advanced Options"):
            # Display options
            st.markdown("#### Display Options")
            show_images = st.checkbox("Show Images", value=True)
            show_sentiment = st.checkbox("Show Sentiment Analysis", value=True)
            show_tags = st.checkbox("Show Tags", value=True)
            
            # Export options
            st.markdown("#### Export Options")
            export_format = st.selectbox(
                "Export Format",
                ["CSV", "JSON", "Excel"]
            )
            
            if st.button("Export Results"):
                st.info("Export functionality to be implemented")
        
        # About section
        with st.sidebar.expander("About This Dashboard"):
            st.markdown("""
            This dashboard aggregates news from multiple sources 
            across the Indo-Pacific region and categorizes them 
            based on importance, topics, and sentiment.
            
            **Version**: 1.0.0
            
            **GitHub**: [Project Repository](https://github.com/yourusername/indo-pacific-dashboard)
            """)
        
        # Return all filter settings as a dictionary
        return {
            "selected_sources": selected_sources,
            "selected_topic": selected_topic,
            "selected_country": selected_country,
            "min_importance": min_importance,
            "sentiment_filter": sentiment_filter,
            "sort_by": sort_by,
            "search_term": search_term,
            "time_filter": time_filter,
            "show_images": show_images,
            "show_sentiment": show_sentiment,
            "show_tags": show_tags
        }
    
    # Import the report generator component
    try:
        from components.report_generator import ReportGenerator
        logger.info("Report generator component loaded successfully")
    except Exception as e:
        logger.error(f"Error loading report generator component: {str(e)}")
        # Create a mock Report Generator class to prevent crashes
        class ReportGenerator:
            def __init__(self, articles=None):
                self.articles = articles or []
            def create_report_ui(self):
                st.warning("Report generator component could not be loaded. Please check logs.")
                st.error(f"Error: {str(e)}")
    
    # Constants
    FILLER_IMAGE_PATH = os.path.join(SCRIPT_DIR, "data", "static", "images", "indo_pacific_filler_pic.jpg")
    
except Exception as e:
    logger.error(f"Error during initialization: {str(e)}")
    st.error(f"Error during initialization: {str(e)}")
    st.info("Please make sure all required modules and directories exist.")
    st.stop()

# Performance measurement decorator
def measure_time(func):
    """Decorator to measure the execution time of functions"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        logger.info(f"Function '{func.__name__}' executed in {duration:.2f} seconds")
        return result
    return wrapper

def rate_importance(content, tags):
    """
    Rate the importance of an article based on keywords and tags.
    Returns a score from 1-5.
    """
    score = 0
    content_lower = content.lower()
    
    # Check for keywords in content
    for keyword, weight in IMPORTANT_KEYWORDS.items():
        if keyword.lower() in content_lower:
            score += weight
    
    # Check for keywords in tags
    for tag in tags:
        if tag.lower() in IMPORTANT_KEYWORDS:
            score += IMPORTANT_KEYWORDS[tag.lower()]
    
    # Additional weight for specific scenarios
    if any(word in content_lower for word in ['emergency', 'urgent', 'breaking']):
        score += 5
        
    if any(phrase in content_lower for phrase in ['military conflict', 'armed forces', 'security threat']):
        score += 5
    
    # Convert score to 1-5 scale
    normalized_score = min(max(round(score / 20), 1), 5)
    
    return normalized_score

def get_category_analysis(content):
    """
    Analyze which categories are most prominent in the article.
    Returns a dictionary of category scores.
    """
    from data.keywords import (
        POLITICAL_KEYWORDS, MILITARY_KEYWORDS, CIVIL_AFFAIRS_KEYWORDS,
        DRUG_PROLIFERATION_KEYWORDS, CWMD_KEYWORDS, BUSINESS_KEYWORDS
    )
    
    content_lower = content.lower()
    categories = {
        'Political': 0,
        'Military': 0,
        'Civil Affairs': 0,
        'Drug Proliferation': 0,
        'CWMD': 0,
        'Business': 0,
    }
    
    # Count mentions of keywords in each category
    for keyword in POLITICAL_KEYWORDS:
        if keyword.lower() in content_lower:
            categories['Political'] += 1
            
    for keyword in MILITARY_KEYWORDS:
        if keyword.lower() in content_lower:
            categories['Military'] += 1
            
    for keyword in CIVIL_AFFAIRS_KEYWORDS:
        if keyword.lower() in content_lower:
            categories['Civil Affairs'] += 1
            
    for keyword in DRUG_PROLIFERATION_KEYWORDS:
        if keyword.lower() in content_lower:
            categories['Drug Proliferation'] += 1
            
    for keyword in CWMD_KEYWORDS:
        if keyword.lower() in content_lower:
            categories['CWMD'] += 1
            
    for keyword in BUSINESS_KEYWORDS:
        if keyword.lower() in content_lower:
            categories['Business'] += 1
    
    # Return only categories that have at least one hit
    return {k: v for k, v in categories.items() if v > 0}

@st.cache_data(ttl=7200)  # Cache for 2 hours
def get_article_data(selected_feeds, filters):
    """
    Cached function to fetch and process articles.
    This separates data fetching from UI rendering for better performance.
    """
    all_articles = []
    
    try:
        # Fetch RSS feeds with a loading indicator
        with st.spinner('Fetching articles...'):
            # Add a more detailed progress bar
            progress_bar = st.progress(0)
            
            # Fetch the data
            feeds_data = cached_fetch_rss_feeds(selected_feeds)
            progress_bar.progress(50)
            
            # Process each entry
            for source_idx, (source_name, feed) in enumerate(feeds_data.items()):
                # Update progress
                progress_percentage = 50 + int((source_idx / len(feeds_data)) * 50)
                progress_bar.progress(progress_percentage)
                
                if not feed or 'entries' not in feed:
                    logger.warning(f"No entries found for {source_name}")
                    continue
                    
                for entry in feed['entries']:
                    try:
                        # Skip entries that indicate feed failures
                        title = entry.get('title', '')
                        if 'Unable to fetch content' in title:
                            continue
                        
                        # Process the entry
                        content = entry.get('summary', '')
                        
                        # Check country relevance
                        if filters['selected_country'] != 'All':
                            if filters['selected_country'].lower() not in content.lower():
                                continue
                        
                        # Check topic relevance if selected
                        if filters['selected_topic'] != 'All':
                            # Get categories for this article
                            categories = get_category_analysis(content)
                            if filters['selected_topic'] not in categories:
                                continue
                        else:
                            # Generate categories only if needed
                            categories = get_category_analysis(content)
                        
                        # Generate article metadata
                        tags = generate_tags(content)
                        summary = generate_summary(content)
                        importance = rate_importance(content, tags)
                        sentiment = analyze_sentiment(content)
                        
                        # Add an 'Overall' sentiment if not present
                        if sentiment and 'Overall' not in sentiment:
                            sentiment_values = list(sentiment.values())
                            if sentiment_values:
                                sentiment['Overall'] = round(sum(sentiment_values) / len(sentiment_values), 2)
                        
                        # Apply importance filter
                        if importance < filters['min_importance']:
                            continue
                        
                        # Apply sentiment filter
                        if filters['sentiment_filter'] != 'All':
                            if filters['sentiment_filter'] == 'Positive sentiment' and not any(v > 0.1 for v in sentiment.values()):
                                continue
                            if filters['sentiment_filter'] == 'Negative sentiment' and not any(v < -0.1 for v in sentiment.values()):
                                continue
                            if filters['sentiment_filter'] == 'Neutral sentiment' and not any(-0.1 <= v <= 0.1 for v in sentiment.values()):
                                continue
                        
                        # Apply keyword search
                        if filters['search_term'] and filters['search_term'].lower() not in str(content).lower():
                            continue
                            
                        # Convert time tuple to datetime safely
                        try:
                            pub_date = datetime.datetime(*entry['published_parsed'][:6]) if entry.get('published_parsed') else datetime.datetime.now()
                        except (TypeError, ValueError):
                            pub_date = datetime.datetime.now()
                        
                        # Apply time filter
                        if filters['time_filter'] != 'All Time':
                            now = datetime.datetime.now()
                            if filters['time_filter'] == 'Today' and (now - pub_date).days > 1:
                                continue
                            elif filters['time_filter'] == 'Past Week' and (now - pub_date).days > 7:
                                continue
                            elif filters['time_filter'] == 'Past Month' and (now - pub_date).days > 30:
                                continue
                            elif filters['time_filter'] == 'Past 3 Months' and (now - pub_date).days > 90:
                                continue
                        
                        article = {
                            'title': title,
                            'link': entry.get('link', ''),
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
                        logger.warning(f"Error processing article from {source_name}: {str(e)}")
                        continue
            
            # Clear progress bar when done
            progress_bar.empty()
    except Exception as e:
        logger.error(f"Error fetching feeds: {str(e)}")
    
    return all_articles

# Improved article display function to show sentiment and tags inline (not hidden)
def display_article_improved(article, image):
    """
    Display a single article in a card format with improved sentiment display.
    
    Parameters:
    -----------
    article : dict
        Article data dictionary containing title, date, summary, etc.
    image : PIL.Image
        Image to display with the article
    """
    # Create a card with a border
    with st.container():
        st.markdown("---")
        
        # Two-column layout
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Display the image
            st.image(image, use_column_width=True)
            
            # Display importance rating with stars
            importance_stars = "⭐" * article['importance']
            st.markdown(f"**Importance:** {importance_stars}")
            
            # Display source and date
            st.markdown(f"**Source:** {article['source']}")
            st.markdown(f"**Date:** {article['date'].strftime('%Y-%m-%d %H:%M')}")
            
            # Display categories
            if article.get('categories'):
                st.markdown("**Categories:**")
                for category, count in article['categories'].items():
                    st.markdown(f"- {category}: {count} mentions")
        
        with col2:
            # Article title as link
            st.markdown(f"## [{article['title']}]({article['link']})")
            
            # Summary
            st.markdown(f"{article['summary']}")
            
            # Always display tags directly (not in expander)
            if article.get('tags'):
                st.markdown("**Tags:** " + ", ".join(article['tags']))
            
            # Always display sentiment analysis directly (not in expander)
            if article.get('sentiment'):
                st.markdown("**Sentiment Analysis:**")
                
                # Create a horizontal bar chart for sentiment
                for entity, score in article['sentiment'].items():
                    # Determine color based on sentiment
                    color = "green" if score > 0 else "red" if score < 0 else "gray"
                    
                    # Calculate width percentage (convert -1 to 1 scale to 0-100%)
                    width = abs(score) * 50  # 50% is neutral
                    
                    # Display horizontal bar
                    st.markdown(
                        f"""
                        <div style="display: flex; align-items: center; margin-bottom: 5px;">
                            <div style="width: 80px;">{entity}:</div>
                            <div style="background-color: {color}; width: {width}%; 
                                        height: 15px; border-radius: 3px;"></div>
                            <div style="margin-left: 10px;">{score:.2f}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
            # Call to action buttons
            col_a, col_b, col_c = st.columns(3)
            
            # Create a unique key for each button based on multiple properties
            unique_key = hashlib.md5(
                f"{article['title']}{article['link']}{str(article['date'])}{article['source']}".encode()
            ).hexdigest()[:12]
            
            with col_a:
                st.button("Read Full Article", 
                          key=f"read_{unique_key}", 
                          help=f"Open {article['link']}")
            with col_b:
                st.button("Save for Later", 
                          key=f"save_{unique_key}", 
                          help="Save this article to your reading list")
            with col_c:
                st.button("Share", 
                          key=f"share_{unique_key}", 
                          help="Share this article")

# Function to display logs in debug mode
def display_logs():
    """Display recent logs in the debug section"""
    with st.expander("View Error Logs"):
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                log_content = f.readlines()
                
            # Filter to show only warnings and errors
            error_logs = [line for line in log_content if 'ERROR' in line or 'WARNING' in line]
            
            # Show the most recent logs (limited to 50 for performance)
            recent_logs = error_logs[-50:] if len(error_logs) > 50 else error_logs
            
            # Display error logs with formatting
            st.text_area("Recent Errors and Warnings", value="".join(recent_logs), height=300)
            
            # Add log management options
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Clear Logs"):
                    try:
                        # Backup the log file before clearing
                        backup_file = os.path.join(
                            log_dir, 
                            f"dashboard_{datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')}_backup.log"
                        )
                        with open(log_file, 'r') as src, open(backup_file, 'w') as dst:
                            dst.write(src.read())
                        
                        # Clear the log file
                        with open(log_file, 'w') as f:
                            f.write(f"Log cleared at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        
                        st.success("Logs cleared successfully")
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f"Error clearing logs: {str(e)}")
            
            with col2:
                if st.button("Download Logs"):
                    try:
                        with open(log_file, 'r') as f:
                            log_content = f.read()
                        
                        st.download_button(
                            label="Download Log File",
                            data=log_content,
                            file_name=f"dashboard_logs_{datetime.datetime.now().strftime('%Y-%m-%d')}.log",
                            mime="text/plain"
                        )
                    except Exception as e:
                        st.error(f"Error preparing logs for download: {str(e)}")
        else:
            st.info("No log file found for today.")

# Function to render the reports view
def render_reports_view(all_articles):
    """
    Render the reports page with report generation functionality
    
    Parameters:
    -----------
    all_articles : list
        List of processed article dictionaries
    """
    st.title("Indo-Pacific Analysis Reports")
    
    st.markdown("""
    Generate comprehensive analytical reports based on the aggregated news data.
    These reports include sentiment analysis, key developments, and regional trends.
    """)
