# utils/feed_parser.py
"""
Utilities for fetching and processing RSS feeds for the Indo-Pacific Dashboard.
Modified to use logging instead of direct Streamlit warnings.
"""

import requests
import feedparser
import time
import datetime
from bs4 import BeautifulSoup
import random
from urllib.parse import urlparse
import ssl
import logging

# Import logging directly - since this file is imported after logger initialization
logger = logging.getLogger("indo_pacific_dashboard")

# Disable SSL verification warnings for problematic sites
ssl._create_default_https_context = ssl._create_unverified_context

# Import configuration
from data.rss_sources import FEED_CONFIG

def fetch_rss_feeds(feed_list):
    """
    Fetch RSS feeds from multiple sources with caching and error handling.
    Uses logging instead of direct Streamlit warnings.
    
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
            else:
                # Log warning instead of showing on UI
                logger.warning(f"No entries found for {source_name}")
        except Exception as e:
            # Log error instead of showing on UI
            logger.error(f"Error fetching {source_name}: {str(e)}")
    
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
    
    # List of user agents to rotate between
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    ]
    
    # Get domain from URL for request headers
    domain = urlparse(url).netloc
    
    for attempt in range(max_retries):
        try:
            # Get a random user agent
            user_agent = random.choice(user_agents)
            
            # Create request headers
            headers = {
                'User-Agent': user_agent,
                'Accept': 'application/rss+xml, application/xml, text/xml, application/atom+xml',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': f'https://{domain}/',
                'DNT': '1',
                'Cache-Control': 'max-age=0'
            }
            
            # Use requests or direct feedparser based on the attempt
            if attempt == 0:
                # First try with requests (more control)
                response = requests.get(url, headers=headers, timeout=timeout, verify=False)
                response.raise_for_status()
                feed = feedparser.parse(response.content)
            else:
                # Then try direct feedparser on retries
                feed = feedparser.parse(url, agent=user_agent)
            
            # Check if feed was successfully parsed
            if hasattr(feed, 'status') and feed.status != 200 and not feed.entries:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                else:
                    raise Exception(f"Failed to parse feed: Status {feed.status}")
            
            # Even without a status code, check if we got entries
            if not feed.entries:
                # Try to create a minimal mock feed for problematic sources
                if attempt == max_retries - 1:
                    return create_mock_feed(url, domain)
                else:
                    time.sleep(retry_delay)
                    continue
            
            # Convert to a more easily serializable format
            entries = []
            for entry in feed.entries:
                processed_entry = process_entry(entry)
                entries.append(processed_entry)
            
            if not entries:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                else:
                    return create_mock_feed(url, domain)
                
            return {'entries': entries, 'status': getattr(feed, 'status', 200)}
            
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            else:
                # Log the error instead of raising it
                logger.error(f"Failed to fetch {url} after {max_retries} attempts: {str(e)}")
                return create_mock_feed(url, domain)

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
