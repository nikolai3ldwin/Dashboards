import streamlit as st

# Install required packages if not present
import subprocess
import sys

def install_packages():
    packages = ['folium', 'streamlit-folium', 'mgrs']
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import folium
    from streamlit_folium import folium_static
    from mgrs import MGRS
except ImportError:
    install_packages()
    import folium
    from streamlit_folium import folium_static
    from mgrs import MGRS

import pandas as pd
import numpy as np

# Function to convert MGRS to lat/lon
def mgrs_to_latlon(mgrs_string):
    m = MGRS()
    try:
        # Remove spaces from MGRS string
        mgrs_clean = mgrs_string.replace(" ", "")
        lat, lon = m.toLatLon(mgrs_clean)
        return lat, lon
    except:
        # Return approximate coordinates for Wallis and Futuna if conversion fails
        return -13.3, -176.2

# Create dataframes for each category
political_data = {
    'name': ['Territorial Assembly', 'French Administration HQ', 'Uvea Royal Palace', 'Mata-Utu Town Hall'],
    'location': ['Main legislative building, Mata-Utu', 'Prefect\'s office, Mata-Utu', 'Traditional king\'s residence', 'Municipal administration'],
    'mgrs': ['01LAR 82345 67890', '01LAR 82346 67892', '01LAR 82340 67885', '01LAR 82348 67895'],
    'category': ['Political'] * 4
}

transportation_data = {
    'name': ['Hihifo Airport', 'Mata-Utu Port', 'Vele Airport (Futuna)', 'Port of Leava (Futuna)'],
    'location': ['Main international airport', 'Main commercial seaport', 'Secondary airport', 'Secondary seaport'],
    'mgrs': ['01LAR 82320 67940', '01LAR 82350 67870', '01LAR 83450 66780', '01LAR 83455 66785'],
    'category': ['Transportation'] * 4
}

security_data = {
    'name': ['Main Gendarmerie Station', 'Emergency Response Center', 'Maritime Surveillance Post'],
    'location': ['Central police facility', 'Disaster management HQ', 'Coastal monitoring'],
    'mgrs': ['01LAR 82347 67893', '01LAR 82349 67894', '01LAR 82351 67871'],
    'category': ['Security'] * 3
}

healthcare_data = {
    'name': ['Sia Hospital', 'Northern Dispensary', 'Southern Dispensary'],
    'location': ['Main medical facility', 'Medical outpost', 'Medical outpost'],
    'mgrs': ['01LAR 82344 67888', '01LAR 82330 67920', '01LAR 82360 67860'],
    'category': ['Healthcare'] * 3
}

cultural_data = {
    'name': ['Cathedral of Mata-Utu', 'Traditional Meeting Ground', 'Royal Tomb'],
    'location': ['Main Catholic church', 'Cultural ceremonies site', 'Historical site'],
    'mgrs': ['01LAR 82343 67887', '01LAR 82341 67886', '01LAR 82342 67884'],
    'category': ['Cultural'] * 3
}

communications_data = {
    'name': ['Main Communications Tower', 'Radio Wallis et Futuna', 'Satellite Ground Station'],
    'location': ['Central telecom facility', 'Broadcasting station', 'International comms'],
    'mgrs': ['01LAR 82352 67872', '01LAR 82353 67873', '01LAR 82354 67874'],
    'category': ['Communications'] * 3
}

environmental_data = {
    'name': ['Marine Protected Area HQ', 'Lalolalo Lake', 'Coastal Conservation Zone'],
    'location': ['Conservation center', 'Protected crater lake', 'Marine sanctuary office'],
    'mgrs': ['01LAR 82355 67875', '01LAR 82325 67930', '01LAR 82356 67876'],
    'category': ['Environmental'] * 3
}

utilities_data = {
    'name': ['Main Power Plant', 'Water Treatment Plant', 'Fuel Storage Facility'],
    'location': ['Primary generation facility', 'Central facility', 'Strategic reserves'],
    'mgrs': ['01LAR 82357 67877', '01LAR 82358 67878', '01LAR 82359 67879'],
    'category': ['Utilities'] * 3
}

economic_data = {
    'name': ['Central Market', 'Handicraft Center', 'Government Treasury'],
    'location': ['Main commercial center', 'Traditional crafts', 'Financial center'],
    'mgrs': ['01LAR 82361 67881', '01LAR 82362 67882', '01LAR 82363 67883'],
    'category': ['Economic'] * 3
}

# Combine all dataframes
all_dfs = []
for data in [political_data, transportation_data, security_data, healthcare_data, 
             cultural_data, communications_data, environmental_data, utilities_data, 
             economic_data]:
    all_dfs.append(pd.DataFrame(data))

df = pd.concat(all_dfs, ignore_index=True)

# Convert MGRS coordinates to lat/lon
df[['latitude', 'longitude']] = df['mgrs'].apply(lambda x: pd.Series(mgrs_to_latlon(x)))

# Define color scheme for categories
color_scheme = {
    'Political': 'red',
    'Transportation': 'blue',
    'Security': 'green',
    'Healthcare': 'white',
    'Cultural': 'purple',
    'Communications': 'orange',
    'Environmental': 'lightgreen',
    'Utilities': 'gray',
    'Economic': 'yellow'
}

# Set page config
st.set_page_config(page_title="Wallis and Futuna Infrastructure", layout="wide")

# Main title
st.title('Wallis and Futuna Infrastructure Map')

# Create two columns for layout
col1, col2 = st.columns([3, 1])

# Sidebar filters
with col2:
    st.subheader('Filters')
    selected_categories = st.multiselect(
        'Select Categories',
        df['category'].unique(),
        default=df['category'].unique()
    )

    # Search box
    search_term = st.text_input('Search locations')

    # Show data table option
    show_table = st.checkbox('Show Data Table', value=True)

# Filter data based on selection and search
filtered_df = df[df['category'].isin(selected_categories)]
if search_term:
    filtered_df = filtered_df[filtered_df['name'].str.contains(search_term, case=False) |
                            filtered_df['location'].str.contains(search_term, case=False)]

# Create map
with col1:
    m = folium.Map(location=[-13.3, -176.2], zoom_start=11)

    # Add markers to map
    for idx, row in filtered_df.iterrows():
        folium.Marker(
            [row['latitude'], row['longitude']],
            popup=folium.Popup(
                f"""
                <b>{row['name']}</b><br>
                Category: {row['category']}<br>
                Location: {row['location']}<br>
                MGRS: {row['mgrs']}
                """,
                max_width=300
            ),
            icon=folium.Icon(color=color_scheme[row['category']], icon='info-sign'),
            tooltip=row['name']
        ).add_to(m)

    # Display map
    folium_static(m, width=800)

# Display data table if checked
if show_table:
    st.subheader('Location Details')
    st.dataframe(
        filtered_df[['name', 'location', 'category', 'mgrs']],
        hide_index=True,
        use_container_width=True
    )

# Add legend
st.sidebar.subheader('Legend')
for category, color in color_scheme.items():
    st.sidebar.markdown(
        f'<span style="color:{color}">●</span> {category}',
        unsafe_allow_html=True
    )
