# sentiment.py
"""
Sentiment analysis utilities for the Indo-Pacific Dashboard.
"""

import nltk
from textblob import TextBlob
import re

# Download required NLTK data if not already present
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def analyze_sentiment(text):
    """
    Analyze sentiment in text content with a focus on key regional actors.
    
    Parameters:
    -----------
    text : str
        Text content to analyze
    
    Returns:
    --------
    dict
        Dictionary mapping entities to sentiment scores (-1 to 1)
    """
    if not text:
        return {}
    
    # Key entities to track sentiment for
    key_entities = {
        'US': ['US', 'United States', 'America', 'Washington', 'Biden', 'Americans'],
        'China': ['China', 'Chinese', 'Beijing', 'CCP', 'Xi Jinping', 'PRC'],
        'Australia': ['Australia', 'Australian', 'Canberra', 'Albanese'],
        'Japan': ['Japan', 'Japanese', 'Tokyo', 'Kishida'],
        'India': ['India', 'Indian', 'New Delhi', 'Modi'],
        'ASEAN': ['ASEAN', 'Southeast Asia', 'Southeast Asian'],
        'Pacific Islands': ['Pacific Islands', 'Pacific Island Countries', 'PIF', 'Forum']
    }
    
    # Pre-process the text
    text_lower = text.lower()
    
    # Initialize sentiment results
    sentiment_results = {}
    
    # Analyze overall sentiment
    overall_sentiment = TextBlob(text).sentiment.polarity
    
    # For each entity, analyze sentences containing references to it
    for entity, terms in key_entities.items():
        entity_sentences = []
        
        # Split text into sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        # Find sentences containing entity terms
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(term.lower() in sentence_lower for term in terms):
                entity_sentences.append(sentence)
        
        # If entity is mentioned, analyze sentiment for those sentences
        if entity_sentences:
            entity_sentiment = sum(TextBlob(sentence).sentiment.polarity for sentence in entity_sentences) / len(entity_sentences)
            sentiment_results[entity] = round(entity_sentiment, 2)
        else:
            # If not mentioned, don't include in results
            pass
    
    # Handle case where no entities were found
    if not sentiment_results:
        sentiment_results['Overall'] = round(overall_sentiment, 2)
    
    return sentiment_results

def get_sentiment_color(score):
    """
    Get a color representation based on sentiment score.
    
    Parameters:
    -----------
    score : float
        Sentiment score from -1 (negative) to 1 (positive)
    
    Returns:
    --------
    str
        Hex color code
    """
    if score > 0.5:
        return "#28a745"  # Strong positive - green
    elif score > 0:
        return "#a3cfbb"  # Weak positive - light green
    elif score == 0:
        return "#6c757d"  # Neutral - gray
    elif score > -0.5:
        return "#f8d7da"  # Weak negative - light red
    else:
        return "#dc3545"  # Strong negative - red

def get_sentiment_label(score):
    """
    Get a text label based on sentiment score.
    
    Parameters:
    -----------
    score : float
        Sentiment score from -1 (negative) to 1 (positive)
    
    Returns:
    --------
    str
        Sentiment label
    """
    if score > 0.5:
        return "Very Positive"
    elif score > 0:
        return "Somewhat Positive"
    elif score == 0:
        return "Neutral"
    elif score > -0.5:
        return "Somewhat Negative"
    else:
        return "Very Negative"

def analyze_entity_relations(text):
    """
    Advanced analysis of entity relationships in text.
    
    Parameters:
    -----------
    text : str
        Text content to analyze
    
    Returns:
    --------
    dict
        Dictionary mapping entity pairs to relationship sentiment
    """
    # This is a placeholder for more advanced analysis
    # In a real implementation, you might use NER and relationship extraction
    
    # For now, return an empty dict
    return {}
