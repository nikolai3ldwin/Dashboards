import pandas as pd
from PySide6.QtWidgets import QApplication, QLabel, QComboBox, QVBoxLayout, QWidget, QPushButton, QLineEdit, QFormLayout
import numpy as np

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


class ShipWeaponLoader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Ship Weapon Loader Dashboard')
        self.layout = QVBoxLayout()
        self.ship_select_label = QLabel('Select Ship:')
        self.ship_select_combo = QComboBox()
        self.ship_select_combo.addItems(df_ships['Ship_Name'])
        self.ship_info_label = QLabel('Ship Information:')
        self.ship_info_display = QLabel('')
        self.add_weapons_label = QLabel('Add Weapons:')
        self.available_space_label = QLabel('')
        self.add_weapons_button = QPushButton('Add Weapons')
        self.add_weapons_button.clicked.connect(self.add_weapons_dialog)

        self.layout.addWidget(self.ship_select_label)
        self.layout.addWidget(self.ship_select_combo)
        self.layout.addWidget(self.ship_info_label)
        self.layout.addWidget(self.ship_info_display)
        self.layout.addWidget(self.add_weapons_label)
        self.layout.addWidget(self.available_space_label)
        self.layout.addWidget(self.add_weapons_button)

        self.setLayout(self.layout)

        self.update_ship_info()

    def update_ship_info(self):
        selected_ship = self.ship_select_combo.currentText()
        ship_info = df_ships[df_ships['Ship_Name'] == selected_ship].squeeze()
        info_text = f"Ship Name: {ship_info['Ship_Name']} \n"
        info_text += f"Vessel Type: {ship_info['Vessel_Type']} \n"
        info_text += f"Total Weapon Space: {ship_info['Ship_Total_Weapon_Space']} units \n"
        info_text += f"Load Location: {ship_info['Load_Location']} ({ship_info['Load_Latitude']}, {ship_info['Load_Longitude']}) \n"
        self.ship_info_display.setText(info_text)
        self.available_space_label.setText(
            f'Available Space: {self.calculate_available_space()} units')

    def calculate_available_space(self):
        selected_ship = self.ship_select_combo.currentText()
        ship_info = df_ships[df_ships['Ship_Name'] == selected_ship].squeeze()
        loaded_space = sum(count * df_weapons.loc[df_weapons['Weapon_Type'] == weapon,
                           'Weapon_Space'].iloc[0] for weapon, count in ship_info['Loaded_Weapons'])
        available_space = ship_info["Ship_Total_Weapon_Space"] - loaded_space
        return available_space

    def add_weapons_dialog(self):
        pass  # Implement the dialog to add weapons here


app = QApplication([])
window = ShipWeaponLoader()
window.show()
app.exec()
