import streamlit as st
import feedparser
import requests
from PIL import Image
from io import BytesIO
import datetime
import os
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter
import ssl
from textblob import TextBlob
import pandas as pd

from importance_keywords import IMPORTANT_KEYWORDS

# Disable SSL verification (only if necessary)
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Function to download NLTK data if not already present
def download_nltk_data():
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)

download_nltk_data()

# Default img if unable to get image from RSS feed
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILLER_IMAGE_PATH = os.path.join(SCRIPT_DIR, "indo_pacific_filler_pic.jfif")

# RSS feeds including specific sources for New Caledonia and Wallis and Futuna
rss_feeds = [
    ("https://www.rnz.co.nz/rss/pacific.xml", "RNZ Pacific"),
    ("https://thediplomat.com/feed/", "The Diplomat"),
    ("https://www.eastasiaforum.org/feed/", "East Asia Forum"),
    ("https://www.lowyinstitute.org/the-interpreter/rss.xml", "The Interpreter"),
    ("https://www.pina.com.fj/feed/", "Pacific Islands News Association"),
    ("https://pidp.eastwestcenter.org/feed/", "Pacific Islands Development Program")
]

# Function to fetch and parse RSS feeds
@st.cache_data(ttl=3600)
def fetch_rss_feed(url):
    return feedparser.parse(url)

# Function to get image from URL
@st.cache_data(ttl=3600)
def get_image(url):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return img
    except:
        return Image.open(FILLER_IMAGE_PATH)

# Modified importance rating function to use 1-5 scale
def rate_importance(content, tags):
    score = 0
    content_lower = content.lower()
    
    # Check for keywords in content
    for keyword, weight in IMPORTANT_KEYWORDS.items():
        if keyword in content_lower:
            score += weight
    
    # Check for keywords in tags
    for tag in tags:
        if tag in IMPORTANT_KEYWORDS:
            score += IMPORTANT_KEYWORDS[tag]
    
    # Additional weight for specific scenarios
    if any(word in content_lower for word in ['emergency', 'urgent', 'breaking']):
        score += 5
        
    if any(phrase in content_lower for phrase in ['military conflict', 'armed forces', 'security threat']):
        score += 5
    
    # Convert score to 1-5 scale
    normalized_score = min(max(round(score / 20), 1), 5)
    
    return normalized_score

def generate_tags(content, num_tags=5):
    text = BeautifulSoup(content, "html.parser").get_text()
    stop_words = set(stopwords.words('english'))
    words = [word.lower() for word in word_tokenize(text) 
             if word.isalnum() and word.lower() not in stop_words]
    return [word for word, _ in Counter(words).most_common(num_tags)]

def generate_summary(content, num_sentences=3):
    text = BeautifulSoup(content, "html.parser").get_text()
    sentences = sent_tokenize(text)
    return ' '.join(sentences[:num_sentences])

def analyze_sentiment(text):
    blob = TextBlob(text)
    
    # Get sentiment scores
    sentiment_scores = {
        'US': 0,
        'China': 0,
        'overall': blob.sentiment.polarity
    }
    
    # Analyze sentiment towards specific countries
    for sentence in blob.sentences:
        if 'US' in sentence.string or 'United States' in sentence.string:
            sentiment_scores['US'] += sentence.sentiment.polarity
        if 'China' in sentence.string:
            sentiment_scores['China'] += sentence.sentiment.polarity
    
    return sentiment_scores

# Main Streamlit app
st.set_page_config(page_title="Indo-Pacific Current Events", layout="wide")
st.title("Indo-Pacific Current Events")

# Sidebar filters
st.sidebar.header("Filters")
selected_sources = st.sidebar.multiselect(
    "Select Sources",
    [feed[1] for feed in rss_feeds]
)

# Country filter
countries = ['All', 'New Caledonia', 'Wallis and Futuna']
selected_country = st.sidebar.selectbox("Select Country", countries)

# Importance filter
min_importance = st.sidebar.slider("Minimum Importance (1-5)", 1, 5, 1)

# Sentiment filter
sentiment_filter = st.sidebar.selectbox(
    "Sentiment Analysis",
    ['All', 'Positive towards US', 'Negative towards US']
)

sort_by = st.sidebar.selectbox("Sort By", ["Date", "Importance"])
search_term = st.sidebar.text_input("Search for keywords")

# Fetch and process articles
with st.spinner('Loading articles...'):
    all_articles = []
    for feed_url, source_name in rss_feeds:
        if not selected_sources or source_name in selected_sources:
            feed = fetch_rss_feed(feed_url)
            for entry in feed.entries:
                content = entry.get('summary', '')
                
                # Check country relevance
                if selected_country != 'All':
                    if selected_country.lower() not in content.lower():
                        continue
                
                tags = generate_tags(content)
                summary = generate_summary(content)
                importance = rate_importance(content, tags)
                sentiment = analyze_sentiment(content)
                
                # Apply importance filter
                if importance < min_importance:
                    continue
                
                # Apply sentiment filter
                if sentiment_filter != 'All':
                    if sentiment_filter == 'Positive towards US' and sentiment['US'] <= 0:
                        continue
                    if sentiment_filter == 'Negative towards US' and sentiment['US'] >= 0:
                        continue
                
                if not search_term or search_term.lower() in str(content).lower():
                    article = {
                        'title': entry.title,
                        'link': entry.link,
                        'date': datetime.datetime(*entry.published_parsed[:6]),
                        'summary': summary,
                        'tags': tags,
                        'importance': importance,
                        'sentiment': sentiment,
                        'source': source_name,
                        'image_url': entry.media_content[0]['url'] if 'media_content' in entry else None
                    }
                    all_articles.append(article)

    # Sort articles
    if sort_by == "Date":
        all_articles.sort(key=lambda x: x['date'], reverse=True)
    else:  # sort by importance
        all_articles.sort(key=lambda x: x['importance'], reverse=True)

# Display articles
for article in all_articles:
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if article['image_url']:
            img = get_image(article['image_url'])
        else:
            img = Image.open(FILLER_IMAGE_PATH)
        st.image(img, use_column_width=True)
    
    with col2:
        st.subheader(f"[{article['title']}]({article['link']})")
        st.write(f"Date: {article['date'].strftime('%Y-%m-%d %H:%M:%S')}")
        st.write(f"Summary: {article['summary']}")
        st.write(f"Importance Rating: {article['importance']}/5 ⭐")
        
        # Display sentiment with emojis
        st.write("Sentiment Analysis:")
        for entity, score in article['sentiment'].items():
            emoji = "🟢" if score > 0 else "🔴" if score < 0 else "⚪"
            st.write(f"- {entity}: {emoji} ({score:.2f})")
        
        st.write(f"Tags: {', '.join(article['tags'])}")
        st.write(f"Source: {article['source']}")
    
    st.markdown("---")

st.markdown("Dashboard created with Streamlit - Data sourced from various RSS feeds")
