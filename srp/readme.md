# Ship Weapon Loader Dashboard

This is a Streamlit application that allows users to manage and load weapons onto different ships. The application provides a user-friendly interface to view ship information, select weapons to load, and monitor the progress of each ship's journey.

## Features

- **Ship Selection**: Select a ship from the available list to view its details.
- **Ship Information**: View comprehensive information about the selected ship, including its name, vessel type, total weapon space, load location, and origin/destination countries.
- **Weapon Loading**: Add weapons to the selected ship by choosing from the available weapon types. The application calculates the total loaded space and remaining available space.
- **Load Duration**: The application displays the total load duration after adding new weapons, considering the loading time for each weapon type.
- **Combined Weapons Table**: View a table that combines the already loaded weapons and the newly added weapons, along with the total weapon counts and space allocation.
- **Weapon Space Allocation Chart**: A bar chart visualizes the allocation of weapon space across different weapon types and the remaining space left.
- **Journey Progress**: Monitor the progress of the selected ship's journey with a progress bar chart that includes a ship icon indicating the current location.

## Getting Started

1. Clone the repository or download the source code.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Run the Streamlit application with `streamlit run app.py`.
4. The application will open in your default web browser.

## Dependencies

The application relies on the following Python libraries:

- Pandas
- Streamlit
- NumPy
- Altair
- Pillow

## Data

The application uses fake data frames for ships, weapons, and ship routes. The data is defined within the code itself.

## Contributing

Contributions to this project are welcome. If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
