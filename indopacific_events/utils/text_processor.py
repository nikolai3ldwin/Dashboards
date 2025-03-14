# text_processor.py
"""
Utilities for processing text content in the Indo-Pacific Dashboard.
"""

import re
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist

# Download required NLTK data if not already present
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

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
    
    # Clean text
    clean_text = clean_html(text) if '<' in text and '>' in text else text
    
    # Tokenize the text
    tokens = word_tokenize(clean_text.lower())
    
    # Remove stopwords and short words
    stop_words = set(stopwords.words('english'))
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
        return tags

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
    
    # Clean text if it contains HTML
    clean_text = clean_html(text) if '<' in text and '>' in text else text
    
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', clean_text)
    
    if len(sentences) <= max_sentences:
        return clean_text
    
    # Simple extractive summarization - take first few sentences
    summary = ' '.join(sentences[:max_sentences])
    
    return summary
