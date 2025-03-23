# components/article_card_with_ner.py
"""
Component for displaying articles with named entity and relationship visualization 
in the Indo-Pacific Dashboard.
"""

import streamlit as st
from PIL import Image
import hashlib
import re

# Use our advanced NER functionality
from utils.advanced_ner import analyze_article_content

def display_article_with_ner(article, image):
    """
    Display an article card with named entity recognition and relationship visualization.
    
    Parameters:
    -----------
    article : dict
        Article data dictionary containing title, date, summary, etc.
    image : PIL.Image
        Image to display with the article
    """
    # Create a card with a border
    with st.container():
        st.markdown("---")
        
        # Two-column layout
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Display the image
            st.image(image, use_column_width=True)
            
            # Display importance rating with stars
            importance_stars = "⭐" * article['importance']
            st.markdown(f"**Importance:** {importance_stars}")
            
            # Display source and date
            st.markdown(f"**Source:** {article['source']}")
            st.markdown(f"**Date:** {article['date'].strftime('%Y-%m-%d %H:%M')}")
            
            # Display categories
            if article.get('categories'):
                st.markdown("**Categories:**")
                for category, count in article['categories'].items():
                    st.markdown(f"- {category}: {count} mentions")
        
        with col2:
            # Article title as link
            st.markdown(f"## [{article['title']}]({article['link']})")
            
            # Summary
            st.markdown(f"{article['summary']}")
            
            # Always display tags directly
            if article.get('tags'):
                st.markdown("**Tags:** " + ", ".join(article['tags']))
            
            # Perform NER analysis on the full text (summary if full text unavailable)
            text_for_analysis = article.get('full_text', article['summary'])
            ner_results = analyze_article_content(text_for_analysis)
            
            # Display entities found if any
            if ner_results['entities']:
                st.markdown("**Named Entities:**")
                
                # Display each entity type in a clean format
                entity_display = ""
                for entity_type, entities in ner_results['entities'].items():
                    # Use friendly names for entity types
                    type_names = {
                        "GPE": "Countries/Cities",
                        "ORG": "Organizations",
                        "PERSON": "People",
                        "NORP": "Nationalities/Groups",
                        "LOC": "Locations",
                        "FAC": "Facilities"
                    }
                    
                    friendly_name = type_names.get(entity_type, entity_type)
                    entity_display += f"- **{friendly_name}**: {', '.join(entities)}\n"
                
                st.markdown(entity_display)
            
            # Display entity relationships if any
            if ner_results['relationships']:
                st.markdown("**Entity Relationships:**")
                
                # Create a more visual representation of relationships
                for rel in ner_results['relationships']:
                    # Determine color based on relationship type
                    color = "#1E88E5" if rel['type'] == "cooperation" else \
                           "#D81B60" if rel['type'] == "conflict" else \
                           "#FFC107" if rel['type'] == "economic" else \
                           "#673AB7" if rel['type'] == "diplomatic" else \
                           "#4CAF50" if rel['type'] == "military" else \
                           "#9E9E9E"
                    
                    # Create relationship indicator
                    st.markdown(
                        f"""
                        <div style="margin-bottom: 8px;">
                            <span style="font-weight: bold; color: #555;">{rel['source']}</span>
                            <span style="color: {color}; padding: 2px 6px; margin: 0 6px; border-radius: 3px; font-size: 0.8em; font-weight: bold; background-color: rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.1);">
                                {rel['type'].upper()}
                            </span>
                            <span style="font-weight: bold; color: #555;">{rel['target']}</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
            # Always display sentiment analysis directly
            if article.get('sentiment'):
                st.markdown("**Sentiment Analysis:**")
                
                # Create a horizontal bar chart for sentiment
                for entity, score in article['sentiment'].items():
                    # Determine color based on sentiment
                    color = "green" if score > 0 else "red" if score < 0 else "gray"
                    
                    # Calculate width percentage (convert -1 to 1 scale to 0-100%)
                    width = abs(score) * 50  # 50% is neutral
                    
                    # Display horizontal bar
                    st.markdown(
                        f"""
                        <div style="display: flex; align-items: center; margin-bottom: 5px;">
                            <div style="width: 80px;">{entity}:</div>
                            <div style="background-color: {color}; width: {width}%; 
                                        height: 15px; border-radius: 3px;"></div>
                            <div style="margin-left: 10px;">{score:.2f}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
            # Call to action buttons
            col_a, col_b, col_c = st.columns(3)
            
            # Create a unique key for each button based on multiple properties
            unique_key = hashlib.md5(
                f"{article['title']}{article['link']}{str(article['date'])}{article['source']}".encode()
            ).hexdigest()[:12]
            
            with col_a:
                st.button("Read Full Article", 
                          key=f"read_{unique_key}", 
                          help=f"Open {article['link']}")
            with col_b:
                st.button("Save for Later", 
                          key=f"save_{unique_key}", 
                          help="Save this article to your reading list")
            with col_c:
                st.button("Share", 
                          key=f"share_{unique_key}", 
                          help="Share this article")
