# main.py
"""
Indo-Pacific Dashboard - Main Application
A comprehensive dashboard for monitoring and analyzing current events in the Indo-Pacific region.
"""

import streamlit as st
import os
import sys
import time
import datetime
import pandas as pd
import logging
from PIL import Image
import hashlib
from pathlib import Path

# Set up paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Ensure necessary directories exist
os.makedirs(os.path.join(SCRIPT_DIR, "data", "static", "images"), exist_ok=True)
os.makedirs(os.path.join(SCRIPT_DIR, "logs"), exist_ok=True)
os.makedirs(os.path.join(SCRIPT_DIR, "reports"), exist_ok=True)

# Set up logging
log_dir = os.path.join(SCRIPT_DIR, "logs")
log_file = os.path.join(log_dir, f"dashboard_{datetime.datetime.now().strftime('%Y-%m-%d')}.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("indo_pacific_dashboard")

# Initialize modules_loaded variable
modules_loaded = False
report_generator_available = False

# Import utility modules with error handling
try:
    # Import RSS feed parser
    from utils.feed_parser import cached_fetch_rss_feeds, process_entry
    # Import image handler
    from utils.image_handler import get_image
    # Import sentiment analysis
    from utils.sentiment import analyze_sentiment
    # Import text processing
    from utils.text_processor import generate_tags, generate_summary
    # Import data sources
    from data.keywords import IMPORTANT_KEYWORDS, CATEGORY_WEIGHTS
    from data.rss_sources import RSS_FEEDS, SOURCE_CATEGORIES
    # Import UI components
    from utils.theme import apply_theme, toggle_theme
    from components.filters import create_sidebar_filters
    from components.article_card_with_ner import display_article_with_ner as display_article
    
    # Try to import the simplified NER instead of the advanced one
    try:
        # First try the simplified NER
        from utils.simplified_ner import analyze_article_content
        logger.info("Using simplified NER implementation")
    except ImportError:
        # If that fails, try to fallback to a very basic implementation
        logger.warning("Simplified NER not available, using basic placeholder")
        
        # Define a basic placeholder function
        def analyze_article_content(text):
            return {
                "entities": {},
                "relationships": [],
                "importance": {}
            }
    
    # Import report generator (optional)
    try:
        from components.report_generator import ReportGenerator
        report_generator_available = True
    except ImportError:
        report_generator_available = False
        logger.warning("Report generator component not available")
        
    logger.info("Successfully imported all modules")
    modules_loaded = True  # Set to True only if all imports succeed
except Exception as e:
    logger.error(f"Error importing modules: {str(e)}")
    modules_loaded = False
    report_generator_available = False

# Configure Streamlit page
st.set_page_config(
    page_title="Indo-Pacific Current Events Dashboard",
    page_icon="🌏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'dashboard'
if 'selected_sources' not in st.session_state:
    st.session_state.selected_sources = []
if 'articles_data' not in st.session_state:
    st.session_state.articles_data = []
    
# Define view navigation function
def change_view(view_name):
    st.session_state.current_view = view_name

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
            feeds_data = cached_fetch_rss_feeds(selected_feeds)
            
            for source_name, feed in feeds_data.items():
                if not feed or 'entries' not in feed:
                    logger.warning(f"No entries found for {source_name}")
                    continue
                    
                # Process each entry
                for entry in feed.get('entries', [])[:10]:  # Limit to 10 most recent entries per source
                    try:
                        # Skip entries that indicate feed failures
                        title = entry.get('title', '')
                        if 'Unable to fetch content' in title:
                            continue
                        
                        # Extract the content for filtering and processing
                        content = entry.get('summary', '')
                        
                        # Apply country filter
                        if filters['selected_country'] != 'All':
                            if filters['selected_country'].lower() not in content.lower():
                                continue
                        
                        # Generate article metadata
                        categories = get_category_analysis(content)
                        
                        # Apply topic filter
                        if filters['selected_topic'] != 'All' and filters['selected_topic'] not in categories:
                            continue
                        
                        # Generate tags and calculate importance
                        tags = generate_tags(content)
                        importance = rate_importance(content, tags)
                        
                        # Apply importance filter
                        if importance < filters['min_importance']:
                            continue
                        
                        # Apply keyword search filter
                        if filters['search_term'] and filters['search_term'].lower() not in str(content).lower():
                            continue
                        
                        # Generate summary for articles that pass filters
                        summary = generate_summary(content)
                        
                        # Do sentiment analysis
                        sentiment = analyze_sentiment(content)
                        
                        # Apply sentiment filter
                        if filters['sentiment_filter'] != 'All':
                            if "US" in sentiment:
                                if filters['sentiment_filter'] == 'Positive towards US' and sentiment['US'] <= 0:
                                    continue
                                if filters['sentiment_filter'] == 'Negative towards US' and sentiment['US'] >= 0:
                                    continue
                            elif "China" in sentiment:
                                if filters['sentiment_filter'] == 'Positive towards China' and sentiment['China'] <= 0:
                                    continue
                                if filters['sentiment_filter'] == 'Negative towards China' and sentiment['China'] >= 0:
                                    continue
                        
                        # Convert time tuple to datetime
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
                        
                        # Create the article data dictionary
                        article = {
                            'title': title,
                            'link': entry.get('link', ''),
                            'date': pub_date,
                            'summary': summary,
                            'tags': tags,
                            'importance': importance,
                            'sentiment': sentiment,
                            'source': source_name,
                            'image_url': entry.get('media_content', [{}])[0].get('url') if entry.get('media_content') else None,
                            'categories': categories
                        }
                        all_articles.append(article)
                    except Exception as e:
                        logger.warning(f"Error processing article from {source_name}: {str(e)}")
                        continue
    except Exception as e:
        logger.error(f"Error fetching feeds: {str(e)}")
    
    # Sort articles based on the selected sorting option
    if filters['sort_by'] == 'Date':
        all_articles.sort(key=lambda x: x['date'], reverse=True)
    elif filters['sort_by'] == 'Importance':
        all_articles.sort(key=lambda x: x['importance'], reverse=True)
    elif filters['sort_by'] == 'Relevance':
        # For relevance sorting, combine importance with recency
        for article in all_articles:
            days_old = (datetime.datetime.now() - article['date']).days
            article['relevance_score'] = article['importance'] * (1 / (days_old + 1))
        all_articles.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
    
    # Cap the number of articles to prevent UI slowdowns
    if len(all_articles) > 50:
        logger.info(f"Limiting to 50 most relevant articles out of {len(all_articles)} total matches")
        all_articles = all_articles[:50]
    
    return all_articles

# Define the view functions - these are defined in the original code

def dashboard_view():
    """Main dashboard view showing filtered articles"""
    st.title("Indo-Pacific Current Events Dashboard")
    
    # Create filters in sidebar
    filters = create_sidebar_filters(RSS_FEEDS)
    
    # Get selected feed URLs based on selected sources
    selected_feeds = [(url, source) for url, source in RSS_FEEDS if source in filters['selected_sources']]
    
    # Display selected filters summary
    st.markdown("### Current Filters")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"**Sources:** {len(filters['selected_sources'])}/{len(RSS_FEEDS)} selected")
    with col2:
        st.write(f"**Topic:** {filters['selected_topic']}")
    with col3:
        st.write(f"**Country:** {filters['selected_country']}")
    
    # If no sources selected, use default sources
    if not filters['selected_sources']:
        # Get first three sources as default
        default_sources = [source for _, source in RSS_FEEDS[:3]]
        
        # Update session state and filters
        st.session_state.selected_sources = default_sources
        filters['selected_sources'] = default_sources
        
        # Update selected feeds
        selected_feeds = [(url, source) for url, source in RSS_FEEDS if source in default_sources]
        
        st.info(f"Using default news sources: {', '.join(default_sources)}")
    
    # Fetch and process articles
    with st.spinner("Fetching articles..."):
        articles = get_article_data(selected_feeds, filters)
    
    # Save articles for use in other views
    st.session_state.articles_data = articles
    
    # Display results count
    st.markdown(f"### Found {len(articles)} articles")
    
    # No articles found
    if not articles:
        st.info("No articles found matching your criteria. Try adjusting your filters.")
        return
    
    # Toggle view mode
    view_options = ["Card View", "Compact View", "Table View"]
    view_mode = st.radio("Select View Mode:", view_options, horizontal=True)
    
    # Pagination controls
    articles_per_page = 10
    total_pages = max(1, (len(articles) + articles_per_page - 1) // articles_per_page)
    
    # Initialize page number in session state if not present
    if 'page_number' not in st.session_state:
        st.session_state.page_number = 1
    
    # Ensure page number is valid
    if st.session_state.page_number > total_pages:
        st.session_state.page_number = 1
    
    # Page navigation
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("← Previous", disabled=st.session_state.page_number <= 1):
            st.session_state.page_number -= 1
            st.rerun()
    
    with col2:
        st.write(f"Page {st.session_state.page_number} of {total_pages}")
    
    with col3:
        if st.button("Next →", disabled=st.session_state.page_number >= total_pages):
            st.session_state.page_number += 1
            st.rerun()
    
    # Calculate slice indices for current page
    start_idx = (st.session_state.page_number - 1) * articles_per_page
    end_idx = min(start_idx + articles_per_page, len(articles))
    
    # Get current page articles
    current_page_articles = articles[start_idx:end_idx]
    
    # Display articles based on view mode
    if view_mode == "Table View":
        # Create a DataFrame for table view
        table_data = []
        for article in current_page_articles:
            table_data.append({
                "Date": article['date'].strftime("%Y-%m-%d"),
                "Title": article['title'],
                "Source": article['source'],
                "Importance": "⭐" * article['importance'],
                "Categories": ", ".join(article['categories'].keys())
            })
        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True)
    elif view_mode == "Compact View":
        # Compact view with minimal info
        for article in current_page_articles:
            with st.container():
                col1, col2 = st.columns([1, 5])
                with col1:
                    st.write(f"**{'⭐' * article['importance']}**")
                    st.write(article['date'].strftime("%Y-%m-%d"))
                with col2:
                    st.markdown(f"**[{article['title']}]({article['link']})**")
                    st.write(f"{article['source']} • {', '.join(list(article['categories'].keys())[:2])}")
                st.markdown("---")
    else:
        # Default card view
        for article in current_page_articles:
            try:
                # Determine importance class
                importance_class = "importance-low"
                if article['importance'] >= 4:
                    importance_class = "importance-high"
                elif article['importance'] >= 2:
                    importance_class = "importance-medium"
                
                # Get image if enabled
                image = None
                if filters.get('show_images', True) and article.get('image_url'):
                    try:
                        image = get_image(article['image_url'])
                    except Exception as e:
                        logger.warning(f"Error loading image: {str(e)}")
                
                # Display article card
                with st.container():
                    st.markdown(f"<div class='article-card {importance_class}'>", unsafe_allow_html=True)
                    
                    col1, col2 = st.columns([1, 3])
                    
                    with col1:
                        # Show image if available
                        if image is not None:
                            st.image(image, use_column_width=True)
                        
                        # Show importance
                        st.markdown(f"**Importance:** {'⭐' * article['importance']}")
                        
                        # Show source and date
                        st.markdown(f"**Source:** {article['source']}")
                        st.markdown(f"**Date:** {article['date'].strftime('%Y-%m-%d')}")
                        
                        # Show categories
                        if article.get('categories'):
                            st.markdown("**Categories:**")
                            for category, count in article['categories'].items():
                                st.markdown(f"- {category}: {count} mentions")
                    
                    with col2:
                        # Article title
                        st.markdown(f"## [{article['title']}]({article['link']})")
                        
                        # Summary
                        st.markdown(article['summary'])
                        
                        # Show tags if enabled
                        if filters.get('show_tags', True) and article.get('tags'):
                            st.markdown("**Tags:** " + ", ".join(article['tags']))
                        
                        # Show sentiment if enabled
                        if filters.get('show_sentiment', True) and article.get('sentiment'):
                            st.markdown("**Sentiment Analysis:**")
                            for entity, score in article['sentiment'].items():
                                # Determine color based on sentiment
                                color = "green" if score > 0 else "red" if score < 0 else "gray"
                                # Show sentiment bar
                                st.markdown(
                                    f"""
                                    <div style="display: flex; align-items: center; margin-bottom: 5px;">
                                        <div style="width: 80px;">{entity}:</div>
                                        <div style="background-color: {color}; width: {abs(score) * 50}%; 
                                                    height: 15px; border-radius: 3px;"></div>
                                        <div style="margin-left: 10px;">{score:.2f}</div>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )
                    
                    st.markdown("</div>", unsafe_allow_html=True)
            except Exception as e:
                # Log error but continue to next article
                logger.error(f"Error displaying article {article.get('title', 'Unknown')}: {str(e)}")
                continue
                
    # Add refresh button
    if st.button("Refresh Data"):
        st.cache_data.clear()
        st.rerun()

def analytics_view():
    """Analytics and data visualization view"""
    st.title("Indo-Pacific Analytics")
    
    # Get articles data
    all_articles = st.session_state.articles_data
    
    if not all_articles:
        st.warning("No article data available. Please select some sources and fetch articles first.")
        return
    
    st.write(f"Analyzing {len(all_articles)} articles")
    
    # Create tabs for different analytics views
    tab1, tab2, tab3, tab4 = st.tabs(["Category Breakdown", "Source Analysis", "Sentiment Analysis", "Importance Analysis"])
    
    with tab1:
        st.subheader("Articles by Category")
        # Count categories
        category_counts = {}
        for article in all_articles:
            for category in article.get('categories', {}).keys():
                if category not in category_counts:
                    category_counts[category] = 0
                category_counts[category] += 1
        
        # Create category data
        if category_counts:
            cat_df = pd.DataFrame({"Category": category_counts.keys(), "Count": category_counts.values()})
            cat_df = cat_df.sort_values("Count", ascending=False)
            
            # Show bar chart
            st.bar_chart(cat_df.set_index("Category"))
        else:
            st.info("No category data available.")
    
    with tab2:
        st.subheader("Articles by Source")
        # Count sources
        source_counts = {}
        for article in all_articles:
            source = article.get('source', 'Unknown')
            if source not in source_counts:
                source_counts[source] = 0
            source_counts[source] += 1
        
        # Create source data
        if source_counts:
            source_df = pd.DataFrame({"Source": source_counts.keys(), "Count": source_counts.values()})
            source_df = source_df.sort_values("Count", ascending=False)
            
            # Show bar chart
            st.bar_chart(source_df.set_index("Source"))
        else:
            st.info("No source data available.")
    
    with tab3:
        st.subheader("Sentiment Analysis")
        # Aggregate sentiment
        entity_sentiment = {}
        for article in all_articles:
            for entity, score in article.get('sentiment', {}).items():
                if entity not in entity_sentiment:
                    entity_sentiment[entity] = []
                entity_sentiment[entity].append(score)
        
        # Calculate average sentiment
        avg_sentiment = {}
        for entity, scores in entity_sentiment.items():
            avg_sentiment[entity] = sum(scores) / len(scores)
        
        # Create sentiment data
        if avg_sentiment:
            sentiment_df = pd.DataFrame({"Entity": avg_sentiment.keys(), "Sentiment": avg_sentiment.values()})
            sentiment_df = sentiment_df.sort_values("Sentiment", ascending=False)
            
            # Display chart
            st.bar_chart(sentiment_df.set_index("Entity"))
            
            # Show detailed sentiment breakdown
            st.subheader("Detailed Sentiment Analysis")
            for entity, score in avg_sentiment.items():
                # Determine status based on score
                if score > 0.1:
                    status = "Positive"
                    color = "green"
                elif score < -0.1:
                    status = "Negative"
                    color = "red"
                else:
                    status = "Neutral"
                    color = "gray"
                
                # Show sentiment with color coding
                st.markdown(f"**{entity}**: {score:.2f} - <span style='color:{color}'>{status}</span>", unsafe_allow_html=True)
        else:
            st.info("No sentiment data available.")
    
    with tab4:
        st.subheader("Importance Analysis")
        # Count importance ratings
        importance_counts = {}
        for i in range(1, 6):  # Importance from 1 to 5
            importance_counts[i] = 0
        
        for article in all_articles:
            importance = article.get('importance', 1)
            importance_counts[importance] += 1
        
        # Create importance data
        imp_df = pd.DataFrame({"Importance": importance_counts.keys(), "Count": importance_counts.values()})
        
        # Show chart
        st.bar_chart(imp_df.set_index("Importance"))
        
        # Show high importance articles
        st.subheader("High Importance Articles (Rating 4-5)")
        high_imp_articles = [a for a in all_articles if a.get('importance', 0) >= 4]
        
        if high_imp_articles:
            for article in high_imp_articles:
                st.markdown(f"**[{article['title']}]({article['link']})** - {article['source']}")
                st.markdown(f"Importance: {'⭐' * article['importance']} | Date: {article['date'].strftime('%Y-%m-%d')}")
                st.markdown("---")
        else:
            st.info("No high importance articles found.")

def reports_view():
    """Reports generation view"""
    st.title("Indo-Pacific Reports Generator")
    
    if not report_generator_available:
        st.error("Report generator component is not available.")
        st.info("Please make sure the report_generator.py module is properly installed and accessible.")
        return
    
    # Get all articles data for reports
    all_articles = st.session_state.articles_data
    
    # If no articles available, try to fetch from default sources
    if not all_articles:
        st.warning("No article data available. Please select some sources and fetch articles first.")
        # Get a few default sources
        default_sources = [source for _, source in RSS_FEEDS[:3]]
        default_feeds = [(url, source) for url, source in RSS_FEEDS if source in default_sources]
        
        if st.button("Fetch Data from Default Sources"):
            with st.spinner("Fetching article data..."):
                # Use default filters
                default_filters = {
                    "selected_sources": default_sources,
                    "selected_topic": "All",
                    "selected_country": "All",
                    "min_importance": 1,
                    "sentiment_filter": "All",
                    "sort_by": "Date",
                    "search_term": "",
                    "time_filter": "Past Week"
                }
                all_articles = get_article_data(default_feeds, default_filters)
                st.session_state.articles_data = all_articles
                st.success(f"Fetched {len(all_articles)} articles.")
    
    # Initialize report generator
    report_gen = ReportGenerator(all_articles)
    
    # Create report generator UI
    report_gen.create_report_ui()

def settings_view():
    """Settings and configuration view"""
    st.title("Dashboard Settings")
    
    # Theme settings
    st.header("UI Settings")
    col1, col2 = st.columns(2)
    
    with col1:
        # Theme selection
        current_theme = st.session_state.get('theme', 'light')
        new_theme = st.radio(
            "Select Theme",
            options=["Light", "Dark"],
            index=0 if current_theme == 'light' else 1
        )
        
        # Update theme if changed
        if (new_theme == "Light" and current_theme != 'light') or (new_theme == "Dark" and current_theme != 'dark'):
            st.session_state.theme = new_theme.lower()
            st.success(f"Theme changed to {new_theme}. Refresh to see changes.")
            st.button("Apply Theme", on_click=lambda: st.rerun())
    
    with col2:
        # Default view
        default_view = st.selectbox(
            "Default Dashboard View",
            options=["Dashboard", "Reports", "Analytics", "Settings"],
            index=0
        )
        
        # Number of articles per page
        articles_per_page = st.slider(
            "Articles Per Page",
            min_value=5,
            max_value=50,
            value=20,
            step=5
        )
    
    # Feed settings
    st.header("Feed Settings")
    
    # Cache duration
    cache_duration = st.slider(
        "Cache Duration (hours)",
        min_value=1,
        max_value=24,
        value=2,
        help="How long to cache feed data before refreshing"
    )
    
    # Add custom feed
    st.subheader("Add Custom RSS Feed")
    with st.form("add_feed_form"):
        feed_url = st.text_input("Feed URL", placeholder="https://example.com/rss")
        feed_name = st.text_input("Feed Name", placeholder="Example News")
        
        # Add feed button
        submitted = st.form_submit_button("Add Feed")
        if submitted and feed_url and feed_name:
            st.success(f"Added feed: {feed_name}")
            # In a real implementation, this would update the RSS_FEEDS list
            st.info("Note: Custom feeds are not persistent in this version")
    
    # System information
    st.header("System Information")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Python Version", sys.version.split()[0])
        st.metric("Streamlit Version", st.__version__)
    
    with col2:
        st.metric("Last Updated", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        st.metric("Articles in Cache", len(st.session_state.get('articles_data', [])))
    
    # View logs option
    with st.expander("View Error Logs"):
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                log_content = f.read()
            st.text_area("Log Content", log_content, height=300)
            
            # Download logs button
            st.download_button(
                label="Download Logs",
                data=log_content,
                file_name=f"dashboard_logs_{datetime.datetime.now().strftime('%Y-%m-%d')}.log",
                mime="text/plain"
            )
        else:
            st.info("No log file found.")
    
    # Clear cache button
    if st.button("Clear Cache"):
        st.cache_data.clear()
        st.success("Cache cleared successfully!")

def about_view():
    """About page view"""
    st.title("About Indo-Pacific Dashboard")
    
    st.markdown("""
    ## Indo-Pacific Current Events Dashboard
    
    A comprehensive real-time dashboard for monitoring and analyzing current events in the Indo-Pacific region. 
    This tool uses RSS feeds from reputable sources to present categorized, filtered, and prioritized news 
    with importance ratings and sentiment analysis.

    ### Features

    - **Multi-source News Aggregation**: Collects and consolidates news from multiple RSS feeds.
    - **Advanced Filtering**: Filter by country, topic, importance, and sentiment.
    - **Importance Rating**: Automatically rates article importance using keyword-based weighting.
    - **Sentiment Analysis**: Analyzes sentiment toward key regional actors.
    - **Categorical Analysis**: Classifies content into key regional topics:
      - Political & Diplomatic
      - Military & Defense
      - Civil Affairs
      - Drug Proliferation
      - CWMD (Counter Weapons of Mass Destruction)
      - Business & Economic
      - Regional Specific (New Caledonia, Wallis and Futuna, etc.)
    - **Search Functionality**: Find specific events and topics across all sources.
    - **Visual Presentation**: Clean, responsive interface with images and importance indicators.
    
    ### Acknowledgments
    
    - Streamlit for the fantastic web application framework
    - All the news sources that provide RSS feeds for their content
    - NLTK and TextBlob for text processing
    
    ### Version
    
    Current Version: 1.0.0
    
    """)
    
    # Show license
    with st.expander("License"):
        st.markdown("""
        ### MIT License

        Copyright (c) 2025 Indo-Pacific Dashboard

        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in all
        copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
        SOFTWARE.
        """)

def main():
    """Main function to run the dashboard"""
    # Apply theme
    if modules_loaded and 'theme' in st.session_state:
        try:
            apply_theme()
        except Exception as e:
            logger.error(f"Error applying theme: {str(e)}")
    
    # Add navigation in sidebar
    st.sidebar.title("Indo-Pacific Dashboard")
    
    # Navigation buttons
    nav_options = [
        ("🏠 Dashboard", "dashboard"),
        ("📊 Analytics", "analytics"),
        ("📑 Reports", "reports"),
        ("⚙️ Settings", "settings"),
        ("ℹ️ About", "about")
    ]
    
    st.sidebar.markdown("### Navigation")
    
    for label, view in nav_options:
        if st.sidebar.button(label, key=f"nav_{view}"):
            change_view(view)
    
    # Add theme toggle
    current_theme = st.session_state.get('theme', 'light')
    theme_icon = "🌙" if current_theme == 'light' else "☀️"
    theme_label = f"{theme_icon} {'Dark' if current_theme == 'light' else 'Light'} Mode"
    
    if st.sidebar.button(theme_label, key="theme_toggle"):
        st.session_state.theme = 'dark' if current_theme == 'light' else 'light'
        st.rerun()
    
    # Add footer to sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("© 2025 Indo-Pacific Dashboard")
    st.sidebar.markdown("Version 1.0.0")
    
    # Display appropriate view based on session state
    current_view = st.session_state.get('current_view', 'dashboard')
    
    try:
        if current_view == 'dashboard':
            dashboard_view()
        elif current_view == 'reports':
            reports_view()
        elif current_view == 'analytics':
            analytics_view()
        elif current_view == 'settings':
            settings_view()
        elif current_view == 'about':
            about_view()
        else:
            st.error(f"Unknown view: {current_view}")
            dashboard_view()  # Fallback to dashboard
    except Exception as e:
        logger.error(f"Error rendering view {current_view}: {str(e)}")
        st.error(f"Error rendering view: {str(e)}")
        st.info("Please check the logs for details or try refreshing the page.")

if __name__ == "__main__":
    main()
