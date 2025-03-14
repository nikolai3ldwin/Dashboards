# utils/feed_parser.py
"""
Optimized version of feed parser with faster handling of feed errors.
"""

import streamlit as st  # Import Streamlit at the top
import requests
import feedparser
import time
import datetime
from bs4 import BeautifulSoup
import random
from urllib.parse import urlparse
import ssl
import logging
import concurrent.futures

# Import logging directly - since this file is imported after logger initialization
logger = logging.getLogger("indo_pacific_dashboard")

# Disable SSL verification warnings for problematic sites
ssl._create_default_https_context = ssl._create_unverified_context

# Import text processor
from .text_processor import clean_html

# Import configuration
from data.rss_sources import FEED_CONFIG

# Create an in-memory cache for mock feeds to avoid recreating them
_mock_feed_cache = {}

@st.cache_data(ttl=3600)  # Cache for 1 hour
def cached_fetch_rss_feeds(feed_list):
    """
    Cached version of fetch_rss_feeds for improved performance.
    
    Parameters:
    -----------
    feed_list : list
        List of (url, source_name) tuples
    
    Returns:
    --------
    dict
        Dictionary mapping source names to processed feed data
    """
    return fetch_rss_feeds(feed_list)

def fetch_rss_feeds(feed_list):
    """
    Fetch RSS feeds from multiple sources with parallel processing.
    
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
    
    # Use thread pool to fetch feeds in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Create a dictionary of future to source_name
        future_to_source = {
            executor.submit(fetch_single_feed_fast, url): (url, source_name) 
            for url, source_name in feed_list
        }
        
        # Process results as they complete
        for future in concurrent.futures.as_completed(future_to_source):
            url, source_name = future_to_source[future]
            try:
                feed_data = future.result()
                if feed_data and feed_data.get('entries'):
                    results[source_name] = feed_data
                else:
                    # If no entries and not already logged, log a warning
                    if not feed_data.get('is_mock', False):
                        logger.warning(f"No entries found for {source_name}")
            except Exception as e:
                # Log error instead of showing on UI
                logger.error(f"Error fetching {source_name}: {str(e)}")
    
    return results

def fetch_single_feed_fast(url):
    """
    Faster version of feed fetching with reduced retries and timeouts.
    
    Parameters:
    -----------
    url : str
        URL of the RSS feed to fetch
    
    Returns:
    --------
    dict
        Processed feed data with entries
    """
    max_retries = 1  # Reduced retries for speed
    timeout = 5  # Reduced timeout for speed
    domain = urlparse(url).netloc
    
    # Check if we have a mock feed already cached
    cache_key = f"mock_{domain}"
    if url in _mock_feed_cache:
        return _mock_feed_cache[url]
    
    # List of user agents to rotate between
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    ]
    
    for attempt in range(max_retries):
        try:
            # Get a random user agent
            user_agent = random.choice(user_agents)
            
            # Create request headers
            headers = {
                'User-Agent': user_agent,
                'Accept': 'application/rss+xml, application/xml, text/xml, application/atom+xml'
            }
            
            # Direct approach first (faster)
            feed = feedparser.parse(url, agent=user_agent)
            
            # Check if feed was successfully parsed and has entries
            if feed.entries:
                # Convert to a more easily serializable format
                entries = []
                for entry in feed.entries:
                    processed_entry = process_entry(entry)
                    entries.append(processed_entry)
                
                return {'entries': entries, 'status': getattr(feed, 'status', 200)}
            
            # If we got here, feeding parsing failed - try with requests as fallback
            try:
                response = requests.get(url, headers=headers, timeout=timeout, verify=False)
                response.raise_for_status()
                feed = feedparser.parse(response.content)
                
                if feed.entries:
                    entries = []
                    for entry in feed.entries:
                        processed_entry = process_entry(entry)
                        entries.append(processed_entry)
                    
                    return {'entries': entries, 'status': response.status_code}
            except:
                pass
            
            # If all methods failed, create a mock feed
            mock_feed = create_mock_feed(url, domain)
            _mock_feed_cache[url] = mock_feed  # Cache the mock feed
            return mock_feed
            
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(0.5)  # Brief delay between retries
                continue
            else:
                # Create and cache a mock feed
                mock_feed = create_mock_feed(url, domain)
                _mock_feed_cache[url] = mock_feed
                return mock_feed

def create_mock_feed(url, domain):
    """
    Creates a minimal mock feed for problematic sources
    to allow the dashboard to function.
    """
    current_time = datetime.datetime.now()
    mock_entry = {
        'title': f"Unable to fetch content from {domain}",
        'link': url,
        'summary': f"This is a placeholder entry. The RSS feed at {url} could not be accessed.",
        'published_parsed': current_time.timetuple(),
        'media_content': []
    }
    
    # Log the mock feed creation instead of displaying it
    logger.warning(f"Created mock feed for {domain} as feed was unavailable")
    
    return {'entries': [mock_entry], 'status': 0, 'is_mock': True}

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
    title = getattr(entry, 'title', 'No Title')
    link = getattr(entry, 'link', '')
    
    # Handle summary/description/content with fallbacks
    summary = ''
    if hasattr(entry, 'summary'):
        summary = entry.summary
    elif hasattr(entry, 'description'):
        summary = entry.description
    elif hasattr(entry, 'content'):
        for content in entry.content:
            if content.get('type') == 'text/html':
                summary = content.value
                break
    
    # Clean the summary
    summary = clean_html(summary) if summary else "No summary available."
    
    # Handle published date with fallbacks
    published = None
    if hasattr(entry, 'published_parsed') and entry.published_parsed:
        published = entry.published_parsed
    elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
        published = entry.updated_parsed
    else:
        # If no date available, use current time
        published = datetime.datetime.now().timetuple()
    
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
