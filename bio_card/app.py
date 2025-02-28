import streamlit as st
from datetime import datetime
from pages.data_extraction import show_data_extraction_page
from pages.profile_builder import show_profile_builder_page
from pages.api_connections import show_api_connections_page
from pages.document_repository import show_document_repository_page

# Set up the page configuration
st.set_page_config(
    page_title="Investigative Profile Builder",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
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

if 'profile_collection' not in st.session_state:
    st.session_state.profile_collection = {}

if 'doc_collection' not in st.session_state:
    st.session_state.doc_collection = {}

def main():
    """Main application."""
    st.title("Investigative Profile Builder")
    st.write("Extract, organize, and analyze information for investigative profiles")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Data Extraction", "Profile Builder", "API Connections", "Document Repository"])
    
    # Display saved profiles in sidebar
    if st.session_state.profile_collection:
        st.sidebar.title("Saved Profiles")
        selected_profile = st.sidebar.selectbox(
            "Select Profile", 
            list(st.session_state.profile_collection.keys())
        )
        
        if selected_profile:
            if st.sidebar.button("Load Profile"):
                st.session_state.extracted_data = st.session_state.profile_collection[selected_profile]['data'].copy()
                st.sidebar.success(f"Loaded profile: {selected_profile}")
                st.session_state.profile_collection[selected_profile]['last_accessed'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Display current stats
    st.sidebar.title("Current Profile Stats")
    stats = {
        "Personal Info Points": len(st.session_state.extracted_data['personal_info']),
        "Professional Background": len(st.session_state.extracted_data['professional_background']),
        "Financial Info": len(st.session_state.extracted_data['financial_info']),
        "Public Records": len(st.session_state.extracted_data['public_records']),
        "Connections": len(st.session_state.extracted_data['connections']),
        "Digital Footprint": len(st.session_state.extracted_data['digital_footprint'])
    }
    
    for key, value in stats.items():
        st.sidebar.write(f"- {key}: {value}")
    
    # Navigate to selected page
    if page == "Data Extraction":
        show_data_extraction_page()
    elif page == "Profile Builder":
        show_profile_builder_page()
    elif page == "API Connections":
        show_api_connections_page()
    elif page == "Document Repository":
        show_document_repository_page()

if __name__ == "__main__":
    main()
