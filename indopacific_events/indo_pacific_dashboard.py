# indo_pacific_dashboard.py
"""
Indo-Pacific Dashboard - Main application file

A Streamlit dashboard for monitoring and analyzing current events in the Indo-Pacific region.
"""

import streamlit as st
import datetime
import pandas as pd
import os
import sys

# Import theme manager
from utils.theme import set_theme_config, apply_theme, create_theme_toggle

# Set up error handling
try:
    # Ensure the necessary directories exist
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(SCRIPT_DIR, "data", "static", "images"), exist_ok=True)
    
    # Add current directory to path if needed
    if SCRIPT_DIR not in sys.path:
        sys.path.insert(0, SCRIPT_DIR)
    
    # Import utility modules
    from utils.feed_parser import fetch_rss_feeds, process_entry
    from utils.image_handler import get_image
    from utils.sentiment import analyze_sentiment
    from utils.text_processor import generate_tags, generate_summary
    
    # Import data sources
    from data.keywords import IMPORTANT_KEYWORDS, CATEGORY_WEIGHTS
    from data.rss_sources import RSS_FEEDS
    
    # Import UI components
    from components.filters import create_sidebar_filters
    from components.article_card import display_article
    
    # Constants
    FILLER_IMAGE_PATH = os.path.join(SCRIPT_DIR, "data", "static", "images", "indo_pacific_filler_pic.jpg")
    
except Exception as e:
    st.error(f"Error during initialization: {str(e)}")
    st.info("Please make sure all required modules and directories exist.")
    st.stop()

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

def main():
    # Initialize and apply theme
    set_theme_config()
    apply_theme()
    
    # Configure page settings
    st.set_page_config(page_title="Indo-Pacific Current Events", layout="wide")
    
    # Add theme toggle in header
    header_cols = st.columns([3, 1])
    with header_cols[0]:
        st.title("Indo-Pacific Current Events Dashboard")
    with header_cols[1]:
        create_theme_toggle()
    
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
                    st.warning(f"Could not fetch feed from {source_name}")
                    continue
                    
                for entry in feed['entries']:
                    try:
                        # Process the entry
                        content = entry.get('summary', '')
                        
                        # Skip mock entries if we're not in debug mode
                        if 'Unable to fetch content' in entry.get('title', '') and not st.session_state.get('debug_mode', False):
                            continue
                            
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
                        
                        # Generate article metadata
                        tags = generate_tags(content)
                        summary = generate_summary(content)
                        importance = rate_importance(content, tags)
                        sentiment = analyze_sentiment(content)
                        categories = get_category_analysis(content)
                        
                        # Apply importance filter
                        if importance < filters['min_importance']:
                            continue
                        
                        # Apply sentiment filter
                        if filters['sentiment_filter'] != 'All':
                            if filters['sentiment_filter'] == 'Positive towards US' and sentiment.get('US', 0) <= 0:
                                continue
                            if filters['sentiment_filter'] == 'Negative towards US' and sentiment.get('US', 0) >= 0:
                                continue
                            if filters['sentiment_filter'] == 'Positive towards China' and sentiment.get('China', 0) <= 0:
                                continue
                            if filters['sentiment_filter'] == 'Negative towards China' and sentiment.get('China', 0) >= 0:
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
                        st.warning(f"Error processing article from {source_name}: {str(e)}")
                        continue
        except Exception as e:
            st.error(f"Error fetching feeds: {str(e)}")

        # Display a message if no articles were found
        if not all_articles:
            st.warning("No articles match your current filter criteria. Try adjusting your filters.")
            # Add a button to reset filters
            if st.button("Reset Filters"):
                # Reset session state for filters
                if 'selected_sources' in st.session_state:
                    st.session_state.selected_sources = []
                # Force page refresh
                st.experimental_rerun()
            st.stop()

        # Sort articles
        if filters['sort_by'] == "Date":
            all_articles.sort(key=lambda x: x['date'], reverse=True)
        elif filters['sort_by'] == "Importance":
            all_articles.sort(key=lambda x: x['importance'], reverse=True)
        elif filters['sort_by'] == "Relevance":
            # Sort by number of category hits if a topic filter is applied
            if filters['selected_topic'] != 'All':
                all_articles.sort(key=lambda x: x['categories'].get(filters['selected_topic'], 0), reverse=True)
            else:
                all_articles.sort(key=lambda x: len(x['categories']), reverse=True)
                
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Articles", len(all_articles))
    with col2:
        avg_importance = round(sum(a['importance'] for a in all_articles) / max(len(all_articles), 1), 1)
        st.metric("Average Importance", f"{avg_importance}/5")
    with col3:
        topic_counts = {}
        for article in all_articles:
            for category in article['categories']:
                topic_counts[category] = topic_counts.get(category, 0) + 1
        top_topic = max(topic_counts.items(), key=lambda x: x[1])[0] if topic_counts else "None"
        st.metric("Top Topic", top_topic)
    with col4:
        recent_date = max([a['date'] for a in all_articles], default=datetime.datetime.now())
        st.metric("Most Recent", recent_date.strftime("%Y-%m-%d %H:%M"))
    
    # Pagination controls
    articles_per_page = 10
    if 'page' not in st.session_state:
        st.session_state.page = 0
        
    total_pages = (len(all_articles) - 1) // articles_per_page + 1
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("← Previous", disabled=st.session_state.page <= 0):
            st.session_state.page -= 1
            st.experimental_rerun()
    
    with col2:
        st.write(f"Page {st.session_state.page + 1} of {total_pages}")
        
    with col3:
        if st.button("Next →", disabled=st.session_state.page >= total_pages - 1):
            st.session_state.page += 1
            st.experimental_rerun()
    
    # Calculate slice for current page
    start_idx = st.session_state.page * articles_per_page
    end_idx = min(start_idx + articles_per_page, len(all_articles))
    
    # Display articles for current page
    for article in all_articles[start_idx:end_idx]:
        try:
            display_article(article, get_image(article['image_url']))
        except Exception as e:
            st.error(f"Error displaying article: {str(e)}")
            continue
    
    # Bottom pagination controls
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("← Previous", key="prev_bottom", disabled=st.session_state.page <= 0):
            st.session_state.page -= 1
            st.experimental_rerun()
    
    with col2:
        st.write(f"Page {st.session_state.page + 1} of {total_pages}")
        
    with col3:
        if st.button("Next →", key="next_bottom", disabled=st.session_state.page >= total_pages - 1):
            st.session_state.page += 1
            st.experimental_rerun()
    
    # Footer
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("Dashboard created with Streamlit - Data sourced from various RSS feeds")
    with col2:
        st.markdown(f"Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    # Debug mode toggle
    with st.expander("Advanced Options"):
        debug_mode = st.checkbox("Debug Mode", value=st.session_state.get('debug_mode', False))
        st.session_state.debug_mode = debug_mode
        
        if debug_mode:
            st.write("Feed Sources:")
            for url, name in RSS_FEEDS:
                st.write(f"- {name}: {url}")
            
            if st.button("Reset All Settings"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.experimental_rerun()

if __name__ == "__main__":
    main()
