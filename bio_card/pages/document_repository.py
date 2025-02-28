import streamlit as st
import json
from datetime import datetime
from utils.document_processing import extract_text
from utils.api_connectors import authenticate_google_drive, list_google_drive_files

def show_document_repository_page():
    """Display the document repository page."""
    st.header("Document Repository")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        show_document_sources(col1)
    
    with col2:
        show_document_collection(col2)

def show_document_sources(container):
    """Display document source options in the provided container."""
    container.subheader("Document Sources")
    
    # Google Drive connection
    with container.expander("Google Drive", expanded=True):
        if st.button("Connect to Google Drive"):
            with st.spinner("Authenticating..."):
                authenticated = authenticate_google_drive()
            
            if authenticated:
                st.success("Connected to Google Drive")
                
                with st.spinner("Fetching files..."):
                    files = list_google_drive_files()
                
                st.write("Available files:")
                for file in files:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"📄 {file['name']}")
                    with col2:
                        if st.button("Import", key=f"import_{file['id']}"):
                            st.session_state.doc_collection[file['id']] = {
                                'name': file['name'],
                                'text': f"Sample text from {file['name']}",  # In real implementation, download and process
                                'date_added': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                'source': 'Google Drive'
                            }
                            st.success(f"Imported {file['name']}")
                            st.experimental_rerun()
    
    # Local file upload
    with container.expander("Local Files", expanded=True):
        st.subheader("Upload Files")
        
        upload_files = st.file_uploader("Upload to Repository", type=["pdf", "docx", "txt", "csv", "xlsx"], accept_multiple_files=True)
        
        if upload_files:
            for file in upload_files:
                file_extension = file.name.split('.')[-1].lower()
                
                if file_extension in ['pdf', 'docx', 'txt']:
                    with st.spinner(f"Processing {file.name}..."):
                        extracted_text = extract_text(file)
                    
                    if extracted_text:
                        doc_id = f"{file.name}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                        st.session_state.doc_collection[doc_id] = {
                            'name': file.name,
                            'text': extracted_text,
                            'date_added': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'source': 'Local Upload'
                        }
                        st.success(f"Added {file.name} to repository")
                else:
                    st.warning(f"File type {file_extension} not processed for text extraction, but added to repository")
                    doc_id = f"{file.name}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    st.session_state.doc_collection[doc_id] = {
                        'name': file.name,
                        'text': "Binary file - no text extraction",
                        'date_added': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'source': 'Local Upload',
                        'binary': True
                    }
    
    # URL import
    with container.expander("Web URL", expanded=True):
        st.subheader("Import from URL")
        
        url = st.text_input("Web Page URL")
        
        if st.button("Fetch Content") and url:
            st.info("In a real implementation, this would fetch and process content from the provided URL.")
            
            # This is a mock implementation
            doc_id = f"url_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            st.session_state.doc_collection[doc_id] = {
                'name': url,
                'text': f"Content fetched from {url}",
                'date_added': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'source': 'Web URL'
            }
            st.success(f"Added content from {url} to repository")

def show_document_collection(container):
    """Display the document collection in the provided container."""
    container.subheader("Document Collection")
    
    # Filter and sort options
    col1, col2 = container.columns(2)
    with col1:
        sort_by = st.selectbox("Sort by", ["Date Added (Newest)", "Date Added (Oldest)", "Name (A-Z)", "Name (Z-A)"])
    with col2:
        filter_source = st.selectbox("Filter by source", ["All Sources", "Google Drive", "Local Upload", "Web URL"])
    
    # Process documents based on sort and filter options
    documents = []
    for doc_id, doc_info in st.session_state.doc_collection.items():
        # Apply source filter
        if filter_source != "All Sources" and doc_info.get('source') != filter_source:
            continue
        
        documents.append((doc_id, doc_info))
    
    # Apply sorting
    if sort_by == "Date Added (Newest)":
        documents.sort(key=lambda x: x[1]['date_added'], reverse=True)
    elif sort_by == "Date Added (Oldest)":
        documents.sort(key=lambda x: x[1]['date_added'])
    elif sort_by == "Name (A-Z)":
        documents.sort(key=lambda x: x[1]['name'])
    elif sort_by == "Name (Z-A)":
        documents.sort(key=lambda x: x[1]['name'], reverse=True)
    
    # Display documents
    if not documents:
        container.info("No documents in the repository yet. Connect to Google Drive or upload files.")
    else:
        for doc_id, doc_info in documents:
            with container.expander(f"{doc_info['name']} - {doc_info['date_added']}"):
                st.write(f"**Source:** {doc_info.get('source', 'Unknown')}")
                
                if doc_info.get('binary', False):
                    st.write("Binary file - no text preview available")
                else:
                    st.write("**Preview:**")
                    st.text_area(
                        "Document Content", 
                        doc_info['text'][:500] + "..." if len(doc_info['text']) > 500 else doc_info['text'],
                        height=150,
                        key=f"preview_{doc_id}"
                    )
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button("Process Document", key=f"process_{doc_id}"):
                        st.session_state['current_doc'] = doc_id
                        st.info(f"Go to 'Data Extraction' tab to process {doc_info['name']}")
                
                with col2:
                    if st.button("Download", key=f"download_{doc_id}"):
                        # In a real app, this would provide the actual file
                        st.info("Download functionality would be implemented here")
                
                with col3:
                    if st.button("Copy Text", key=f"copy_{doc_id}"):
                        st.info("Text copied to clipboard functionality would be implemented here")
                
                with col4:
                    if st.button("Delete", key=f"delete_{doc_id}"):
                        if st.session_state.doc_collection.pop(doc_id, None):
                            st.success(f"Deleted {doc_info['name']} from repository")
                            st.experimental_rerun()
    
    # Export repository metadata
    container.divider()
    if container.button("Export Repository Metadata"):
        repo_metadata = {}
        for doc_id, doc_info in st.session_state.doc_collection.items():
            repo_metadata[doc_id] = {
                'name': doc_info['name'],
                'date_added': doc_info['date_added'],
                'source': doc_info.get('source', 'Unknown'),
                'binary': doc_info.get('binary', False)
            }
        
        # Provide download button for the metadata
        container.download_button(
            label="Download Repository Metadata",
            data=json.dumps(repo_metadata, indent=2),
            file_name="document_repository_metadata.json",
            mime="application/json"
        )
    
    # Import metadata
    container.write("Import repository metadata:")
    uploaded_metadata = container.file_uploader("Upload Repository Metadata", type=["json"], key="metadata_upload")
    
    if uploaded_metadata is not None:
        try:
            metadata_content = json.loads(uploaded_metadata.getvalue().decode())
            if container.button("Import Metadata"):
                for doc_id, doc_info in metadata_content.items():
                    if doc_id not in st.session_state.doc_collection:
                        # Add placeholder for actual document content
                        doc_info['text'] = "[Document content not available - metadata only]"
                        st.session_state.doc_collection[doc_id] = doc_info
                
                container.success(f"Imported metadata for {len(metadata_content)} documents")
                st.experimental_rerun()
        except Exception as e:
            container.error(f"Error importing metadata: {str(e)}")
