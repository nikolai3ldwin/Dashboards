import pandas as pd
import streamlit as st
import numpy as np
import altair as alt
from PIL import Image
from math import radians, cos, sin, asin, sqrt

# Define the fake data frames
df_ships = pd.DataFrame({
    'Ship_Name': ['Sea Warrior', 'Liberty', 'Freedom', 'Independence', 'Defender'],
    'Vessel_Type': ['Destroyer', 'Frigate', 'Cruiser', 'Carrier', 'Submarine'],
    'Ship_Total_Weapon_Space': [500, 200, 600, 1200, 300],
    'Load_Location': ['Pearl Harbor', 'San Diego', 'Norfolk', 'Yokosuka', 'Guam'],
    'Load_Latitude': [21.3442, 32.7157, 36.8508, 35.2815, 13.444],
    'Load_Longitude': [-157.974, -117.161, -76.2859, 139.672, 144.793],
    'Country_of_Origin': ['USA', 'USA', 'USA', 'USA', 'USA'],
    'Country_of_Destination': ['Japan', 'Australia', 'South Korea', 'Philippines', 'Taiwan'],
    'Loaded_Weapons': [[('Missiles', 2), ('Cannons', 1)], [('Missiles', 1)], [('Torpedoes', 3)], [('Missiles', 2), ('Aircraft', 1)], [('Torpedoes', 2)]]
})

df_weapons = pd.DataFrame({
    'Weapon_Type': ['Missiles', 'Torpedoes', 'Cannons', 'Aircraft'],
    'Weapon_Space': [100, 50, 150, 300],
    'Weapon_Type_Load_Duration': ['2 hours', '1.5 hours', '3 hours', '4 hours'],
    'Load_Location': ['Pearl Harbor', 'San Diego', 'Norfolk', 'Yokosuka'],
    'Load_Latitude': [21.3442, 32.7157, 36.8508, 35.2815],
    'Load_Longitude': [-157.974, -117.161, -76.2859, 139.672],
    'Country': ['USA', 'USA', 'USA', 'USA']
})

df_ship_routes = pd.DataFrame({
    'Ship_Name': ['Sea Warrior', 'Liberty', 'Freedom', 'Independence', 'Defender'],
    'Load_Location': ['Pearl Harbor', 'San Diego', 'Norfolk', 'Yokosuka', 'Guam'],
    'Load_Latitude': [21.3442, 32.7157, 36.8508, 35.2815, 13.444],
    'Load_Longitude': [-157.974, -117.161, -76.2859, 139.672, 144.793],
    'Target_Location': ['Tokyo', 'Sydney', 'Busan', 'Manila', 'Taipei'],
    'Target_Latitude': [35.6895, -33.8688, 35.1028, 14.5995, 25.0330],
    'Target_Longitude': [139.6917, 151.2093, 129.0416, 120.9842, 121.5654],
    'Current_Location': ['Pacific Ocean', 'Pacific Ocean', 'Atlantic Ocean', 'Pacific Ocean', 'Pacific Ocean'],
    'Current_Latitude': [25.0, 20.0, 30.0, 40.0, 15.0],
    'Current_Longitude': [-160.0, -140.0, -70.0, 160.0, 150.0],
    'Progress': [0.3, 0.6, 0.8, 0.2, 0.5]
})


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r


