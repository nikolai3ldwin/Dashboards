import streamlit as st
import json
from utils.api_connectors import (
    check_linkedin_data, 
    check_public_records, 
    analyze_social_media, 
    make_custom_api_request
)

def show_api_connections_page():
    """Display the API connections page."""
    st.header("API Connections")
    
    api_tabs = st.tabs(["LinkedIn", "Public Records", "Social Media", "Custom API"])
    
    with api_tabs[0]:
        show_linkedin_tab()
    
    with api_tabs[1]:
        show_public_records_tab()
    
    with api_tabs[2]:
        show_social_media_tab()
    
    with api_tabs[3]:
        show_custom_api_tab()

def show_linkedin_tab():
    """Display LinkedIn API tab."""
    st.subheader("LinkedIn Data")
    
    linkedin_url = st.text_input("LinkedIn Profile URL")
    api_key = st.text_input("API Key (if available)", type="password")
    
    if st.button("Check LinkedIn Data"):
        if linkedin_url:
            with st.spinner("Fetching LinkedIn data..."):
                linkedin_data = check_linkedin_data(linkedin_url, api_key)
            
            st.json(linkedin_data)
            
            if st.button("Add to Profile"):
                # Add current position to professional background
                if 'current_position' in linkedin_data:
                    st.session_state.extracted_data['professional_background'].append({
                        'value': linkedin_data['current_position'],
                        'source': 'LinkedIn API',
                        'entity_type': 'ORG',
                        'context': []
                    })
                
                # Add previous positions
                for position in linkedin_data.get('previous_positions', []):
                    st.session_state.extracted_data['professional_background'].append({
                        'value': position,
                        'source': 'LinkedIn API',
                        'entity_type': 'ORG',
                        'context': []
                    })
                
                # Add skills 
                if 'skills' in linkedin_data:
                    st.session_state.extracted_data['professional_background'].append({
                        'value': f"Skills: {', '.join(linkedin_data['skills'])}",
                        'source': 'LinkedIn API',
                        'entity_type': 'SKILL',
                        'context': []
                    })
                
                # Add education
                for education in linkedin_data.get('education', []):
                    st.session_state.extracted_data['professional_background'].append({
                        'value': f"Education: {education}",
                        'source': 'LinkedIn API',
                        'entity_type': 'EDU',
                        'context': []
                    })
                
                st.success("LinkedIn data added to profile")
        else:
            st.error("Please enter a LinkedIn profile URL")

def show_public_records_tab():
    """Display public records API tab."""
    st.subheader("Public Records Search")
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name")
    with col2:
        state = st.selectbox("State", ["", "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", 
                                     "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
                                     "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
                                     "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
                                     "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"])
    
    if st.button("Search Public Records"):
        if name:
            with st.spinner("Searching public records..."):
                records = check_public_records(name, state if state else None)
            
            # Display records in expandable sections
            if 'court_cases' in records and records['court_cases']:
                with st.expander("Court Cases", expanded=True):
                    for case in records['court_cases']:
                        st.write(f"**Case Number:** {case.get('case_number')}")
                        st.write(f"**Court:** {case.get('court')}")
                        st.write(f"**Type:** {case.get('type')}")
                        st.write(f"**Date:** {case.get('date')}")
                        st.divider()
            
            if 'property_records' in records and records['property_records']:
                with st.expander("Property Records", expanded=True):
                    for property in records['property_records']:
                        st.write(f"**Address:** {property.get('address')}")
                        st.write(f"**Purchase Date:** {property.get('purchase_date')}")
                        st.write(f"**Value:** {property.get('value')}")
                        st.divider()
            
            if 'business_registrations' in records and records['business_registrations']:
                with st.expander("Business Registrations", expanded=True):
                    for business in records['business_registrations']:
                        st.write(f"**Name:** {business.get('name')}")
                        st.write(f"**State:** {business.get('state')}")
                        st.write(f"**Registration Date:** {business.get('registration_date')}")
                        st.divider()
            
            if st.button("Add to Profile"):
                # Add court cases to public records
                for case in records.get('court_cases', []):
                    st.session_state.extracted_data['public_records'].append({
                        'value': f"Court Case: {case.get('case_number')} - {case.get('court')}",
                        'details': case,
                        'source': 'Public Records API',
                        'entity_type': 'LEGAL',
                        'context': []
                    })
                
                # Add property to financial info
                for property in records.get('property_records', []):
                    st.session_state.extracted_data['financial_info'].append({
                        'value': f"Property: {property.get('address')} - {property.get('value')}",
                        'details': property,
                        'source': 'Public Records API',
                        'entity_type': 'MONEY',
                        'context': []
                    })
                
                # Add businesses to professional background
                for business in records.get('business_registrations', []):
                    st.session_state.extracted_data['professional_background'].append({
                        'value': f"Business: {business.get('name')}",
                        'details': business,
                        'source': 'Public Records API',
                        'entity_type': 'ORG',
                        'context': []
                    })
                
                st.success("Public records data added to profile")
        else:
            st.error("Please enter a name to search")

