# components/filters.py
"""
UI components for filtering content in the Indo-Pacific Dashboard
"""

import streamlit as st

def create_sidebar_filters(rss_feeds):
    """
    Create and handle all sidebar filters for the dashboard.
    Returns a dictionary of filter settings.
    
    Parameters:
    -----------
    rss_feeds : list
        List of (url, source_name) tuples for RSS feeds
    
    Returns:
    --------
    dict
        Dictionary containing all filter settings
    """
    st.sidebar.title("Dashboard Filters")
    
    # Source selection with categorized layout
    from data.rss_sources import SOURCE_CATEGORIES
    
    # Show expand/collapse all option
    st.sidebar.markdown("### News Sources")
    
    all_sources = [source for _, source in rss_feeds]
    
    # Initialize with empty list if state doesn't exist
    if 'selected_sources' not in st.session_state:
        st.session_state.selected_sources = []
    
    # Add Select All / Clear All buttons
    col1, col2 = st.sidebar.columns(2)
    if col1.button("Select All"):
        st.session_state.selected_sources = all_sources.copy()
    if col2.button("Clear All"):
        st.session_state.selected_sources = []
    
    # Display source categories as expandable sections
    selected_sources = []
    for category, sources in SOURCE_CATEGORIES.items():
        with st.sidebar.expander(f"{category} ({len(sources)})"):
            for source in sources:
                if source in all_sources:
                    is_selected = st.checkbox(
                        source,
                        value=source in st.session_state.selected_sources
                    )
                    if is_selected and source not in selected_sources:
                        selected_sources.append(source)
    
    # Update session state
    st.session_state.selected_sources = selected_sources
    
    # Topic filter with new categories
    st.sidebar.markdown("### Topic Filters")
    
    topics = [
        "All", 
        "Political", 
        "Military", 
        "Civil Affairs", 
        "Drug Proliferation",
        "CWMD", 
        "Business"
    ]
    
    selected_topic = st.sidebar.selectbox(
        "Select Topic Category",
        topics
    )
    
    # Country filter
    countries = [
        "All", 
        "New Caledonia", 
        "Wallis and Futuna", 
        "China", 
        "United States",
        "Japan", 
        "Australia", 
        "India", 
        "Indonesia", 
        "Philippines", 
        "Malaysia",
        "Vietnam", 
        "South Korea", 
        "Taiwan", 
        "Thailand",
        "Cambodia", 
        "Myanmar", 
        "Papua New Guinea", 
        "Fiji", 
        "Solomon Islands",
        "Vanuatu", 
        "Samoa", 
        "Tonga", 
        "Cook Islands"
    ]
    
    selected_country = st.sidebar.selectbox(
        "Select Country/Region",
        countries
    )
    
    # Importance filter
    st.sidebar.markdown("### Content Filters")
    
    min_importance = st.sidebar.slider(
        "Minimum Importance Rating",
        min_value=1,
        max_value=5,
        value=1,
        help="Filter articles by their importance rating (1-5)"
    )
    
    # Sentiment filter
    sentiment_options = [
        "All", 
        "Positive towards US", 
        "Negative towards US",
        "Positive towards China",
        "Negative towards China"
    ]
    
    sentiment_filter = st.sidebar.selectbox(
        "Sentiment Analysis",
        sentiment_options
    )
    
    # Sort options
    sort_options = ["Date", "Importance", "Relevance"]
    sort_by = st.sidebar.selectbox(
        "Sort Results By",
        sort_options
    )
    
    # Keyword search
    search_term = st.sidebar.text_input(
        "Search for keywords",
        help="Enter keywords to search across all articles"
    )
    
    # Time period filter
    time_periods = [
        "All Time",
        "Today",
        "Past Week",
        "Past Month",
        "Past 3 Months"
    ]
    
    time_filter = st.sidebar.selectbox(
        "Time Period",
        time_periods
    )
    
    # Advanced options expander
    with st.sidebar.expander("Advanced Options"):
        # Display options
        st.markdown("#### Display Options")
        show_images = st.checkbox("Show Images", value=True)
        show_sentiment = st.checkbox("Show Sentiment Analysis", value=True)
        show_tags = st.checkbox("Show Tags", value=True)
        
        # Export options
        st.markdown("#### Export Options")
        export_format = st.selectbox(
            "Export Format",
            ["CSV", "JSON", "Excel"]
        )
        
        if st.button("Export Results"):
            st.info("Export functionality to be implemented")
    
    # About section
    with st.sidebar.expander("About This Dashboard"):
        st.markdown("""
        This dashboard aggregates news from multiple sources 
        across the Indo-Pacific region and categorizes them 
        based on importance, topics, and sentiment.
        
        **Version**: 1.0.0
        
        **GitHub**: [Project Repository](https://github.com/yourusername/indo-pacific-dashboard)
        """)
    
    # Return all filter settings as a dictionary
    return {
        "selected_sources": selected_sources,
        "selected_topic": selected_topic,
        "selected_country": selected_country,
        "min_importance": min_importance,
        "sentiment_filter": sentiment_filter,
        "sort_by": sort_by,
        "search_term": search_term,
        "time_filter": time_filter,
        "show_images": show_images,
        "show_sentiment": show_sentiment,
        "show_tags": show_tags
    }
