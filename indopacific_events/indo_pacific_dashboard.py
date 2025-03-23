# indo_pacific_dashboard.py
"""
Improved Indo-Pacific Dashboard
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
from streamlit.source_util import get_pages

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

# Function to hide specific pages in the sidebar
def hide_report_pages():
    # Get the streamlit pages dictionary
    pages = get_pages("")
    
    # Identify report generator pages to remove
    pages_to_remove = []
    for page, config in pages.items():
        if "report" in page.lower() or "Report" in page:
            pages_to_remove.append(page)
    
    # Remove the identified pages
    for page in pages_to_remove:
        try:
            del pages[page]
        except KeyError:
            pass

# Call this function immediately
hide_report_pages()

# Add CSS to ensure hamburger menu shows properly as 3 lines
st.markdown("""
<style>
/* Create the hamburger menu icon with 3 lines */
[data-testid="collapsedControl"] {
    display: block !important;
    visibility: visible !important;
    position: relative;
    width: 28px;
    height: 24px;
}

/* Add three bars to create hamburger icon */
[data-testid="collapsedControl"]::before,
[data-testid="collapsedControl"]::after,
[data-testid="collapsedControl"] span {
    content: '';
    display: block;
    position: absolute;
    height: 3px;
    width: 100%;
    background-color: currentColor;
    border-radius: 3px;
    left: 0;
}

[data-testid="collapsedControl"]::before {
    top: 5px;
}

[data-testid="collapsedControl"] span {
    top: 14px;
}

[data-testid="collapsedControl"]::after {
    bottom: 5px;
}

/* Hide the default arrow */
[data-testid="collapsedControl"] svg {
    display: none !important;
}

/* Ensure the menu items for report generator are hidden */
span a[href="./Report_Generator"],
span a[href="./report_generator"],
span a[href="./02_Report_Generator"],
span a[href*="report"] {
    display: none !important;
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
    Cached function to fetch and process articles with improved performance.
    """
    all_articles = []
    
    try:
        # Fetch RSS feeds with a loading indicator
        with st.spinner('Fetching articles...'):
            # Add a more detailed progress bar
            progress_bar = st.progress(0)
            
            # Set a smaller batch size for feeds to process at once
            # This prevents timeout issues with many feeds
            BATCH_SIZE = 5
            
            # Process feeds in smaller batches
            for i in range(0, len(selected_feeds), BATCH_SIZE):
                batch = selected_feeds[i:i+BATCH_SIZE]
                
                # Update progress
                progress_percentage = int((i / len(selected_feeds)) * 50)
                progress_bar.progress(progress_percentage)
                
                # Fetch this batch of feeds
                batch_feeds_data = cached_fetch_rss_feeds(batch)
                
                # Process each entry
                for source_idx, (source_name, feed) in enumerate(batch_feeds_data.items()):
                    # Update progress within batch
                    batch_progress = int((source_idx / len(batch_feeds_data)) * (50/len(selected_feeds)*BATCH_SIZE))
                    progress_bar.progress(progress_percentage + batch_progress)
                    
                    if not feed or 'entries' not in feed:
                        logger.warning(f"No entries found for {source_name}")
                        continue
                        
                    # Limit to the most recent entries per source to avoid overwhelming the system
                    recent_entries = feed['entries'][:10]  # Only process 10 most recent entries per source
                    
                    for entry in recent_entries:
                        try:
                            # Skip entries that indicate feed failures
                            title = entry.get('title', '')
                            if 'Unable to fetch content' in title:
                                continue
                            
                            # Process the entry
                            content = entry.get('summary', '')
                            
                            # Apply filters
                            # Country filter
                            if filters['selected_country'] != 'All':
                                if filters['selected_country'].lower() not in content.lower():
                                    continue
                            
                            # Generate article metadata - do this in a specific order
                            # to minimize processing for articles that will be filtered out
                            
                            # 1. First check categories to filter by topic
                            categories = get_category_analysis(content)
                            if filters['selected_topic'] != 'All' and filters['selected_topic'] not in categories:
                                continue
                            
                            # 2. Check importance
                            tags = generate_tags(content)
                            importance = rate_importance(content, tags)
                            if importance < filters['min_importance']:
                                continue
                            
                            # 3. Apply keyword search filter
                            if filters['search_term'] and filters['search_term'].lower() not in str(content).lower():
                                continue
                            
                            # 4. Generate summary only for articles that pass other filters
                            summary = generate_summary(content)
                            
                            # 5. Do sentiment analysis last as it's computationally expensive
                            sentiment = analyze_sentiment(content)
                            
                            # Add an 'Overall' sentiment if not present
                            if sentiment and 'Overall' not in sentiment:
                                sentiment_values = list(sentiment.values())
                                if sentiment_values:
                                    sentiment['Overall'] = round(sum(sentiment_values) / len(sentiment_values), 2)
                            
                            # Apply sentiment filter
                            if filters['sentiment_filter'] != 'All':
                                if filters['sentiment_filter'] == 'Positive sentiment' and not any(v > 0.1 for v in sentiment.values()):
                                    continue
                                if filters['sentiment_filter'] == 'Negative sentiment' and not any(v < -0.1 for v in sentiment.values()):
                                    continue
                                if filters['sentiment_filter'] == 'Neutral sentiment' and not any(-0.1 <= v <= 0.1 for v in sentiment.values()):
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
    
    # Cap the number of articles to prevent UI slowdowns
    if len(all_articles) > 50:
        st.warning(f"Limited to 50 most relevant articles out of {len(all_articles)} total matches")
        all_articles = all_articles[:50]
    
    return all_articles
