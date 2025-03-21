# pages/02_Report_Generator.py
"""
Indo-Pacific Report Generator Page for Streamlit multi-page app
"""

import streamlit as st
import sys
import os
import datetime
import random
from pathlib import Path

# Add parent directory to path to import from main app
parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(parent_dir)

# Import required components
try:
    from components.report_generator import ReportGenerator
except ImportError:
    # Create a fallback if the component isn't found
    class ReportGenerator:
        def __init__(self, articles=None):
            self.articles = articles or []
        
        def create_report_ui(self):
            st.error("Report generator component not found. Please make sure 'components/report_generator.py' exists.")
            st.info("Try running the standalone dashboard first to set up all required components.")

# Set page config
st.set_page_config(
    page_title="Indo-Pacific Report Generator",
    page_icon="📊",
    layout="wide"
)

# Initialize session state for articles
if 'all_articles' not in st.session_state:
    st.session_state.all_articles = []

def generate_mock_articles(count=15):
    """Generate mock articles for demonstration"""
    
    sources = [
        "The Diplomat", "Asia Pacific Report", "RNZ Pacific", 
        "South China Morning Post", "Defense News", "East Asia Forum"
    ]
    
    topics = [
        "military exercise", "trade agreement", "diplomatic visit", 
        "security partnership", "territorial dispute", "naval deployment"
    ]
    
    countries = [
        "China", "Japan", "Australia", "United States", "India", 
        "Indonesia", "Philippines", "Malaysia", "Vietnam", "South Korea"
    ]
    
    articles = []
    
    # Generate random dates in the past 30 days
    now = datetime.datetime.now()
    
    for i in range(count):
        # Create random date
        days_ago = random.randint(0, 30)
        article_date = now - datetime.timedelta(days=days_ago)
        
        # Select random elements
        source = random.choice(sources)
        country1 = random.choice(countries)
        country2 = random.choice([c for c in countries if c != country1])
        topic = random.choice(topics)
        
        # Generate title
        title = f"{country1} and {country2} announce new {topic}"
        
        # Generate summary
        summary = (f"{country1} has announced a new {topic} with {country2}, "
                  f"signaling closer cooperation between the two nations. "
                  f"This development comes amid growing regional tensions and "
                  f"changing dynamics in the Indo-Pacific region.")
        
        # Create mock category information
        if "military" in topic or "security" in topic or "naval" in topic:
            categories = {'Military': 2, 'Political': 1}
        elif "trade" in topic or "economic" in topic:
            categories = {'Business': 2, 'Political': 1}
        elif "diplomatic" in topic:
            categories = {'Political': 2, 'Civil Affairs': 1}
        elif "territorial" in topic:
            categories = {'Political': 2, 'Military': 1}
        else:
            categories = {'Political': 1, 'Business': 1}
        
        # Generate mock sentiment
        sentiment = {
            country1: round(random.uniform(-0.8, 0.8), 2),
            country2: round(random.uniform(-0.8, 0.8), 2),
            "US": round(random.uniform(-0.8, 0.8), 2) if random.random() > 0.5 else None
        }
        sentiment = {k: v for k, v in sentiment.items() if v is not None}
        
        # Generate tags
        tags = topic.split() + [country1.lower(), country2.lower(), "indo-pacific"]
        
        article = {
            'title': title,
            'link': f"https://example.com/article{i}",
            'date': article_date,
            'summary': summary,
            'tags': tags[:5],
            'importance': random.randint(1, 5),
            'sentiment': sentiment,
            'source': source,
            'image_url': None,
            'categories': categories
        }
        
        articles.append(article)
    
    # Sort by date
    articles.sort(key=lambda x: x['date'], reverse=True)
    return articles

def main():
    st.title("Indo-Pacific Region Report Generator")
    
    st.markdown("""
    Generate comprehensive analytical reports from the aggregated news data.
    These reports include sentiment analysis, key developments, and regional trends.
    """)
    
    # Sidebar for data options
    with st.sidebar:
        st.header("Data Options")
        
        # Refresh data button
        if st.button("Refresh Data"):
            with st.spinner("Fetching latest news data..."):
                # Try to load from the main app's session state or generate mock data
                try:
                    # For multi-page setups, try to get data from session state
                    from app import get_article_data, RSS_FEEDS
                    
                    # Create dummy filters to get all articles
                    filters = {
                        'selected_sources': [],
                        'selected_topic': 'All',
                        'selected_country': 'All',
                        'min_importance': 1,
                        'sentiment_filter': 'All',
                        'sort_by': 'Date',
                        'search_term': '',
                        'time_filter': 'All Time'
                    }
                    
                    # Get all articles
                    st.session_state.all_articles = get_article_data(RSS_FEEDS, filters)
                    
                except (ImportError, AttributeError):
                    # If main app import fails, use mock data
                    st.session_state.all_articles = generate_mock_articles(15)
                    
                st.success("Data refreshed!")
        
        # Show current data stats
        st.subheader("Current Data")
        st.info(f"Articles loaded: {len(st.session_state.all_articles)}")
        
        if st.session_state.all_articles:
            dates = [a['date'] for a in st.session_state.all_articles]
            min_date = min(dates)
            max_date = max(dates)
            st.text(f"Date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")
            
            # Show article sources
            sources = set(a['source'] for a in st.session_state.all_articles)
            st.text(f"Sources: {len(sources)}")
            
            # Show categories
            categories = set()
            for article in st.session_state.all_articles:
                for category in article.get('categories', {}):
                    categories.add(category)
            
            st.text(f"Categories: {', '.join(categories)}")
        
        # About section
        st.markdown("---")
        st.markdown("""
        ### About Reports
        
        Reports are generated using article data and provide:
        
        - Comprehensive analysis
        - Sentiment evaluation
        - Regional trend identification
        - Key development highlights
        
        Reports can be downloaded in Markdown or HTML format.
        """)
    
    # Check if we have articles
    if not st.session_state.all_articles:
        st.warning("No articles loaded. Please fetch data using the sidebar button.")
        
        if st.button("Generate Mock Data"):
            with st.spinner("Creating mock data..."):
                st.session_state.all_articles = generate_mock_articles(15)
                st.success("Mock data created!")
                st.experimental_rerun()
        
        return
    
    # Create the report generator
    report_generator = ReportGenerator(st.session_state.all_articles)
    
    # Create UI for the report generator
    report_generator.create_report_ui()

if __name__ == "__main__":
    main()
