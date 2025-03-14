# components/article_card.py
"""
Component for displaying individual articles in the dashboard.
"""

import streamlit as st
from PIL import Image

def display_article(article, image):
    """
    Display a single article in a card format.
    
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
            
            # Create expandable sections for additional info
            with st.expander("Details"):
                # Tags
                if article.get('tags'):
                    st.markdown("**Tags:** " + ", ".join(article['tags']))
                
                # Sentiment analysis with visual indicators
                if article.get('sentiment'):
                    st.markdown("**Sentiment Analysis:**")
                    
                    # Create a horizontal bar chart for sentiment
                    for entity, score in article['sentiment'].items():
                        # Determine color based on sentiment
                        color = "green" if score > 0 else "red" if score < 0 else "gray"
                        
                        # Calculate width percentage (convert -1 to 1 scale to 0-100%)
                        width = abs(score) * 50  # 50% is neutral
                        
                        # Create label
                        label = f"{entity}: {score:.2f}"
                        
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
            with col_a:
                st.button("Read Full Article", key=f"read_{article['title'][:10]}", 
                          help=f"Open {article['link']}")
            with col_b:
                st.button("Save for Later", key=f"save_{article['title'][:10]}", 
                          help="Save this article to your reading list")
            with col_c:
                st.button("Share", key=f"share_{article['title'][:10]}", 
                          help="Share this article")

def display_article_compact(article, image):
    """
    Display a single article in a more compact format.
    
    Parameters:
    -----------
    article : dict
        Article data dictionary containing title, date, summary, etc.
    image : PIL.Image
        Image to display with the article
    """
    # Create a compact card
    with st.container():
        # Horizontal layout
        cols = st.columns([1, 4])
        
        with cols[0]:
            # Display the image and importance
            st.image(image, use_column_width=True)
            st.markdown(f"**{article['importance']}**⭐")
        
        with cols[1]:
            # Article title and source
            st.markdown(f"### [{article['title']}]({article['link']})")
            st.markdown(f"**{article['source']}** · {article['date'].strftime('%Y-%m-%d')}")
            
            # Truncated summary
            short_summary = article['summary'][:150] + "..." if len(article['summary']) > 150 else article['summary']
            st.markdown(short_summary)
        
        st.markdown("---")

def display_articles_grid(articles, images_dict, columns=3):
    """
    Display articles in a grid layout.
    
    Parameters:
    -----------
    articles : list
        List of article dictionaries
    images_dict : dict
        Dictionary mapping article URLs to loaded images
    columns : int
        Number of columns in the grid
    """
    # Create a grid of articles
    cols = st.columns(columns)
    
    for i, article in enumerate(articles):
        with cols[i % columns]:
            # Get the image
            image = images_dict.get(article.get('image_url', ''))
            
            # Card container
            st.markdown(
                f"""
                <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; 
                            margin-bottom: 15px; height: 400px; overflow: hidden;">
                """,
                unsafe_allow_html=True
            )
            
            # Image
            st.image(image, use_column_width=True)
            
            # Title and importance
            st.markdown(f"### [{article['title']}]({article['link']})")
            importance_stars = "⭐" * article['importance']
            st.markdown(f"**Importance:** {importance_stars}")
            
            # Truncated summary
            short_summary = article['summary'][:100] + "..." if len(article['summary']) > 100 else article['summary']
            st.markdown(short_summary)
            
            # Source and date
            st.markdown(f"**{article['source']}** · {article['date'].strftime('%m/%d/%Y')}")
            
            # End container
            st.markdown("</div>", unsafe_allow_html=True)
