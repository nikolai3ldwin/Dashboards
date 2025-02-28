import streamlit as st
from datetime import datetime
from utils.document_processing import extract_text
from utils.data_extraction import extract_entities, extract_regex_matches, get_sentences_with_entity, identify_data_category

def show_data_extraction_page():
    """Display the data extraction page."""
    st.header("Extract Data from Documents")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Upload Document")
        uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"], accept_multiple_files=True)
        
        # Process files only if files were uploaded
        if uploaded_file and len(uploaded_file) > 0:
            for file in uploaded_file:
                # Extract text from document
                st.info(f"Processing {file.name}...")
                extracted_text = extract_text(file)
                
                if extracted_text:
                    # Save document to collection
                    doc_id = file.name
                    st.session_state.doc_collection[doc_id] = {
                        'name': file.name,
                        'text': extracted_text,
                        'date_added': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    # Extract entities using regex patterns
                    with st.spinner("Extracting entities..."):
                        entities = extract_entities(extracted_text)
                    
                    # Extract regex matches
                    with st.spinner("Extracting patterns..."):
                        regex_matches = extract_regex_matches(extracted_text)
                    
                    st.success(f"Successfully processed {file.name}")
                    
                    # Display extracted information in tabs
                    tabs = st.tabs(["Entities", "Pattern Matches", "Full Text"])
                    
                    with tabs[0]:
                        for entity_type, items in entities.items():
                            if items:
                                st.write(f"**{entity_type}:**")
                                for item in items:
                                    col1, col2 = st.columns([3, 1])
                                    with col1:
                                        st.write(f"- {item}")
                                    with col2:
                                        if st.button(f"Add to Profile", key=f"add_{entity_type}_{item}"):
                                            category = identify_data_category(entity_type, item)
                                            context = get_sentences_with_entity(extracted_text, item)
                                            
                                            if category == 'personal_info':
                                                st.session_state.extracted_data[category][item] = {
                                                    'value': item,
                                                    'source': file.name,
                                                    'context': context[:3] if context else []
                                                }
                                            else:
                                                st.session_state.extracted_data[category].append({
                                                    'value': item,
                                                    'source': file.name,
                                                    'entity_type': entity_type,
                                                    'context': context[:3] if context else []
                                                })
                    
                    with tabs[1]:
                        for pattern_type, matches in regex_matches.items():
                            if matches:
                                st.write(f"**{pattern_type.capitalize()}:**")
                                for match in matches:
                                    col1, col2 = st.columns([3, 1])
                                    with col1:
                                        st.write(f"- {match}")
                                    with col2:
                                        if st.button(f"Add to Profile", key=f"add_{pattern_type}_{match}"):
                                            category = identify_data_category(pattern_type, match)
                                            context = get_sentences_with_entity(extracted_text, match)
                                            
                                            if category == 'personal_info':
                                                st.session_state.extracted_data[category][pattern_type] = {
                                                    'value': match,
                                                    'source': file.name,
                                                    'context': context[:3] if context else []
                                                }
                                            else:
                                                st.session_state.extracted_data[category].append({
                                                    'value': match,
                                                    'pattern_type': pattern_type,
                                                    'source': file.name,
                                                    'context': context[:3] if context else []
                                                })
                    
                    with tabs[2]:
                        st.text_area("Document Text", extracted_text, height=400)
                else:
                    st.error(f"Could not extract text from {file.name}. Unsupported file format.")
    
    with col2:
        st.subheader("Extracted Profile Data")
        
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
        
        if st.button("Clear Extracted Data"):
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
