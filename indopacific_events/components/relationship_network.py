# components/relationship_network.py
"""
Component for displaying entity relationship network visualization 
in the Indo-Pacific Dashboard.
"""

import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import io

def create_relationship_network(all_articles):
    """
    Create a network visualization of entity relationships across all articles.
    
    Parameters:
    -----------
    all_articles : list
        List of article dictionaries with NER analysis results
    
    Returns:
    --------
    matplotlib.figure.Figure
        Network visualization figure
    """
    # Extract relationship data from all articles
    relationships = []
    
    # First, process each article to get NER data if not already present
    from utils.advanced_ner import analyze_article_content
    
    for article in all_articles:
        # Skip if no summary is available
        if not article.get('summary'):
            continue
            
        # Use the full text if available, otherwise use the summary
        text_for_analysis = article.get('full_text', article['summary'])
        
        # If NER analysis is already in the article data, use it
        # Otherwise, perform the analysis now
        if article.get('ner_data'):
            ner_results = article['ner_data']
        else:
            ner_results = analyze_article_content(text_for_analysis)
            
        # Add relationships to our list
        for rel in ner_results.get('relationships', []):
            relationships.append({
                'source': rel['source'],
                'target': rel['target'],
                'type': rel['type'],
                'article_title': article['title'],
                'article_date': article['date']
            })
    
    # If no relationships found, return None
    if not relationships:
        return None
        
    # Create a directed graph
    G = nx.DiGraph()
    
    # Add nodes and edges to the graph
    for rel in relationships:
        # Add nodes if they don't exist
        if not G.has_node(rel['source']):
            G.add_node(rel['source'])
        if not G.has_node(rel['target']):
            G.add_node(rel['target'])
            
        # Add edge with type as attribute
        if G.has_edge(rel['source'], rel['target']):
            # If edge already exists, update the weight and types
            G[rel['source']][rel['target']]['weight'] += 1
            if rel['type'] not in G[rel['source']][rel['target']]['types']:
                G[rel['source']][rel['target']]['types'].append(rel['type'])
        else:
            # Create new edge
            G.add_edge(
                rel['source'], 
                rel['target'], 
                weight=1, 
                types=[rel['type']]
            )
    
    # Calculate node sizes based on degree centrality
    centrality = nx.degree_centrality(G)
    node_sizes = [centrality[node] * 1000 + 100 for node in G.nodes()]
    
    # Determine edge colors based on relationship type
    edge_colors = []
    for u, v, data in G.edges(data=True):
        # Use the first type in the list for color
        primary_type = data['types'][0]
        if primary_type == "cooperation":
            edge_colors.append('#1E88E5')  # Blue
        elif primary_type == "conflict":
            edge_colors.append('#D81B60')  # Red
        elif primary_type == "economic":
            edge_colors.append('#FFC107')  # Yellow
        elif primary_type == "diplomatic":
            edge_colors.append('#673AB7')  # Purple
        elif primary_type == "military":
            edge_colors.append('#4CAF50')  # Green
        else:
            edge_colors.append('#9E9E9E')  # Gray
    
    # Create a figure
    plt.figure(figsize=(12, 8))
    
    # Use a better layout algorithm for directed graphs
    pos = nx.spring_layout(G, seed=42, k=0.3)
    
    # Draw nodes
    nx.draw_networkx_nodes(
        G, 
        pos, 
        node_size=node_sizes,
        node_color='#B3E5FC',  # Light blue
        edgecolors='#0288D1',  # Darker blue
        alpha=0.8
    )
    
    # Draw edges with arrows
    nx.draw_networkx_edges(
        G, 
        pos, 
        width=[G[u][v]['weight'] for u, v in G.edges()],
        edge_color=edge_colors,
        alpha=0.7,
        arrowsize=15,
        arrowstyle='->'
    )
    
    # Draw labels with better font
    nx.draw_networkx_labels(
        G, 
        pos, 
        font_size=10,
        font_family='sans-serif',
        font_weight='bold'
    )
    
    # Add a title
    plt.title("Entity Relationship Network", fontsize=16)
    
    # Add a legend
    legend_elements = [
        plt.Line2D([0], [0], color='#1E88E5', lw=2, label='Cooperation'),
        plt.Line2D([0], [0], color='#D81B60', lw=2, label='Conflict'),
        plt.Line2D([0], [0], color='#FFC107', lw=2, label='Economic'),
        plt.Line2D([0], [0], color='#673AB7', lw=2, label='Diplomatic'),
        plt.Line2D([0], [0], color='#4CAF50', lw=2, label='Military'),
        plt.Line2D([0], [0], color='#9E9E9E', lw=2, label='Other')
    ]
    plt.legend(handles=legend_elements, loc='lower right')
    
    plt.axis('off')  # Hide the axes
    plt.tight_layout()
    
    return plt.gcf()

def display_relationship_network(all_articles):
    """
    Display a network visualization of entity relationships in Streamlit.
    
    Parameters:
    -----------
    all_articles : list
        List of article dictionaries
    """
    st.subheader("Entity Relationship Network")
    
    # Create network visualization
    fig = create_relationship_network(all_articles)
    
    if fig:
        # Display the figure
        st.pyplot(fig)
        
        # Add explanation
        st.markdown("""
        This network shows relationships between countries, organizations, and other entities mentioned in the articles.
        - **Node size**: Indicates how central/important an entity is in the network
        - **Edge color**: Indicates the type of relationship (see legend)
        - **Edge width**: Indicates the strength/frequency of the relationship
        """)
        
        # Save as image button
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
        buf.seek(0)
        
        st.download_button(
            label="Download Network Image",
            data=buf,
            file_name="entity_network.png",
            mime="image/png"
        )
    else:
        st.info("Not enough relationship data to create a network visualization.")
