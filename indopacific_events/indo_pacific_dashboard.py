import streamlit as st
import feedparser
import requests
from PIL import Image
from io import BytesIO
import datetime
import random
import os

# default img if unable to get image from RSS feed

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILLER_IMAGE_PATH = os.path.join(SCRIPT_DIR, "indo_pacific_filler_pic.jfif")

# Function to fetch and parse RSS feeds


def fetch_rss_feed(url):
    return feedparser.parse(url)

# Function to get image from URL


def get_image(url):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return img
    except:
        # Return the filler image if the URL image can't be fetched
        return Image.open(FILLER_IMAGE_PATH)

# Function to generate a summary (placeholder)


def generate_summary(content):
    # In a real application, you might use NLP techniques here
    return content[:200] + "..."

# Function to rate importance (placeholder)


def rate_importance():
    # In a real application, you might use more sophisticated logic
    return round(random.uniform(1, 10), 1)


# Set page title
st.set_page_config(
    page_title="Indo-Pacific Current Events Dashboard", layout="wide")

# Title
st.title("Indo-Pacific Current Events Dashboard")

# RSS feed URLs (replace with actual Indo-Pacific news RSS feeds)
rss_feeds = [
    "https://www.eastasiaforum.org/feed/",
    "https://thediplomat.com/feed/",
    "https://www.lowyinstitute.org/the-interpreter/rss.xml"
]

# Fetch and display articles
for feed_url in rss_feeds:
    feed = fetch_rss_feed(feed_url)
    st.header(feed.feed.title)

    for entry in feed.entries[:5]:  # Display top 5 articles from each feed
        col1, col2 = st.columns([1, 3])

        with col1:
            img = None
            if 'media_content' in entry and entry.media_content:
                img_url = entry.media_content[0]['url']
                img = get_image(img_url)
            elif 'links' in entry and len(entry.links) > 1:
                img_url = entry.links[1].href
                img = get_image(img_url)

            if img is None:
                img = Image.open(FILLER_IMAGE_PATH)

            st.image(img, use_column_width=True)

        with col2:
            st.subheader(entry.title)
            if 'published_parsed' in entry and entry.published_parsed:
                date = datetime.datetime(
                    *entry.published_parsed[:6]).strftime('%Y-%m-%d %H:%M:%S')
            else:
                date = "Date not available"
            st.write(f"Date: {date}")

            if 'summary' in entry:
                st.write(entry.summary)
            else:
                st.write("Summary not available")

            st.write("Generated Summary:")
            st.write(generate_summary(entry.get('summary', '')))

            importance = rate_importance()
            st.write(
                f"Importance Rating (Civil Affairs Perspective): {importance}/10")

        st.markdown("---")

# Add a footer
st.markdown(
    "Dashboard created with Streamlit - Data sourced from various RSS feeds - By SGT Nikolai Baldwin")
