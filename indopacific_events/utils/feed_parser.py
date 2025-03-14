# feed_parser.py
"""
Utilities for fetching and processing RSS feeds for the Indo-Pacific Dashboard.
"""

import streamlit as st
import feedparser
import requests
import time
from bs4 import BeautifulSoup
import datetime
from .text_processor import clean_html

# Import configuration
from data.rss_sources import FEED_CONFIG

@st.cache_data(ttl=FEED_CONFIG.get("cache_ttl", 3600))
def fetch_rss_feeds(feed_list):
    """
    Fetch RSS feeds from multiple sources with caching and error handling.
    
    Parameters:
    -----------
    feed_list : list
        List of (url, source_name) tuples
    
    Returns:
    --------
    dict
        Dictionary mapping source names to processed feed data
    """
    results = {}
    
    for feed_url, source_name in feed_list:
        try:
            feed_data = fetch_single_feed(feed_url)
            if feed_data and feed_data.get('entries'):
                results[source_name] = feed_data
        except Exception as e:
            st.warning(f"Error fetching {source_name}: {str(e)}")
    
    return results

def fetch_single_feed(url):
    """
    Fetch a single RSS feed with retry logic and error handling.
    
    Parameters:
    -----------
    url : str
        URL of the RSS feed to fetch
    
    Returns:
    --------
    dict
        Processed feed data with entries
    """
    max_retries = FEED_CONFIG.get("max_retries", 3)
    retry_delay = FEED_CONFIG.get("retry_delay", 1)  # seconds
    timeout = FEED_CONFIG.get("timeout", 10)  # seconds
    
    for attempt in range(max_retries):
        try:
            # Add headers to mimic a browser request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # Use requests to get the feed content first
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            feed = feedparser.parse(response.content)
            
            # Check if feed was successfully parsed
            if feed.get('status', 0) != 200 and feed.get('entries', []) == []:
                raise Exception(f"Failed to parse feed: Status {feed.get('status', 'unknown')}")
            
            # Convert to a more easily serializable format
            entries = []
            for entry in feed.entries:
                processed_entry = process_entry(entry)
                entries.append(processed_entry)
            
            if not entries:
                raise Exception("No entries found in feed")
                
            return {'entries': entries, 'status': feed.get('status', 0)}
            
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            else:
                raise Exception(f"Failed after {max_retries} attempts: {str(e)}")

def process_entry(entry):
    """
    Process a single feed entry into a standardized format.
    
    Parameters:
    -----------
    entry : dict
        RSS feed entry from feedparser
    
    Returns:
    --------
    dict
        Processed entry with standardized fields
    """
    # Extract data with safe fallbacks
    title = entry.get('title', 'No Title')
    link = entry.get('link', '')
    summary = extract_summary(entry)
    published = entry.get('published_parsed') or entry.get('updated_parsed')
    
    # Extract media/images
    media_content = []
    
    # Try multiple methods to find images
    if hasattr(entry, 'media_content'):
        media_content = [{'url': m.get('url', '')} for m in entry.get('media_content', [])]
    
    # Look for enclosures (another way RSS can include images)
    elif hasattr(entry, 'enclosures') and entry.enclosures:
        for enclosure in entry.enclosures:
            if enclosure.get('type', '').startswith('image/'):
                media_content.append({'url': enclosure.get('href', '')})
    
    # Look for images in content
    elif hasattr(entry, 'content') and entry.content:
        for content in entry.content:
            if content.get('type') == 'text/html':
                soup = BeautifulSoup(content.value, 'html.parser')
                img_tags = soup.find_all('img')
                for img in img_tags:
                    if img.get('src'):
                        media_content.append({'url': img.get('src')})
                        break  # Just get the first image
    
    # Look in summary for images as last resort
    elif not media_content and hasattr(entry, 'summary'):
        soup = BeautifulSoup(entry.summary, 'html.parser')
        img_tags = soup.find_all('img')
        for img in img_tags:
            if img.get('src'):
                media_content.append({'url': img.get('src')})
                break  # Just get the first image

    return {
        'title': title,
        'link': link,
        'summary': summary,
        'published_parsed': published,
        'media_content': media_content
    }

def extract_summary(entry):
    """
    Extract a clean summary from an RSS entry.
    
    Parameters:
    -----------
    entry : dict
        RSS feed entry from feedparser
    
    Returns:
    --------
    str
        Cleaned summary text
    """
    # Try different fields where the content might be
    if hasattr(entry, 'summary'):
        return clean_html(entry.summary)
    elif hasattr(entry, 'description'):
        return clean_html(entry.description)
    elif hasattr(entry, 'content'):
        for content in entry.content:
            if content.get('type') == 'text/html':
                return clean_html(content.value)
    
    return "No summary available."
