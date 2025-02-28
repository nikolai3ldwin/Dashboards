import streamlit as st
import json
from datetime import datetime

def show_profile_builder_page():
    """Display the profile builder page."""
    st.header("Profile Builder")
    
    # Profile name input
    profile_name = st.text_input("Profile Name", value="New Profile")
    
    tabs = st.tabs(["Personal Info", "Professional Background", "Financial Info", 
                   "Public Records", "Connections", "Digital Footprint", "Timeline"])
    
    with tabs[0]:
        show_personal_info_tab()
    
    with tabs[1]:
        show_professional_background_tab()
    
    with tabs[2]:
        show_financial_info_tab()
    
    with tabs[3]:
        show_public_records_tab()
    
    with tabs[4]:
        show_connections_tab()
    
    with tabs[5]:
        show_digital_footprint_tab()
    
    with tabs[6]:
        show_timeline_tab()
    
    # Save profile
    st.divider()
    if st.button("Save Profile"):
        if profile_name:
            st.session_state.profile_collection[profile_name] = {
                'data': st.session_state.extracted_data.copy(),
                'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'last_modified': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.success(f"Profile '{profile_name}' saved successfully")
            
            # Option to export
            download_json = st.download_button(
                label="Export as JSON",
                data=json.dumps(st.session_state.profile_collection[profile_name], indent=2),
                file_name=f"{profile_name.replace(' ', '_')}_profile.json",
                mime="application/json"
            )

def show_personal_info_tab():
    """Display personal information tab."""
    st.subheader("Personal Information")
    
    # Display existing personal info
    for field, info in st.session_state.extracted_data['personal_info'].items():
        if isinstance(info, dict):
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.write(f"**{field.capitalize()}:**")
            with col2:
                st.write(info.get('value', ''))
            with col3:
                st.write(f"Source: {info.get('source', 'Manual')}")
                
                # Add delete button
                if st.button("Delete", key=f"del_personal_{field}"):
                    del st.session_state.extracted_data['personal_info'][field]
                    st.experimental_rerun()
        else:
            st.write(f"**{field.capitalize()}:** {info}")
    
    # Manual entry
    st.divider()
    st.write("Add manually:")
    
    col1, col2 = st.columns(2)
    with col1:
        field = st.selectbox("Field", ["Name", "Age", "Date of Birth", "Place of Birth", "Address", "Phone", "Other"])
        if field == "Other":
            field = st.text_input("Custom field name")
    with col2:
        value = st.text_input("Value")
    
    notes = st.text_area("Notes (optional)", key="personal_notes")
    
    if st.button("Add Personal Info"):
        if field and value:
            field_key = field.lower()
            st.session_state.extracted_data['personal_info'][field_key] = {
                'value': value,
                'source': 'Manual Entry',
                'notes': notes,
                'context': []
            }
            st.success(f"Added {field} to profile")
            st.experimental_rerun()

def show_professional_background_tab():
    """Display professional background tab."""
    st.subheader("Professional Background")
    
    # Display extracted professional background
    for idx, item in enumerate(st.session_state.extracted_data['professional_background']):
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.write(f"**{item.get('value', '')}**")
            if 'dates' in item and item['dates']:
                st.write(f"*{item['dates']}*")
        with col2:
            st.write(f"Type: {item.get('entity_type', item.get('pattern_type', 'Unknown'))}")
            st.write(f"Source: {item.get('source', 'Manual')}")
        with col3:
            # Add delete button
            if st.button("Delete", key=f"del_prof_{idx}"):
                st.session_state.extracted_data['professional_background'].pop(idx)
                st.experimental_rerun()
                
        if 'notes' in item and item['notes']:
            st.write(f"Notes: {item['notes']}")
            
        with st.expander("Context"):
            for ctx in item.get('context', []):
                st.info(ctx)
        
        st.divider()
    
    # Manual entry
    st.write("Add manually:")
    
    col1, col2 = st.columns(2)
    with col1:
        org = st.text_input("Organization/Position")
    with col2:
        dates = st.text_input("Dates (if known)")
    
    notes = st.text_area("Notes", key="prof_notes")
    
    if st.button("Add Professional Background"):
        if org:
            st.session_state.extracted_data['professional_background'].append({
                'value': org,
                'dates': dates,
                'notes': notes,
                'source': 'Manual Entry',
                'entity_type': 'ORG',
                'context': []
            })
            st.success(f"Added {org} to professional background")
            st.experimental_rerun()

def show_financial_info_tab():
    """Display financial information tab."""
    st.subheader("Financial Information")
    
    # Display extracted financial info
    for idx, item in enumerate(st.session_state.extracted_data['financial_info']):
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.write(f"**{item.get('value', '')}**")
            if 'type' in item:
                st.write(f"*{item['type']}*")
        with col2:
            st.write(f"Type: {item.get('entity_type', item.get('pattern_type', 'Unknown'))}")
            st.write(f"Source: {item.get('source', 'Manual')}")
        with col3:
            # Add delete button
            if st.button("Delete", key=f"del_fin_{idx}"):
                st.session_state.extracted_data['financial_info'].pop(idx)
                st.experimental_rerun()
                
        if 'notes' in item and item['notes']:
            st.write(f"Notes: {item['notes']}")
            
        with st.expander("Context"):
            for ctx in item.get('context', []):
                st.info(ctx)
        
        st.divider()
    
    # Manual entry
    st.write("Add manually:")
    
    col1, col2 = st.columns(2)
    with col1:
        fin_type = st.selectbox("Type", ["Income", "Property", "Investment", "Business Ownership", "Other"])
        if fin_type == "Other":
            fin_type = st.text_input("Custom type")
    with col2:
        fin_value = st.text_input("Value/Description")
    
    fin_notes = st.text_area("Notes", key="fin_notes")
    
    if st.button("Add Financial Info"):
        if fin_value:
            st.session_state.extracted_data['financial_info'].append({
                'value': fin_value,
                'type': fin_type,
                'notes': fin_notes,
                'source': 'Manual Entry',
                'entity_type': 'MONEY' if fin_type in ["Income", "Property", "Investment"] else 'ORG',
                'context': []
            })
            st.success(f"Added {fin_type} information to financial data")
            st.experimental_rerun()

def show_public_records_tab():
    """Display public records tab."""
    st.subheader("Public Records")
    
    # Display extracted public records
    for idx, item in enumerate(st.session_state.extracted_data['public_records']):
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.write(f"**{item.get('value', '')}**")
        with col2:
            st.write(f"Source: {item.get('source', 'Manual')}")
        with col3:
            # Add delete button
            if st.button("Delete", key=f"del_pub_{idx}"):
                st.session_state.extracted_data['public_records'].pop(idx)
                st.experimental_rerun()
                
        if 'details' in item and item['details']:
            with st.expander("Details"):
                st.json(item['details'])
        
        with st.expander("Context"):
            for ctx in item.get('context', []):
                st.info(ctx)
        
        st.divider()
    
    # Manual entry
    st.write("Add manually:")
    
    record_type = st.selectbox("Record Type", ["Court Case", "Property Record", "Business Registration", "License", "Other"])
    if record_type == "Other":
        record_type = st.text_input("Custom record type")
    
    record_value = st.text_input("Record Description")
    record_date = st.date_input("Record Date")
    record_notes = st.text_area("Notes", key="record_notes")
    
    if st.button("Add Public Record"):
        if record_value:
            st.session_state.extracted_data['public_records'].append({
                'value': f"{record_type}: {record_value}",
                'type': record_type,
                'date': record_date.strftime("%Y-%m-%d"),
                'notes': record_notes,
                'source': 'Manual Entry',
                'entity_type': 'LEGAL',
                'context': []
            })
            st.success(f"Added {record_type} to public records")
            st.experimental_rerun()

def show_connections_tab():
    """Display connections tab."""
    st.subheader("Connections & Relationships")
    
    # Display extracted connections
    for idx, item in enumerate(st.session_state.extracted_data['connections']):
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.write(f"**{item.get('value', '')}**")
            if 'relationship' in item:
                st.write(f"*{item['relationship']}*")
        with col2:
            st.write(f"Source: {item.get('source', 'Manual')}")
        with col3:
            # Add delete button
            if st.button("Delete", key=f"del_conn_{idx}"):
                st.session_state.extracted_data['connections'].pop(idx)
                st.experimental_rerun()
                
        if 'notes' in item and item['notes']:
            st.write(f"Notes: {item['notes']}")
            
        with st.expander("Context"):
            for ctx in item.get('context', []):
                st.info(ctx)
        
        st.divider()
    
    # Manual entry
    st.write("Add manually:")
    
    col1, col2 = st.columns(2)
    with col1:
        person_name = st.text_input("Person Name")
    with col2:
        relationship = st.selectbox("Relationship", ["Family", "Business", "Social", "Professional", "Other"])
        if relationship == "Other":
            relationship = st.text_input("Custom relationship")
    
    conn_notes = st.text_area("Notes", key="conn_notes")
    
    if st.button("Add Connection"):
        if person_name:
            st.session_state.extracted_data['connections'].append({
                'value': person_name,
                'relationship': relationship,
                'notes': conn_notes,
                'source': 'Manual Entry',
                'entity_type': 'PERSON',
                'context': []
            })
            st.success(f"Added {person_name} to connections")
            st.experimental_rerun()

def show_digital_footprint_tab():
    """Display digital footprint tab."""
    st.subheader("Digital Footprint")
    
    # Display extracted digital footprint
    for idx, item in enumerate(st.session_state.extracted_data['digital_footprint']):
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.write(f"**{item.get('value', '')}**")
            if 'platform' in item:
                st.write(f"*{item['platform']}*")
        with col2:
            st.write(f"Source: {item.get('source', 'Manual')}")
        with col3:
            # Add delete button
            if st.button("Delete", key=f"del_digital_{idx}"):
                st.session_state.extracted_data['digital_footprint'].pop(idx)
                st.experimental_rerun()
                
        if 'details' in item and item['details']:
            with st.expander("Details"):
                st.json(item['details'])
        
        with st.expander("Context"):
            for ctx in item.get('context', []):
                st.info(ctx)
        
        st.divider()
    
    # Manual entry
    st.write("Add manually:")
    
    col1, col2 = st.columns(2)
    with col1:
        platform = st.selectbox("Platform", ["Email", "Website", "LinkedIn", "Twitter", "Facebook", "Instagram", "TikTok", "YouTube", "Other"])
        if platform == "Other":
            platform = st.text_input("Custom platform")
    with col2:
        handle = st.text_input("Username/Handle/URL")
    
    digital_notes = st.text_area("Notes", key="digital_notes")
    
    if st.button("Add Digital Footprint"):
        if handle:
            st.session_state.extracted_data['digital_footprint'].append({
                'value': f"{platform}: {handle}",
                'platform': platform,
                'handle': handle,
                'notes': digital_notes,
                'source': 'Manual Entry',
                'entity_type': 'DIGITAL',
                'context': []
            })
            st.success(f"Added {platform} profile to digital footprint")
            st.experimental_rerun()

def show_timeline_tab():
    """Display timeline tab."""
    st.subheader("Timeline")
    
    # Collect timeline events from various categories
    timeline_events = []
    
    # Add events from professional background
    for item in st.session_state.extracted_data['professional_background']:
        if 'dates' in item and item['dates']:
            timeline_events.append({
                'date': item['dates'],
                'event': f"Professional: {item['value']}",
                'category': 'Professional',
                'source': item.get('source', 'Unknown')
            })
    
    # Add events from financial info
    for item in st.session_state.extracted_data['financial_info']:
        if 'date' in item and item['date']:
            timeline_events.append({
                'date': item['date'],
                'event': f"Financial: {item['value']}",
                'category': 'Financial',
                'source': item.get('source', 'Unknown')
            })
    
    # Add events from public records
    for item in st.session_state.extracted_data['public_records']:
        if 'date' in item and item['date']:
            timeline_events.append({
                'date': item['date'],
                'event': f"Public Record: {item['value']}",
                'category': 'Public Record',
                'source': item.get('source', 'Unknown')
            })
    
    # Sort events by date if possible
    try:
        timeline_events.sort(key=lambda x: x['date'])
    except:
        # If dates are in inconsistent formats, don't sort
        pass
    
    # Display timeline
    if timeline_events:
        for event in timeline_events:
            col1, col2 = st.columns([1, 3])
            with col1:
                st.write(f"**{event['date']}**")
            with col2:
                st.write(event['event'])
                st.write(f"*Source: {event['source']}*")
            st.divider()
    else:
        st.info("No timeline events available. Add dates to professional background, financial information, or public records.")
    
    # Manual entry
    st.write("Add manually:")
    
    col1, col2 = st.columns(2)
    with col1:
        event_date = st.date_input("Date")
    with col2:
        event_type = st.selectbox("Event Type", ["Personal", "Professional", "Financial", "Legal", "Other"])
    
    event_description = st.text_input("Event Description")
    event_notes = st.text_area("Notes", key="event_notes")
    
    if st.button("Add Timeline Event"):
        if event_description:
            # Determine which category to add to based on event type
            if event_type == "Professional":
                category = 'professional_background'
            elif event_type == "Financial":
                category = 'financial_info'
            elif event_type == "Legal":
                category = 'public_records'
            else:
                # Default to inconsistencies as a catch-all
                category = 'inconsistencies'
            
            st.session_state.extracted_data[category].append({
                'value': event_description,
                'date': event_date.strftime("%Y-%m-%d"),
                'type': event_type,
                'notes': event_notes,
                'source': 'Manual Entry',
                'entity_type': 'EVENT',
                'context': []
            })
            st.success(f"Added event to timeline")
            st.experimental_rerun()