def show_social_media_tab():
    """Display social media API tab."""
    st.subheader("Social Media Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        platform = st.selectbox("Platform", ["Twitter", "Facebook", "Instagram", "TikTok", "YouTube"])
    with col2:
        handle = st.text_input("Username/Handle")
    
    api_key = st.text_input("API Key (if available)", type="password", key="social_api_key")
    
    if st.button("Analyze Social Media"):
        if handle:
            with st.spinner(f"Analyzing {platform} data..."):
                social_data = analyze_social_media(handle, platform, api_key)
            
            st.json(social_data)
            
            if st.button("Add to Digital Footprint"):
                st.session_state.extracted_data['digital_footprint'].append({
                    'value': f"{platform}: @{handle}",
                    'platform': platform,
                    'handle': handle,
                    'details': social_data,
                    'source': f"{platform} API",
                    'entity_type': 'SOCIAL',
                    'context': []
                })
                
                st.success(f"{platform} data added to profile")
        else:
            st.error("Please enter a username/handle")

def show_custom_api_tab():
    """Display custom API tab."""
    st.subheader("Custom API Connection")
    
    col1, col2 = st.columns(2)
    with col1:
        api_url = st.text_input("API Endpoint URL")
    with col2:
        api_method = st.selectbox("HTTP Method", ["GET", "POST", "PUT", "DELETE"])
    
    headers = st.text_area("Headers (JSON format)", "{}")
    params = st.text_area("Parameters/Body (JSON format)", "{}")
    
    if st.button("Send Request"):
        if api_url:
            try:
                headers_dict = json.loads(headers)
                params_dict = json.loads(params)
                
                with st.spinner("Sending API request..."):
                    response = make_custom_api_request(api_url, api_method, headers_dict, params_dict if api_method == "GET" else None, params_dict if api_method != "GET" else None)
                
                if response:
                    st.write(f"Status Code: {response.status_code}")
                    
                    try:
                        json_response = response.json()
                        st.json(json_response)
                        
                        if st.button("Add API Data to Profile"):
                            category = st.selectbox(
                                "Select category to add this data to",
                                ["professional_background", "financial_info", "public_records", 
                                 "connections", "digital_footprint", "inconsistencies"]
                            )
                            
                            data_name = st.text_input("Name for this data point")
                            
                            if data_name:
                                try:
                                    st.session_state.extracted_data[category].append({
                                        'value': data_name,
                                        'raw_data': json.dumps(json_response),
                                        'source': f"Custom API: {api_url}",
                                        'entity_type': 'API_DATA',
                                        'context': []
                                    })
                                    st.success(f"API data added to {category}")
                                except Exception as e:
                                    st.error(f"Error adding data: {str(e)}")
                    except:
                        st.text(response.text)
                        
                        if st.button("Add Text Response to Profile"):
                            category = st.selectbox(
                                "Select category to add this data to",
                                ["professional_background", "financial_info", "public_records", 
                                 "connections", "digital_footprint", "inconsistencies"]
                            )
                            
                            data_name = st.text_input("Name for this data point")
                            
                            if data_name:
                                try:
                                    st.session_state.extracted_data[category].append({
                                        'value': data_name,
                                        'raw_data': response.text,
                                        'source': f"Custom API: {api_url}",
                                        'entity_type': 'API_DATA',
                                        'context': []
                                    })
                                    st.success(f"API data added to {category}")
                                except Exception as e:
                                    st.error(f"Error adding data: {str(e)}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.error("Please enter an API URL")
