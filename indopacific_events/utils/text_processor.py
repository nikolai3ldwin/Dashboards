# utils/text_processor.py
"""
Fixed and improved utilities for processing text content in the Indo-Pacific Dashboard.
"""

import re
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import logging

# Get logger
logger = logging.getLogger("indo_pacific_dashboard")

# Download required NLTK data if not already present
def ensure_nltk_resources():
    """Download required NLTK resources if they don't exist."""
    resources = ['punkt', 'stopwords']
    
    for resource in resources:
        try:
            if not nltk.data.find(f'tokenizers/{resource}' if resource == 'punkt' else f'corpora/{resource}'):
                nltk.download(resource, quiet=True)
                logger.info(f"Downloaded NLTK resource: {resource}")
        except LookupError:
            try:
                nltk.download(resource, quiet=True)
                logger.info(f"Downloaded NLTK resource: {resource}")
            except Exception as e:
                logger.error(f"Failed to download NLTK resource {resource}: {str(e)}")
                # Continue without this resource

# Try to download resources but allow the app to continue if they fail
try:
    ensure_nltk_resources()
except Exception as e:
    logger.warning(f"Could not download NLTK resources: {str(e)}")

def clean_html(html_content):
    """
    Remove HTML tags and clean up text content.
    
    Parameters:
    -----------
    html_content : str
        HTML content to clean
    
    Returns:
    --------
    str
        Cleaned text content
    """
    if not html_content:
        return ""
    
    try:
        # Use BeautifulSoup to parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract text content
        text = soup.get_text(separator=' ', strip=True)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Fix common HTML entities
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&quot;', '"')
        text = text.replace('&#39;', "'")
        
        return text
    except Exception as e:
        logger.error(f"Error cleaning HTML: {str(e)}")
        # Return a safe version of the original content
        return re.sub(r'<[^>]*>', '', html_content)

def generate_tags(text, max_tags=5, min_word_length=4):
    """
    Generate relevant tags from text content using keyword frequency.
    
    Parameters:
    -----------
    text : str
        Text content to analyze
    max_tags : int
        Maximum number of tags to generate
    min_word_length : int
        Minimum word length to consider for tags
    
    Returns:
    --------
    list
        List of relevant tags
    """
    if not text:
        return []
    
    try:
        # Clean text
        clean_text = clean_html(text) if '<' in text and '>' in text else text
        
        # Make sure we have the necessary NLTK data
        ensure_nltk_resources()
        
        # Tokenize the text
        tokens = word_tokenize(clean_text.lower())
        
        # Get stopwords, handle potential error
        try:
            stop_words = set(stopwords.words('english'))
        except (LookupError, FileNotFoundError):
            # Fallback to a minimal set of stopwords if NLTK data isn't available
            stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'with', 'by'}
            logger.warning("Using fallback stopwords list - NLTK data not available")
        
        # Filter tokens
        filtered_tokens = [
            word for word in tokens 
            if word.isalpha() and 
            word not in stop_words and 
            len(word) >= min_word_length
        ]
        
        # Find most common words
        fdist = FreqDist(filtered_tokens)
        
        # Get most common words as tags
        tags = [word for word, _ in fdist.most_common(max_tags)]
        
        # Import keywords to check against if available
        try:
            from data.keywords import IMPORTANT_KEYWORDS
            # Prioritize keywords that exist in our predefined list
            important_tags = [
                word for word in filtered_tokens 
                if word in IMPORTANT_KEYWORDS
            ]
            # Combine important tags with frequency-based tags
            all_tags = list(set(important_tags + tags))
            return all_tags[:max_tags]
        except ImportError:
            # If keywords module not available, just use frequency-based tags
            logger.warning("Could not import IMPORTANT_KEYWORDS, using frequency-based tags only")
            return tags
    except Exception as e:
        logger.error(f"Error generating tags: {str(e)}")
        return []

def generate_summary(text, max_sentences=3):
    """
    Generate a concise summary from text content.
    
    Parameters:
    -----------
    text : str
        Text content to summarize
    max_sentences : int
        Maximum number of sentences in the summary
    
    Returns:
    --------
    str
        Summarized text
    """
    if not text:
        return ""
    
    try:
        # Clean text if it contains HTML
        clean_text = clean_html(text) if '<' in text and '>' in text else text
        
        # Split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', clean_text)
        
        if len(sentences) <= max_sentences:
            return clean_text
        
        # Simple extractive summarization - take first few sentences
        summary = ' '.join(sentences[:max_sentences])
        
        return summary
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        # Return truncated text as fallback
        if len(text) > 200:
            return text[:200] + "..."
        return text
