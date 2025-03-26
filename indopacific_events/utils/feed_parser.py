# utils/feed_parser.py
"""
Optimized and fixed version of feed parser with improved error handling 
for the Indo-Pacific Dashboard.
"""

import requests
import feedparser
import time
import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import ssl
import logging
import concurrent.futures
import streamlit as st
import traceback

# Get logger
logger = logging.getLogger("indo_pacific_dashboard")

# Disable SSL verification warnings for problematic sites
ssl._create_default_https_context = ssl._create_unverified_context

# Import text processor
from .text_processor import clean_html

# Import configuration if available
try:
    from data.rss_sources import FEED_CONFIG
except ImportError:
    # Default configuration if not available
    FEED_CONFIG = {
        "cache_ttl": 3600,  # Time (in seconds) to cache feeds
        "timeout": 15,      # HTTP request timeout in seconds
        "max_retries": 3,   # Maximum number of retry attempts
        "retry_delay": 2    # Delay between retries in seconds
    }
    logger.warning("Could not import FEED_CONFIG, using defaults")

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
    try:
        return fetch_rss_feeds(feed_list)
    except Exception as e:
        logger.error(f"Error in cached_fetch_rss_feeds: {str(e)}")
        # Return empty dict on error
        return {}

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
    
    # Check for empty input
    if not feed_list:
        logger.warning("Empty feed list provided to fetch_rss_feeds")
        return results
    
    try:
        # Use thread pool to fetch feeds in parallel but with fewer workers to avoid overloading
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            # Create a dictionary of future to source_name
            future_to_source = {
                executor.submit(fetch_single_feed, url): (url, source_name) 
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
                        # If no entries, log a warning
                        logger.warning(f"No entries found for {source_name} from {url}")
                except Exception as e:
                    # Log error instead of showing on UI
                    logger.error(f"Error fetching {source_name} from {url}: {str(e)}")
    except Exception as e:
        logger.error(f"Error in feed fetch thread pool: {str(e)}")
    
    return results

def fetch_single_feed(url):
    """
    Improved version of feed fetching with better error handling and longer timeouts.
    
    Parameters:
    -----------
    url : str
        URL of the RSS feed to fetch
    
    Returns:
    --------
    dict
        Processed feed data with entries
    """
    # Get configuration values
    max_retries = FEED_CONFIG.get("max_retries", 2)
    timeout = FEED_CONFIG.get("timeout", 10)
    retry_delay = FEED_CONFIG.get("retry_delay", 2)
    
    # Get domain for logging
    domain = urlparse(url).netloc
    
    # List of user agents to rotate between
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.56'
    ]
    
    for attempt in range(max_retries):
        try:
            # Get a random user agent from the list
            user_agent = user_agents[attempt % len(user_agents)]
            
            # Create request headers
            headers = {
                'User-Agent': user_agent,
                'Accept': 'application/rss+xml, application/xml, text/xml, application/atom+xml'
            }
            
            # Try direct approach with feedparser first (faster)
            feed = feedparser.parse(url, agent=user_agent)
            
            # Check if feed was successfully parsed and has entries
            if feed.entries:
                # Convert to a more easily serializable format
                entries = []
                for entry in feed.entries:
                    processed_entry = process_entry(entry)
                    entries.append(processed_entry)
                
                return {'entries': entries, 'status': getattr(feed, 'status', 200)}
            
            # If direct approach failed, try with requests as fallback
            try:
                # Disable SSL verification for problematic sites
                response = requests.get(url, headers=headers, timeout=timeout, verify=False)
                response.raise_for_status()
                feed = feedparser.parse(response.content)
                
                if feed.entries:
                    entries = []
                    for entry in feed.entries:
                        processed_entry = process_entry(entry)
                        entries.append(processed_entry)
                    
                    return {'entries': entries, 'status': response.status_code}
            except requests.exceptions.RequestException as re:
                logger.warning(f"Request to {domain} failed: {str(re)}")
                # Continue to next approach
            
            # If all methods failed, return empty feed
            logger.error(f"Failed to fetch feed from {domain} after all attempts")
            return {'entries': [], 'status': 0}
            
        except Exception as e:
            # Log error with trace
            logger.error(f"Error fetching feed from {domain}: {str(e)}")
            logger.debug(traceback.format_exc())
            
            # Check if we should retry
            if attempt < max_retries - 1:
                # More substantial delay between retries
                time.sleep(retry_delay)
                continue
            else:
                # Return empty feed on final error
                return {'entries': [], 'status': 0}
    
    # Should never reach here, but just in case
    return {'entries': [], 'status': 0}

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
    try:
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
            # Validate the time tuple before using it
            if isinstance(entry.published_parsed, time.struct_time) or (
                isinstance(entry.published_parsed, tuple) and len(entry.published_parsed) >= 6
            ):
                published = entry.published_parsed
            else:
                published = datetime.datetime.now().timetuple()
        elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
            if isinstance(entry.updated_parsed, time.struct_time) or (
                isinstance(entry.updated_parsed, tuple) and len(entry.updated_parsed) >= 6
            ):
                published = entry.updated_parsed
            else:
                published = datetime.datetime.now().timetuple()
        else:
            # If no date available, use current time
            published = datetime.datetime.now().timetuple()
        
        # Extract media/images
        media_content = []
        
        # Try multiple methods to find images
        try:
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
                        try:
                            soup = BeautifulSoup(content.value, 'html.parser')
                            img_tags = soup.find_all('img')
                            for img in img_tags:
                                if img.get('src'):
                                    media_content.append({'url': img.get('src')})
                                    break  # Just get the first image
                        except Exception as e:
                            logger.warning(f"Error parsing content HTML: {str(e)}")
            
            # Look in summary for images as last resort
            elif not media_content and hasattr(entry, 'summary'):
                try:
                    soup = BeautifulSoup(entry.summary, 'html.parser')
                    img_tags = soup.find_all('img')
                    for img in img_tags:
                        if img.get('src'):
                            media_content.append({'url': img.get('src')})
                            break  # Just get the first image
                except Exception as e:
                    logger.warning(f"Error parsing summary HTML: {str(e)}")
        except Exception as media_error:
            logger.warning(f"Error extracting media: {str(media_error)}")
            # Continue without media if there's an error

        return {
            'title': title,
            'link': link,
            'summary': summary,
            'published_parsed': published,
            'media_content': media_content
        }
        
    except Exception as e:
        logger.error(f"Error processing entry: {str(e)}")
        # Return minimal entry on error
        return {
            'title': getattr(entry, 'title', 'Error: Could not process entry'),
            'link': getattr(entry, 'link', ''),
            'summary': "Error processing this entry. The data may be malformed.",
            'published_parsed': datetime.datetime.now().timetuple(),
            'media_content': []
        }
