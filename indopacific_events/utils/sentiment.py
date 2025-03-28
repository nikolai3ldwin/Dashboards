# utils/sentiment.py
"""
Enhanced sentiment analysis utilities for the Indo-Pacific Dashboard.
"""

import nltk
from textblob import TextBlob
import re
import logging

# Get logger
logger = logging.getLogger("indo_pacific_dashboard")

# Download required NLTK data if not already present
def ensure_nltk_resources():
    """Download required NLTK resources if they don't exist."""
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        try:
            nltk.download('punkt', quiet=True)
            logger.info("Downloaded NLTK punkt tokenizer")
        except Exception as e:
            logger.error(f"Failed to download NLTK punkt: {str(e)}")

# Try to download resources but allow the app to continue if they fail
try:
    ensure_nltk_resources()
except Exception as e:
    logger.warning(f"Could not download NLTK resources: {str(e)}")

def analyze_sentiment(text):
    """
    Analyze sentiment in text content with a focus on all regional actors mentioned.
    
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
    
    try:
        # List of countries and entities to detect
        countries = [
            'United States', 'US', 'China', 'Japan', 'India', 'Australia', 
            'South Korea', 'North Korea', 'Taiwan', 'Indonesia', 'Vietnam',
            'Philippines', 'Malaysia', 'Singapore', 'Thailand', 'Myanmar',
            'Cambodia', 'Laos', 'Papua New Guinea', 'Fiji', 'Solomon Islands',
            'Vanuatu', 'New Caledonia', 'Wallis and Futuna', 'Russia'
        ]
        
        # Simplified country names for results
        country_mapping = {
            'United States': 'US',
            'North Korea': 'N. Korea',
            'South Korea': 'S. Korea',
            'Papua New Guinea': 'PNG',
            'Solomon Islands': 'Solomon Is.'
        }
        
        # Find which countries are mentioned in the text
        mentioned_countries = []
        text_lower = text.lower()
        
        for country in countries:
            if country.lower() in text_lower:
                # Use simplified name if available
                country_name = country_mapping.get(country, country)
                mentioned_countries.append(country_name)
        
        sentiment_results = {}
        
        # Only analyze sentiment for countries that are mentioned
        for country in set(mentioned_countries):
            # Find sentences mentioning this country
            sentences = re.split(r'(?<=[.!?])\s+', text)
            country_sentences = []
            
            for sentence in sentences:
                # Check for country or related terms
                country_lower = country.lower()
                sentence_lower = sentence.lower()
                
                # Get the original country name from mapping if needed
                original_countries = [k for k, v in country_mapping.items() if v == country]
                check_names = [country_lower] + [c.lower() for c in original_countries]
                
                if any(name in sentence_lower for name in check_names):
                    country_sentences.append(sentence)
            
            # Only calculate sentiment if we found sentences
            if country_sentences:
                try:
                    # Calculate sentiment for this country
                    scores = []
                    for sentence in country_sentences:
                        blob = TextBlob(sentence)
                        scores.append(blob.sentiment.polarity)
                    
                    # Average sentiment
                    if scores:
                        sentiment_results[country] = round(sum(scores) / len(scores), 2)
                except Exception as e:
                    logger.warning(f"Error calculating sentiment for {country}: {str(e)}")
        
        # If no country-specific sentiments found, calculate overall sentiment
        if not sentiment_results:
            try:
                blob = TextBlob(text)
                overall_sentiment = blob.sentiment.polarity
                sentiment_results['Overall'] = round(overall_sentiment, 2)
            except Exception as e:
                logger.warning(f"Error analyzing overall sentiment: {str(e)}")
        
        return sentiment_results
        
    except Exception as e:
        logger.error(f"Error in sentiment analysis: {str(e)}")
        # Return empty dict on error
        return {'Error': 0}
