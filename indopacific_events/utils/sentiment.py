# utils/sentiment.py
"""
Enhanced sentiment analysis utilities for the Indo-Pacific Dashboard.
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
    
    # Key entities to track sentiment for - comprehensive list
    # of countries and regional actors in the Indo-Pacific
    key_entities = {
        'US': ['US', 'United States', 'America', 'Washington', 'Biden', 'Americans'],
        'China': ['China', 'Chinese', 'Beijing', 'CCP', 'Xi Jinping', 'PRC'],
        'Australia': ['Australia', 'Australian', 'Canberra', 'Albanese'],
        'Japan': ['Japan', 'Japanese', 'Tokyo', 'Kishida'],
        'India': ['India', 'Indian', 'New Delhi', 'Modi'],
        'Russia': ['Russia', 'Russian', 'Moscow', 'Putin'],
        'South Korea': ['South Korea', 'ROK', 'Seoul'],
        'North Korea': ['North Korea', 'DPRK', 'Pyongyang', 'Kim Jong Un'],
        'Taiwan': ['Taiwan', 'Taiwanese', 'Taipei'],
        'Philippines': ['Philippines', 'Filipino', 'Manila'],
        'Indonesia': ['Indonesia', 'Indonesian', 'Jakarta'],
        'Malaysia': ['Malaysia', 'Malaysian', 'Kuala Lumpur'],
        'Vietnam': ['Vietnam', 'Vietnamese', 'Hanoi'],
        'Thailand': ['Thailand', 'Thai', 'Bangkok'],
        'Singapore': ['Singapore', 'Singaporean'],
        'Cambodia': ['Cambodia', 'Cambodian', 'Phnom Penh'],
        'Myanmar': ['Myanmar', 'Burma', 'Burmese', 'Yangon', 'Naypyidaw'],
        'Laos': ['Laos', 'Lao', 'Vientiane'],
        'New Zealand': ['New Zealand', 'NZ', 'Wellington'],
        'Pakistan': ['Pakistan', 'Pakistani', 'Islamabad'],
        'Bangladesh': ['Bangladesh', 'Bangladeshi', 'Dhaka'],
        'Sri Lanka': ['Sri Lanka', 'Sri Lankan', 'Colombo'],
        'Nepal': ['Nepal', 'Nepalese', 'Kathmandu'],
        'Papua New Guinea': ['Papua New Guinea', 'PNG', 'Port Moresby'],
        'Fiji': ['Fiji', 'Fijian', 'Suva'],
        'Solomon Islands': ['Solomon Islands', 'Honiara'],
        'New Caledonia': ['New Caledonia', 'Nouméa'],
        'Wallis and Futuna': ['Wallis and Futuna', 'Wallis', 'Futuna'],
        'ASEAN': ['ASEAN', 'Association of Southeast Asian Nations', 'Southeast Asia', 'Southeast Asian'],
        'Pacific Islands': ['Pacific Islands', 'Pacific Island Countries', 'PIF', 'Forum', 'Pacific Forum']
    }
    
    # Pre-process the text
    text_lower = text.lower()
    
    # Initialize sentiment results
    sentiment_results = {}
    
    # Analyze overall sentiment first
    overall_sentiment = TextBlob(text).sentiment.polarity
    sentiment_results['Overall'] = round(overall_sentiment, 2)
    
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
    
    # Add regional sentiment if we have enough data
    if len(sentiment_results) > 2:  # If we have more than just Overall and one entity
        entity_scores = [score for entity, score in sentiment_results.items() if entity != 'Overall']
        if entity_scores:
            sentiment_results['Regional'] = round(sum(entity_scores) / len(entity_scores), 2)
    
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
