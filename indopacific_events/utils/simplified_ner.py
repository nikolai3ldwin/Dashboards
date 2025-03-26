# utils/simplified_ner.py
"""
Simplified Named Entity Recognition for the Indo-Pacific Dashboard.
Uses basic text analysis techniques to identify entities without complex dependencies.
"""

import re
import logging
from collections import defaultdict

# Configure logging
logger = logging.getLogger("indo_pacific_dashboard")

# Try to import NLTK, but don't require it
try:
    import nltk
    from nltk.tokenize import word_tokenize
    nltk_available = True
    
    # Download required NLTK data
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        try:
            nltk.download('punkt', quiet=True)
        except:
            pass
except ImportError:
    nltk_available = False
    logger.info("NLTK not available, using regex-only entity extraction")

def extract_entities(text):
    """
    Extract named entities using regular expressions and simple rules.
    
    Parameters:
    -----------
    text : str
        Text content to analyze
    
    Returns:
    --------
    dict
        Dictionary of entity types to lists of entities
    """
    if not text:
        return {}
    
    # Initialize entity dictionary
    entities = {
        "GPE": [],       # Countries, cities, locations
        "ORG": [],       # Organizations
        "PERSON": [],    # People's names
        "NORP": []       # Nationalities or religious/political groups
    }
    
    # Convert text to lowercase for case-insensitive matching
    text_lower = text.lower()
    
    # Countries and territories in the Indo-Pacific region
    countries = [
        "China", "United States", "USA", "US", "Japan", "Australia", "India",
        "Indonesia", "Philippines", "Malaysia", "Vietnam", "Thailand", "Myanmar",
        "Cambodia", "Laos", "Singapore", "South Korea", "North Korea", "Taiwan",
        "New Zealand", "Fiji", "Papua New Guinea", "Solomon Islands", "Vanuatu",
        "Samoa", "Tonga", "New Caledonia", "Wallis and Futuna", "Pacific Islands"
    ]
    
    # Organizations relevant to the region
    organizations = [
        "ASEAN", "United Nations", "UN", "European Union", "EU", "NATO",
        "Pentagon", "State Department", "White House", "Ministry of Defense",
        "Ministry of Foreign Affairs", "WHO", "World Bank", "IMF", "WTO"
    ]
    
    # Political/nationality groups
    groups = [
        "Chinese", "American", "Japanese", "Australian", "Indian", "Indonesian",
        "Filipino", "Malaysian", "Vietnamese", "Thai", "Burmese", "Cambodian",
        "Laotian", "Singaporean", "Korean", "Taiwanese", "Pacific Islander"
    ]
    
    # Extract countries
    for country in countries:
        if country.lower() in text_lower:
            if country not in entities["GPE"]:
                entities["GPE"].append(country)
    
    # Extract organizations
    for org in organizations:
        if org.lower() in text_lower:
            if org not in entities["ORG"]:
                entities["ORG"].append(org)
    
    # Extract nationality/political groups
    for group in groups:
        if group.lower() in text_lower:
            if group not in entities["NORP"]:
                entities["NORP"].append(group)
    
    # Use regex to find potential person names (if they appear with titles or in typical contexts)
    person_patterns = [
        r'President\s+([A-Z][a-z]+\s+[A-Z][a-z]+)',
        r'Prime Minister\s+([A-Z][a-z]+\s+[A-Z][a-z]+)',
        r'Foreign Minister\s+([A-Z][a-z]+\s+[A-Z][a-z]+)',
        r'Secretary\s+([A-Z][a-z]+\s+[A-Z][a-z]+)',
        r'General\s+([A-Z][a-z]+\s+[A-Z][a-z]+)',
        r'Admiral\s+([A-Z][a-z]+\s+[A-Z][a-z]+)'
    ]
    
    for pattern in person_patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            person_name = match.group(1)
            if person_name not in entities["PERSON"]:
                entities["PERSON"].append(person_name)
    
    # Only return non-empty entity types
    return {k: v for k, v in entities.items() if v}

def identify_relationships(text, entities):
    """
    Identify simple relationships between entities in the text.
    
    Parameters:
    -----------
    text : str
        Text content to analyze
    entities : dict
        Dictionary of entities by type
    
    Returns:
    --------
    list
        List of relationship dictionaries
    """
    relationships = []
    
    # Skip if no entities or insufficient entities for relationships
    flattened_entities = []
    for entity_list in entities.values():
        flattened_entities.extend(entity_list)
    
    if len(flattened_entities) < 2:
        return relationships
    
    # Define relationship keywords
    relation_patterns = {
        "cooperation": ["cooperation", "agreement", "partnership", "alliance", "deal", "treaty"],
        "conflict": ["conflict", "tension", "dispute", "war", "confrontation", "clash"],
        "economic": ["trade", "investment", "economic", "financial", "commerce"],
        "diplomatic": ["diplomatic", "diplomacy", "talks", "negotiation", "meeting"],
        "military": ["military", "defense", "security", "naval", "army", "forces"]
    }
    
    # Check each pair of entities for co-occurrence in sentences with relationship words
    sentences = text.split('.')
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        
        # Check which entities appear in the sentence
        entities_in_sentence = []
        for entity_type, entity_list in entities.items():
            for entity in entity_list:
                if entity in sentence:
                    entities_in_sentence.append((entity, entity_type))
        
        # Skip if fewer than 2 entities
        if len(entities_in_sentence) < 2:
            continue
        
        # Find relationship type in sentence
        relation_type = "mentioned"
        for rel_type, keywords in relation_patterns.items():
            if any(keyword in sentence.lower() for keyword in keywords):
                relation_type = rel_type
                break
        
        # Create relationships between all pairs of entities in the sentence
        for i, (entity1, type1) in enumerate(entities_in_sentence):
            for entity2, type2 in entities_in_sentence[i+1:]:
                relationships.append({
                    "source": entity1,
                    "source_type": type1,
                    "target": entity2,
                    "target_type": type2,
                    "type": relation_type,
                    "sentence": sentence
                })
    
    # Remove duplicate relationships by converting to a dict and back
    unique_relationships = {}
    for rel in relationships:
        key = f"{rel['source']}_{rel['target']}_{rel['type']}"
        unique_relationships[key] = rel
    
    return list(unique_relationships.values())

def analyze_article_content(text):
    """
    Analyze article content for entities and their relationships.
    
    Parameters:
    -----------
    text : str
        Text content to analyze
    
    Returns:
    --------
    dict
        Dictionary containing entities and relationships
    """
    try:
        # Extract entities
        extracted_entities = extract_entities(text)
        
        # Identify relationships between entities
        relationships = identify_relationships(text, extracted_entities)
        
        # Calculate basic entity importance (frequency-based)
        entity_importance = {}
        for entity_type, entities in extracted_entities.items():
            for entity in entities:
                entity_importance[entity] = text.lower().count(entity.lower())
        
        return {
            "entities": extracted_entities,
            "relationships": relationships,
            "importance": entity_importance
        }
    except Exception as e:
        logger.error(f"Error in simplified NER analysis: {str(e)}")
        return {"entities": {}, "relationships": [], "importance": {}}
