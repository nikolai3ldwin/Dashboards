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

# Download NLTK data
download_nltk_data()

# default img if unable to get image from RSS feed
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILLER_IMAGE_PATH = os.path.join(SCRIPT_DIR, "indo_pacific_filler_pic.jfif")

# Function to fetch and parse RSS feeds


@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_rss_feed(url):
    return feedparser.parse(url)

# Function to get image from URL


@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_image(url):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return img
    except:
        # Return the filler image if the URL image can't be fetched
        return Image.open(FILLER_IMAGE_PATH)

# Function to generate tags


def generate_tags(content, num_tags=5):
    # Remove HTML tags
    text = BeautifulSoup(content, "html.parser").get_text()

    # Tokenize and remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word.lower() for word in word_tokenize(
        text) if word.isalnum() and word.lower() not in stop_words]

    # Get most common words as tags
    return [word for word, _ in Counter(words).most_common(num_tags)]

# Function to generate a summary


def generate_summary(content, num_sentences=3):
    # Remove HTML tags
    text = BeautifulSoup(content, "html.parser").get_text()

    # Split into sentences and return first n sentences
    sentences = sent_tokenize(text)
    return ' '.join(sentences[:num_sentences])

# Function to rate importance


def rate_importance(content, tags):
    # This is a simple scoring method. You might want to develop a more sophisticated one.
    important_keywords = ['crisis', 'conflict',
                          'treaty', 'agreement', 'election', 'disaster']
    score = sum(content.lower().count(keyword)
                for keyword in important_keywords)
    # Add score for important tags
    score += len(set(tags) & set(important_keywords))
    return min(round(score / 2, 1), 10)  # Ensure max score is 10


# Set page title
st.set_page_config(
    page_title="Indo-Pacific Current Events Dashboard", layout="wide")

# Title
st.title("Indo-Pacific Current Events Dashboard")

# RSS feed URLs
rss_feeds = [
    "https://www.eastasiaforum.org/feed/",
    "https://thediplomat.com/feed/",
    "https://www.lowyinstitute.org/the-interpreter/rss.xml"
]

# Sidebar for filters
st.sidebar.header("Filters")
selected_sources = st.sidebar.multiselect(
    "Select Sources", [feed.split('/')[-2] for feed in rss_feeds])
sort_by = st.sidebar.selectbox("Sort By", ["Date", "Importance"])
search_term = st.sidebar.text_input("Search for keywords")

# Fetch all articles
with st.spinner('Loading articles...'):
    all_articles = []
    for feed_url in rss_feeds:
        feed = fetch_rss_feed(feed_url)
        source = feed_url.split('/')[-2]
        if not selected_sources or source in selected_sources:
            for entry in feed.entries:
                tags = generate_tags(entry.get('summary', ''))
                summary = generate_summary(entry.get('summary', ''))
                importance = rate_importance(entry.get('summary', ''), tags)
                article = {
                    'title': entry.title,
                    'link': entry.link,
                    'date': datetime.datetime(*entry.published_parsed[:6]),
                    'summary': summary,
                    'tags': tags,
                    'importance': importance,
                    'source': source,
                    'image_url': entry.media_content[0]['url'] if 'media_content' in entry else None
                }
                if not search_term or search_term.lower() in str(article).lower():
                    all_articles.append(article)

    # Sort articles
    if sort_by == "Date":
        all_articles.sort(key=lambda x: x['date'], reverse=True)
    else:
        all_articles.sort(key=lambda x: x['importance'], reverse=True)

# After loading is complete
st.success('Articles loaded successfully!')

# Display articles
for article in all_articles:
    col1, col2 = st.columns([1, 3])
    with col1:
        if article['image_url']:
            img = get_image(article['image_url'])
        else:
            img = Image.open(FILLER_IMAGE_PATH)
        st.image(img, use_column_width=True,
                 caption=f"[View Article]({article['link']})")

    with col2:
        st.subheader(f"[{article['title']}]({article['link']})")
        st.write(f"Date: {article['date'].strftime('%Y-%m-%d %H:%M:%S')}")
        st.write(f"Summary: {article['summary']}")
        st.write(f"Tags: {', '.join(article['tags'])}")
        st.write(f"Importance Rating: {article['importance']}/10")
        st.write(f"Source: {article['source']}")

    st.markdown("---")

# Add a footer
st.markdown(
    "Dashboard created with Streamlit - Data sourced from various RSS feeds - By SGT Nikolai Baldwin")