def main():
    st.title('Ship Weapon Loader Dashboard')

    # Select ship
    selected_ship = st.selectbox('Select Ship:', df_ships['Ship_Name'])

    # Display ship information
    ship_info = df_ships[df_ships['Ship_Name'] == selected_ship].squeeze()
    st.write('### Ship Information')
    st.write(f'**Ship Name:** {ship_info["Ship_Name"]}')
    st.write(f'**Vessel Type:** {ship_info["Vessel_Type"]}')
    st.write(
        f'**Total Weapon Space:** {ship_info["Ship_Total_Weapon_Space"]} units')
    st.write(
        f'**Load Location:** {ship_info["Load_Location"]} ({ship_info["Load_Latitude"]}, {ship_info["Load_Longitude"]})')
    st.write('---')

    # Calculate available space
    loaded_space = sum(count * df_weapons.loc[df_weapons['Weapon_Type'] == weapon,
                       'Weapon_Space'].iloc[0] for weapon, count in ship_info['Loaded_Weapons'])
    available_space = ship_info["Ship_Total_Weapon_Space"] - loaded_space

    # Select weapons to load
    st.write('### Add Weapons')
    st.write(f'**Available Space:** {available_space} units')
    with st.expander("Expand to Add Weapons"):
        selected_weapons = {}
        for index, row in df_weapons.iterrows():
            weapon_type = row['Weapon_Type']
            weapon_space = row['Weapon_Space']
            # Limit to 3 weapons per type or available space
            max_count = min(int(available_space / weapon_space), 3)
            selected_count = st.number_input(
                f'{weapon_type} ({weapon_space} space)', min_value=0, max_value=max_count, value=0)
            selected_weapons[weapon_type] = selected_count

            # Check if adding this weapon exceeds available space
            total_load_space = sum(
                selected_weapons[w] * df_weapons.loc[df_weapons['Weapon_Type'] == w, 'Weapon_Space'].iloc[0] for w in selected_weapons)
            if total_load_space > available_space:
                st.warning(
                    'Adding this weapon system exceeds the available space. Please adjust your selection.')
                selected_weapons[weapon_type] = 0  # Reset the selected count

    # Calculate total loaded space
    total_loaded_space = sum(selected_weapons.values())

    # Display total loaded space
    st.write(f'**Total Loaded Space:** {total_loaded_space} units')
    st.write('---')

    # Display total load duration after adding new weapons
    total_load_duration = sum(selected_count * pd.Timedelta(df_weapons.loc[df_weapons['Weapon_Type'] == weapon,
                              'Weapon_Type_Load_Duration'].iloc[0]).total_seconds() for weapon, selected_count in selected_weapons.items())
    st.write('### Total Load Duration After Adding New Weapons')
    st.write(
        f'**Total Load Duration:** {pd.Timedelta(seconds=total_load_duration)}')

    # Update already loaded weapons based on the selected weapons
    updated_loaded_weapons = [
        (weapon, count) for weapon, count in selected_weapons.items() if count > 0]
    df_ships.loc[df_ships['Ship_Name'] == selected_ship,
                 'Loaded_Weapons'] = str(updated_loaded_weapons)

    # Create a dataframe for already loaded and newly added weapons
    loaded_dict = dict(ship_info['Loaded_Weapons'])
    new_dict = {k: selected_weapons.get(k, 0) for k in set(
        loaded_dict) | set(selected_weapons)}
    total_dict = {k: loaded_dict.get(k, 0) + new_dict.get(k, 0)
                  for k in set(loaded_dict) | set(new_dict)}
    df_combined = pd.DataFrame(
        {'Already Loaded': loaded_dict, 'Newly Added': new_dict, 'Total': total_dict}).fillna(0)
    df_combined['Weapon_Space'] = df_combined.index.map(
        lambda x: df_weapons[df_weapons['Weapon_Type'] == x]['Weapon_Space'].iloc[0])
    df_combined['Total Space'] = df_combined['Total'] * \
        df_combined['Weapon_Space']

    # Calculate total space left
    total_space_left = ship_info["Ship_Total_Weapon_Space"] - \
        df_combined['Total Space'].sum()
    # Ensure total space left is not negative
    total_space_left = max(total_space_left, 0)
    st.write(f'**Total Space Left:** {total_space_left} units')

    # Display the combined dataframe
    st.write('### Combined Weapons Table')
    st.write(df_combined)

    # Create a bar chart for weapon space allocation
    weapon_space_data = pd.DataFrame({
        'Weapon Type': df_combined.index.tolist() + ['Total Space Left'],
        'Total Space': df_combined['Total Space'].tolist() + [total_space_left]
    })

    bar_chart = alt.Chart(weapon_space_data).mark_bar().encode(
        x='Weapon Type',
        y='Total Space',
        tooltip=['Weapon Type', 'Total Space']
    ).properties(
        width=600,
        height=400,
        title='Weapon Space Allocation'
    )

    st.altair_chart(bar_chart, use_container_width=True)

    # Get the selected ship's route information
    ship_route = df_ship_routes[df_ship_routes['Ship_Name']
                                == selected_ship].squeeze()

    # Calculate the total distance of the route
    start_lat, start_lon = ship_route['Load_Latitude'], ship_route['Load_Longitude']
    end_lat, end_lon = ship_route['Target_Latitude'], ship_route['Target_Longitude']
    total_distance = haversine(start_lon, start_lat, end_lon, end_lat)

    # Create a progress bar chart
    progress_data = pd.DataFrame({
        'Ship': [selected_ship],
        'Progress': [ship_route['Progress']]
    })

    progress_bar = alt.Chart(progress_data).mark_bar().encode(
        x='Ship',
        x2='Progress',
        y=alt.Y('Progress:Q', axis=None),
        tooltip=['Ship', alt.Tooltip('Progress', format='.2f')]
    ).properties(
        width=600,
        height=50,
        title='Journey Progress'
    )

    # Add the ship image to the chart
    ship_image = Image.open("C:/Users/baldw/Downloads/Boat Icon.png")
    ship_x = int(ship_route['Progress'] * 600)
    progress_bar = progress_bar.mark_image(
        url='data:image/png;base64,' + ship_image.tobytes().decode('latin1'),
        x=ship_x,
        y=25,
        width=50,
        height=50
    )

    st.altair_chart(progress_bar, use_container_width=True)


if __name__ == '__main__':
    main()
