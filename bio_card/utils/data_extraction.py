import re
import nltk
from nltk.tokenize import sent_tokenize
import spacy

# Download necessary NLTK resources
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Initialize spaCy with error handling
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # If the model isn't installed, provide a more graceful error
    print("The spaCy model 'en_core_web_sm' is not installed. Installing now...")
    try:
        import subprocess
        subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"], check=True)
        nlp = spacy.load("en_core_web_sm")
        print("Model installed successfully.")
    except Exception as e:
        print(f"Failed to install spaCy model: {e}")
        # Fallback to a simple NLP object that won't cause crashes
        nlp = spacy.blank("en")
        print("Using blank model as fallback. Entity extraction will be limited.")

# Define regex patterns for various information types
PATTERNS = {
    'name': r'(?:^|\s)([A-Z][a-z]+(?:\s[A-Z][a-z]+){1,3})(?:$|\s)',
    'email': r'[\w\.-]+@[\w\.-]+\.\w+',
    'phone': r'(?:\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}',
    'date': r'(?:\d{1,2}[-/]\d{1,2}[-/]\d{2,4})|(?:\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b)',
    'address': r'\d{1,5}\s\w+\s\w+\.?(?:,\s[A-Za-z]+,\s[A-Z]{2}\s\d{5})?',
    'url': r'https?://(?:www\.)?[\w-]+\.[\w.-]+(?:/[\w-./?%&=]*)?',
    'amount': r'\$\s?[0-9,]+(?:\.\d{2})?',
    'linkedin': r'linkedin\.com/in/[\w-]+',
    'twitter': r'twitter\.com/[\w_]+',
    'facebook': r'facebook\.com/[\w.]+',
    'company': r'(?:at|with|for)\s([A-Z][a-zA-Z]*(?:\s[A-Z][a-zA-Z]*){0,5})'
}

def extract_entities(text):
    """
    Extract named entities from text using spaCy.
    
    Args:
        text (str): The text to analyze
    
    Returns:
        dict: Dictionary of entity types and their values
    """
    # Create default empty structure in case of errors
    entities = {
        'PERSON': [],
        'ORG': [],
        'GPE': [],  # Countries, cities, states
        'LOC': [],  # Non-GPE locations
        'DATE': [],
        'MONEY': []
    }
    
    try:
        doc = nlp(text)
        
        for ent in doc.ents:
            if ent.label_ in entities:
                if ent.text not in entities[ent.label_]:
                    entities[ent.label_].append(ent.text)
    except Exception as e:
        print(f"Error in entity extraction: {e}")
        # Return the empty entities dictionary if there was an error
    
    return entities

def extract_regex_matches(text):
    """
    Extract information using regex patterns.
    
    Args:
        text (str): The text to analyze
    
    Returns:
        dict: Dictionary of pattern types and their matches
    """
    matches = {}
    for key, pattern in PATTERNS.items():
        try:
            matches[key] = list(set(re.findall(pattern, text)))
        except Exception as e:
            print(f"Error in regex matching for {key}: {e}")
            matches[key] = []
    return matches

def get_sentences_with_entity(text, entity):
    """
    Find sentences containing a specific entity.
    
    Args:
        text (str): The text to search in
        entity (str): The entity to search for
    
    Returns:
        list: List of sentences containing the entity
    """
    try:
        sentences = sent_tokenize(text)
        matching_sentences = []
        
        for sentence in sentences:
            if re.search(r'\b' + re.escape(entity) + r'\b', sentence, re.IGNORECASE):
                matching_sentences.append(sentence)
        
        return matching_sentences
    except Exception as e:
        print(f"Error finding sentences with entity: {e}")
        return []

def identify_data_category(entity_type, entity, context=None):
    """
    Identify which profile category an entity belongs to.
    
    Args:
        entity_type (str): The type of entity or pattern
        entity (str): The actual entity value
        context (list, optional): List of sentences for context
    
    Returns:
        str: The category name
    """
    categories = {
        'PERSON': 'connections',
        'ORG': 'professional_background',
        'GPE': 'personal_info',
        'LOC': 'personal_info',
        'DATE': 'timeline',
        'MONEY': 'financial_info'
    }
    
    regex_categories = {
        'email': 'digital_footprint',
        'phone': 'personal_info',
        'address': 'personal_info',
        'url': 'digital_footprint',
        'linkedin': 'digital_footprint',
        'twitter': 'digital_footprint',
        'facebook': 'digital_footprint',
        'company': 'professional_background'
    }
    
    if entity_type in categories:
        return categories[entity_type]
    elif entity_type in regex_categories:
        return regex_categories[entity_type]
    else:
        return 'miscellaneous'
