# sentiment.py
"""
Fixed sentiment analysis utilities for the Indo-Pacific Dashboard.
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
    
    try:
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
        try:
            blob = TextBlob(text)
            overall_sentiment = blob.sentiment.polarity
        except Exception as e:
            logger.warning(f"Error analyzing overall sentiment: {str(e)}")
            overall_sentiment = 0  # Neutral fallback
        
        # For each entity, analyze sentences containing references to it
        for entity, terms in key_entities.items():
            try:
                entity_sentences = []
                
                # Split text into sentences
                try:
                    sentences = re.split(r'(?<=[.!?])\s+', text)
                except Exception as e:
                    logger.warning(f"Error splitting sentences: {str(e)}")
                    sentences = [text]  # Fallback to whole text
                
                # Find sentences containing entity terms
                for sentence in sentences:
                    sentence_lower = sentence.lower()
                    if any(term.lower() in sentence_lower for term in terms):
                        entity_sentences.append(sentence)
                
                # If entity is mentioned, analyze sentiment for those sentences
                if entity_sentences:
                    # Calculate average sentiment
                    try:
                        entity_sentiment_values = []
                        for sentence in entity_sentences:
                            try:
                                sentence_blob = TextBlob(sentence)
                                entity_sentiment_values.append(sentence_blob.sentiment.polarity)
                            except Exception as sentence_error:
                                logger.warning(f"Error analyzing sentence sentiment: {str(sentence_error)}")
                                # Skip this sentence
                                continue
                                
                        # Only add result if we have valid sentiment values
                        if entity_sentiment_values:
                            entity_sentiment = sum(entity_sentiment_values) / len(entity_sentiment_values)
                            sentiment_results[entity] = round(entity_sentiment, 2)
                    except Exception as e:
                        logger.warning(f"Error calculating sentiment for {entity}: {str(e)}")
            except Exception as entity_error:
                logger.warning(f"Error processing entity {entity}: {str(entity_error)}")
                continue
        
        # Handle case where no entities were found
        if not sentiment_results:
            sentiment_results['Overall'] = round(overall_sentiment, 2)
        
        return sentiment_results
        
    except Exception as e:
        logger.error(f"Error in sentiment analysis: {str(e)}")
        # Return empty dict on error
        return {'Error': 0}
