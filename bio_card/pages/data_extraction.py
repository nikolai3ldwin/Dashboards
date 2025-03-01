import streamlit as st
from datetime import datetime
from utils.document_processing import extract_text
from utils.data_extraction import extract_entities, extract_regex_matches, get_sentences_with_entity, identify_data_category

def ensure_session_state():
    """
    Ensure session state variables are initialized with default values.
    This prevents AttributeError and ensures consistent data structure.
    """
    # Initialize extracted_data if not exists
    if 'extracted_data' not in st.session_state:
        st.session_state.extracted_data = {
            'personal_info': {},
            'professional_background': [],
            'financial_info': [],
            'public_records': [],
            'connections': [],
            'digital_footprint': [],
            'inconsistencies': []
        }
    
    # Initialize document collection if not exists
    if 'doc_collection' not in st.session_state:
        st.session_state.doc_collection = {}

def show_data_extraction_page():
    """Display the data extraction page."""
    # Ensure session state is properly initialized
    ensure_session_state()

    st.header("Extract Data from Documents")
    
    # Create two columns for layout
    left_column, right_column = st.columns(2)
    
    # Left column - File upload and processing
    with left_column:
        st.subheader("Upload Document")
        
        # Use a try-except block to handle potential errors with the file uploader
        try:
            # Create the file uploader
            uploaded_files = st.file_uploader(
                "Choose files", 
                type=["pdf", "docx", "txt"], 
                accept_multiple_files=True,
                key="document_uploader"
            )
            
            # Check if we have any uploaded files
            if uploaded_files:
                # Add a button to process all files
                if st.button("Process All Files", key="process_files_btn"):
                    # Iterate through the files safely
                    for i, file in enumerate(uploaded_files):
                        try:
                            # Extract text from document
                            st.info(f"Processing {file.name}...")
                            extracted_text = extract_text(file)
                            
                            if extracted_text:
                                # Safely add to doc collection
                                doc_id = f"{file.name}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                                st.session_state.doc_collection[doc_id] = {
                                    'name': file.name,
                                    'text': extracted_text,
                                    'date_added': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                }
                                
                                # Extract entities
                                with st.spinner("Extracting entities..."):
                                    entities = extract_entities(extracted_text)
                                
                                # Extract regex matches
                                with st.spinner("Extracting patterns..."):
                                    regex_matches = extract_regex_matches(extracted_text)
                                
                                st.success(f"Successfully processed {file.name}")
                                
                                # Create a unique container for this file's results
                                with st.expander(f"Results for {file.name}", expanded=True):
                                    # Use tabs for organizing the different types of extracted data
                                    file_tabs = st.tabs(["Entities", "Pattern Matches", "Full Text"])
                                    
                                    with file_tabs[0]:
                                        for entity_type, items in entities.items():
                                            if items:
                                                st.write(f"**{entity_type}:**")
                                                for item_idx, item in enumerate(items):
                                                    # Create unique key for each button
                                                    button_key = f"entity_{i}_{entity_type}_{item_idx}"
                                                    
                                                    col1, col2 = st.columns([3, 1])
                                                    with col1:
                                                        st.write(f"- {item}")
                                                    with col2:
                                                        if st.button("Add", key=button_key):
                                                            # Identify appropriate category for the entity
                                                            category = identify_data_category(entity_type, item)
                                                            context = get_sentences_with_entity(extracted_text, item)
                                                            
                                                            # Defensive handling of data addition
                                                            if category == 'personal_info':
                                                                # For personal_info, use dictionary with item as key
                                                                st.session_state.extracted_data['personal_info'][item] = {
                                                                    'value': item,
                                                                    'source': file.name,
                                                                    'context': context[:3] if context else []
                                                                }
                                                            else:
                                                                # For list-based categories, append new item
                                                                st.session_state.extracted_data[category].append({
                                                                    'value': item,
                                                                    'source': file.name,
                                                                    'entity_type': entity_type,
                                                                    'context': context[:3] if context else []
                                                                })
                                                            
                                                            st.success(f"Added {item} to {category}")
                                    
                                    with file_tabs[1]:
                                        for pattern_type, matches in regex_matches.items():
                                            if matches:
                                                st.write(f"**{pattern_type.capitalize()}:**")
                                                for match_idx, match in enumerate(matches):
                                                    # Create unique key for each button
                                                    button_key = f"pattern_{i}_{pattern_type}_{match_idx}"
                                                    
                                                    col1, col2 = st.columns([3, 1])
                                                    with col1:
                                                        st.write(f"- {match}")
                                                    with col2:
                                                        if st.button("Add", key=button_key):
                                                            # Identify appropriate category for the pattern
                                                            category = identify_data_category(pattern_type, match)
                                                            context = get_sentences_with_entity(extracted_text, match)
                                                            
                                                            # Defensive handling of data addition
                                                            if category == 'personal_info':
                                                                # For personal_info, use pattern_type as key
                                                                st.session_state.extracted_data['personal_info'][pattern_type] = {
                                                                    'value': match,
                                                                    'source': file.name,
                                                                    'context': context[:3] if context else []
                                                                }
                                                            else:
                                                                # For list-based categories, append new item
                                                                st.session_state.extracted_data[category].append({
                                                                    'value': match,
                                                                    'pattern_type': pattern_type,
                                                                    'source': file.name,
                                                                    'context': context[:3] if context else []
                                                                })
                                                            
                                                            st.success(f"Added {match} to {category}")
                                    
                                    with file_tabs[2]:
                                        st.text_area("Document Text", extracted_text, height=400, key=f"text_{i}")
                            else:
                                st.error(f"Could not extract text from {file.name}. Unsupported file format.")
                        except Exception as e:
                            st.error(f"Error processing file {file.name}: {str(e)}")
            else:
                st.info("Upload files to extract information")
        except Exception as e:
            st.error(f"Error with file uploader: {str(e)}")
    
    # Right column - Display extracted data
    with right_column:
        st.subheader("Extracted Profile Data")
        
        # Ensure session state is initialized
        ensure_session_state()
        
        # Display data by category
        for category, data in st.session_state.extracted_data.items():
            st.write(f"**{category.replace('_', ' ').title()}:**")
            
            if isinstance(data, dict):
                # For dictionary type categories (like personal_info)
                for key, value in data.items():
                    if isinstance(value, dict):
                        st.write(f"- {key}: {value.get('value', '')}")
                        with st.expander("Details"):
                            st.write(f"Source: {value.get('source', 'Unknown')}")
                            st.write("Context:")
                            for ctx in value.get('context', []):
                                st.info(ctx)
                    else:
                        st.write(f"- {key}: {value}")
            else:
                # For list type categories
                for item in data:
                    if isinstance(item, dict):
                        st.write(f"- {item.get('value', '')}")
                        with st.expander("Details"):
                            st.write(f"Source: {item.get('source', 'Unknown')}")
                            st.write(f"Type: {item.get('entity_type', item.get('pattern_type', 'Unknown'))}")
                            st.write("Context:")
                            for ctx in item.get('context', []):
                                st.info(ctx)
                    else:
                        st.write(f"- {item}")
        
        # Clear button
        if st.button("Clear Extracted Data"):
            # Reinitialize with default empty structure
            st.session_state.extracted_data = {
                'personal_info': {},
                'professional_background': [],
                'financial_info': [],
                'public_records': [],
                'connections': [],
                'digital_footprint': [],
                'inconsistencies': []
            }
            st.experimental_rerun()
