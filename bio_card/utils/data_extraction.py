import re
import nltk
from nltk.tokenize import sent_tokenize

# Download necessary NLTK resources with error handling
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    try:
        nltk.download('punkt', quiet=True)
    except Exception as e:
        print(f"Warning: Could not download NLTK punkt resource: {e}")

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
    Simple entity extraction using regex patterns.
    
    Args:
        text (str): The text to analyze
    
    Returns:
        dict: Dictionary of entity types and their values
    """
    # Ensure input is a string
    if not isinstance(text, str):
        return {
            'PERSON': [],
            'ORG': [],
            'GPE': [],
            'LOC': [],
            'DATE': [],
            'MONEY': []
        }

    # Create a basic entity structure
    entities = {
        'PERSON': [],
        'ORG': [],
        'GPE': [],  # Countries, cities, states
        'LOC': [],  # Non-GPE locations
        'DATE': [],
        'MONEY': []
    }
    
    # Use regex to extract entities
    # Names (potential PERSON entities)
    name_pattern = r'\b[A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?\b'
    for match in re.finditer(name_pattern, text):
        if match.group() not in entities['PERSON']:
            entities['PERSON'].append(match.group())
    
    # Organizations (potential ORG entities)
    org_pattern = r'\b[A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]+)+\b'
    for match in re.finditer(org_pattern, text):
        # Exclude names that were already caught
        if match.group() not in entities['PERSON'] and match.group() not in entities['ORG']:
            entities['ORG'].append(match.group())
    
    # Dates
    date_pattern = r'\b(?:\d{1,2}[-/]\d{1,2}[-/]\d{2,4})|(?:(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4})\b'
    for match in re.finditer(date_pattern, text):
        if match.group() not in entities['DATE']:
            entities['DATE'].append(match.group())
    
    # Money amounts
    money_pattern = r'\$\s?[0-9,]+(?:\.\d{2})?'
    for match in re.finditer(money_pattern, text):
        if match.group() not in entities['MONEY']:
            entities['MONEY'].append(match.group())
    
    # Cities, states, countries (GPE)
    locations = [
        "New York", "Los Angeles", "Chicago", "San Francisco", "Seattle", "Boston", "Washington DC",
        "California", "Texas", "Florida", "Illinois", "New York", "Pennsylvania", "Ohio", "Georgia",
        "USA", "United States", "Canada", "Mexico", "UK", "England", "France", "Germany", "Japan", "China"
    ]
    
    for location in locations:
        if re.search(r'\b' + re.escape(location) + r'\b', text):
            if location not in entities['GPE']:
                entities['GPE'].append(location)
    
    return entities

def extract_regex_matches(text):
    """
    Extract information using regex patterns.
    
    Args:
        text (str): The text to analyze
    
    Returns:
        dict: Dictionary of pattern types and their matches
    """
    # Ensure input is a string
    if not isinstance(text, str):
        return {}

    matches = {}
    for key, pattern in PATTERNS.items():
        try:
            # Use set to remove duplicates, convert to list
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
    # Ensure inputs are strings
    if not isinstance(text, str) or not isinstance(entity, str):
        return []

    try:
        # Tokenize text into sentences
        sentences = sent_tokenize(text)
        
        # Find sentences containing the entity
        matching_sentences = [
            sentence for sentence in sentences 
            if re.search(r'\b' + re.escape(entity) + r'\b', sentence, re.IGNORECASE)
        ]
        
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
    # Static mapping for entity types
    categories = {
        'PERSON': 'connections',
        'ORG': 'professional_background',
        'GPE': 'personal_info',
        'LOC': 'personal_info',
        'DATE': 'timeline',
        'MONEY': 'financial_info'
    }
    
    # Static mapping for regex pattern types
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
    
    # Check entity types first
    if entity_type in categories:
        return categories[entity_type]
    
    # Then check regex pattern types
    if entity_type in regex_categories:
        return regex_categories[entity_type]
    
    # Fallback for unknown types
    return 'inconsistencies'
