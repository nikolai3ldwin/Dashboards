# utils/advanced_ner.py
"""
Advanced Named Entity Recognition and Relationship Extraction 
for the Indo-Pacific Dashboard using spaCy.
"""

import spacy
import re
from collections import defaultdict
import logging

# Set up logging
logger = logging.getLogger("indo_pacific_dashboard")

# Load the spaCy model - use a larger model for better accuracy
try:
    # Try to load a larger model if available
    nlp = spacy.load("en_core_web_lg")
    logger.info("Loaded en_core_web_lg model for advanced NER")
except OSError:
    try:
        # Fall back to medium model
        nlp = spacy.load("en_core_web_md")
        logger.info("Loaded en_core_web_md model for advanced NER")
    except OSError:
        # Fall back to small model as last resort
        nlp = spacy.load("en_core_web_sm")
        logger.info("Loaded en_core_web_sm model for advanced NER")

# Define a relationship pattern matcher
# This detects common phrases that indicate relationships between entities
def build_relationship_patterns():
    """Build patterns to detect relationships between entities"""
    return [
        {"label": "cooperation", "pattern": [{"LOWER": {"IN": ["cooperation", "partnership", "alliance", "agreement", "treaty", "deal", "pact"]}}]},
        {"label": "conflict", "pattern": [{"LOWER": {"IN": ["conflict", "tension", "dispute", "war", "battle", "fighting", "clash"]}}]},
        {"label": "economic", "pattern": [{"LOWER": {"IN": ["trade", "investment", "economic", "financial", "commerce", "business"]}}]},
        {"label": "diplomatic", "pattern": [{"LOWER": {"IN": ["diplomatic", "diplomacy", "embassy", "consulate", "ambassador", "envoy"]}}]},
        {"label": "military", "pattern": [{"LOWER": {"IN": ["military", "naval", "army", "defense", "security", "troops", "forces"]}}]},
    ]

def extract_entities_and_relationships(text):
    """
    Extract named entities and their relationships from text using spaCy
    
    Parameters:
    -----------
    text : str
        Text content to analyze
    
    Returns:
    --------
    dict
        Dictionary containing entities and relationships
    """
    if not text:
        return {"entities": [], "relationships": []}
    
    # Process the text with spaCy
    doc = nlp(text)
    
    # Extract entities
    entities = []
    for ent in doc.ents:
        if ent.label_ in ["GPE", "ORG", "NORP", "LOC", "FAC", "PERSON"]:
            entities.append({
                "text": ent.text,
                "type": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char
            })
    
    # Find relationships between entities
    relationships = []
    
    # Extract sentences with multiple entities
    sentences_with_entities = []
    for sent in doc.sents:
        sent_entities = [ent for ent in doc.ents if ent.start >= sent.start and ent.end <= sent.end]
        if len(sent_entities) >= 2:
            sentences_with_entities.append((sent, sent_entities))
    
    # Analyze relationships in each sentence
    for sent, sent_entities in sentences_with_entities:
        # Find relationship keywords in the sentence
        relationship_types = []
        for token in sent:
            if token.lower_ in ["cooperation", "partnership", "alliance", "agreement", "treaty"]:
                relationship_types.append("cooperation")
            elif token.lower_ in ["conflict", "tension", "dispute", "war", "clash"]:
                relationship_types.append("conflict")
            elif token.lower_ in ["trade", "investment", "economic", "financial"]:
                relationship_types.append("economic")
            elif token.lower_ in ["diplomatic", "diplomacy", "embassy", "talks"]:
                relationship_types.append("diplomatic")
            elif token.lower_ in ["military", "naval", "army", "defense", "weapons"]:
                relationship_types.append("military")
        
        # If no specific relationship found, mark as "mentioned"
        if not relationship_types:
            relationship_types = ["mentioned"]
        
        # Create relationship pairs between entities
        for i, entity1 in enumerate(sent_entities):
            if entity1.label_ not in ["GPE", "ORG", "NORP", "LOC"]:
                continue
                
            for j in range(i+1, len(sent_entities)):
                entity2 = sent_entities[j]
                if entity2.label_ not in ["GPE", "ORG", "NORP", "LOC"]:
                    continue
                
                # Create a relationship entry
                for rel_type in relationship_types:
                    relationships.append({
                        "source": entity1.text,
                        "source_type": entity1.label_,
                        "target": entity2.text,
                        "target_type": entity2.label_,
                        "type": rel_type,
                        "sentence": sent.text
                    })
    
    # Group the entities by type for easier display
    grouped_entities = defaultdict(list)
    for entity in entities:
        grouped_entities[entity["type"]].append(entity["text"])
    
    # Convert defaultdict to regular dict and remove duplicates
    grouped_entities = {k: list(set(v)) for k, v in grouped_entities.items()}
    
    # Group relationships by involved entities
    entity_relationships = defaultdict(list)
    for rel in relationships:
        key = f"{rel['source']}_{rel['target']}"
        entity_relationships[key].append(rel)
    
    # Take the most meaningful relationship if multiple exist
    consolidated_relationships = []
    for key, rels in entity_relationships.items():
        # Prioritize more specific relationships over "mentioned"
        specific_rels = [r for r in rels if r["type"] != "mentioned"]
        if specific_rels:
            consolidated_relationships.append(specific_rels[0])
        else:
            consolidated_relationships.append(rels[0])
    
    return {
        "entities": grouped_entities,
        "relationships": consolidated_relationships
    }

def analyze_entity_importance(text, entities_data):
    """
    Analyze which entities appear most prominently in the text
    
    Parameters:
    -----------
    text : str
        Text content to analyze
    entities_data : dict
        Dictionary of extracted entities and relationships
    
    Returns:
    --------
    dict
        Dictionary of entity importance scores
    """
    importance = defaultdict(int)
    
    # Count mentions of each entity
    for entity_type, entities in entities_data["entities"].items():
        for entity in entities:
            # Count occurrences, case-insensitive
            pattern = r'\b' + re.escape(entity) + r'\b'
            matches = re.findall(pattern, text, re.IGNORECASE)
            importance[entity] = len(matches)
    
    # Boost importance based on relationships
    for rel in entities_data["relationships"]:
        importance[rel["source"]] += 1
        importance[rel["target"]] += 1
    
    # Normalize to 0-10 scale if we have entities
    if importance:
        max_score = max(importance.values())
        if max_score > 0:
            for entity in importance:
                importance[entity] = round((importance[entity] / max_score) * 10)
    
    return dict(importance)

def analyze_article_content(text):
    """
    Perform comprehensive NER and relationship analysis on an article
    
    Parameters:
    -----------
    text : str
        Text content to analyze
    
    Returns:
    --------
    dict
        Dictionary containing entities, relationships, and importance scores
    """
    try:
        # Extract entities and relationships
        extraction_results = extract_entities_and_relationships(text)
        
        # Analyze entity importance
        importance_scores = analyze_entity_importance(text, extraction_results)
        
        # Add entity importance to results
        extraction_results["importance"] = importance_scores
        
        return extraction_results
    except Exception as e:
        logger.error(f"Error in advanced NER analysis: {str(e)}")
        return {"entities": {}, "relationships": [], "importance": {}}
