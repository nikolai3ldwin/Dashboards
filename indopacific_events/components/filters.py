# components/filters.py
"""
UI components for filtering content in the Indo-Pacific Dashboard
"""

import streamlit as st
import logging

# Get logger
logger = logging.getLogger("indo_pacific_dashboard")

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
    try:
        st.sidebar.title("Dashboard Filters")
        
        # Source selection with categorized layout
        try:
            from data.rss_sources import SOURCE_CATEGORIES
            logger.info("Successfully imported SOURCE_CATEGORIES")
        except ImportError as e:
            logger.warning(f"Could not import SOURCE_CATEGORIES: {str(e)}")
            # Create a default categorization based on the available feeds
            SOURCE_CATEGORIES = {"All Sources": [source for _, source in rss_feeds]}
        
        # Show expand/collapse all option
        st.sidebar.markdown("### News Sources")
        
        # Extract all source names
        all_sources = [source for _, source in rss_feeds] if rss_feeds else []
        
        # Initialize with empty list if state doesn't exist
        if 'selected_sources' not in st.session_state:
            # Initialize with first three sources as default
            st.session_state.selected_sources = all_sources[:3] if all_sources else []
        
        # Add Select All / Clear All buttons
        try:
            col1, col2 = st.sidebar.columns(2)
            if col1.button("Select All"):
                st.session_state.selected_sources = all_sources.copy()
            if col2.button("Clear All"):
                st.session_state.selected_sources = []
        except Exception as e:
            logger.error(f"Error creating source selection buttons: {str(e)}")
            # Fallback to simpler UI
            if st.sidebar.button("Toggle All Sources"):
                if len(st.session_state.selected_sources) == len(all_sources):
                    st.session_state.selected_sources = []
                else:
                    st.session_state.selected_sources = all_sources.copy()
        
        # Display source categories as expandable sections
        selected_sources = []
        
        try:
            for category, sources in SOURCE_CATEGORIES.items():
                with st.sidebar.expander(f"{category} ({len(sources)})"):
                    for source in sources:
                        if source in all_sources:
                            is_selected = st.checkbox(
                                source,
                                value=source in st.session_state.selected_sources,
                                key=f"source_{source.replace(' ', '_')}"
                            )
                            if is_selected and source not in selected_sources:
                                selected_sources.append(source)
        except Exception as e:
            logger.error(f"Error displaying source categories: {str(e)}")
            # Fallback to simple list
            st.sidebar.markdown("**Sources**")
            for source in all_sources:
                is_selected = st.sidebar.checkbox(
                    source,
                    value=source in st.session_state.selected_sources,
                    key=f"source_{source.replace(' ', '_')}"
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
            topics,
            key="topic_filter"
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
            countries,
            key="country_filter"
        )
        
        # Importance filter
        st.sidebar.markdown("### Content Filters")
        
        min_importance = st.sidebar.slider(
            "Minimum Importance Rating",
            min_value=1,
            max_value=5,
            value=1,
            help="Filter articles by their importance rating (1-5)",
            key="importance_filter"
        )
        
        # Expanded sentiment filter for all countries
        sentiment_options = ["All"]
        
        # Add specific sentiment options for countries
        for country in ["US", "China", "Japan", "Australia", "India"]:
            sentiment_options.append(f"Positive towards {country}")
            sentiment_options.append(f"Negative towards {country}")
        
        sentiment_filter = st.sidebar.selectbox(
            "Sentiment Analysis",
            sentiment_options,
            key="sentiment_filter"
        )
        
        # Sort options
        sort_options = ["Date", "Importance", "Relevance"]
        sort_by = st.sidebar.selectbox(
            "Sort Results By",
            sort_options,
            key="sort_filter"
        )
        
        # Keyword search
        search_term = st.sidebar.text_input(
            "Search for keywords",
            help="Enter keywords to search across all articles",
            key="search_term"
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
            time_periods,
            key="time_filter"
        )
        
        # Advanced options expander
        try:
            with st.sidebar.expander("Advanced Options"):
                # Display options
                st.markdown("#### Display Options")
                show_images = st.checkbox("Show Images", value=True, key="show_images")
                show_sentiment = st.checkbox("Show Sentiment Analysis", value=True, key="show_sentiment")
                show_tags = st.checkbox("Show Tags", value=True, key="show_tags")
                
                # Export options
                st.markdown("#### Export Options")
                export_format = st.selectbox(
                    "Export Format",
                    ["CSV", "JSON", "Excel"],
                    key="export_format"
                )
                
                if st.button("Export Results", key="export_button"):
                    st.info("Export functionality to be implemented")
        except Exception as e:
            logger.error(f"Error displaying advanced options: {str(e)}")
            # Skip these options if they cause errors
            show_images = True
            show_sentiment = True
            show_tags = True
        
        # About section
        try:
            with st.sidebar.expander("About This Dashboard"):
                st.markdown("""
                This dashboard aggregates news from multiple sources 
                across the Indo-Pacific region and categorizes them 
                based on importance, topics, and sentiment.
                
                **Version**: 1.0.0
                
                **GitHub**: [Project Repository](https://github.com/yourusername/indo-pacific-dashboard)
                """)
        except Exception as e:
            logger.error(f"Error displaying about section: {str(e)}")
            # Not critical, can be skipped
        
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
            "show_images": show_images if 'show_images' in locals() else True,
            "show_sentiment": show_sentiment if 'show_sentiment' in locals() else True,
            "show_tags": show_tags if 'show_tags' in locals() else True
        }
        
    except Exception as e:
        logger.error(f"Error creating sidebar filters: {str(e)}")
        # Return default filter settings in case of error
        return {
            "selected_sources": [],
            "selected_topic": "All",
            "selected_country": "All",
            "min_importance": 1,
            "sentiment_filter": "All",
            "sort_by": "Date",
            "search_term": "",
            "time_filter": "All Time",
            "show_images": True,
            "show_sentiment": True,
            "show_tags": True
        }
