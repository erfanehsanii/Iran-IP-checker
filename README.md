# IP Checker and Chrome Closer

This is a Python application that periodically checks the current IP address of the machine and, if the IP is found to be from a specified country (e.g., Iran), it will close any running instances of Google Chrome. This can be useful in situations where internet access needs to be restricted based on geographic location.

## Features

- Retrieves the current IP address.
- Checks the geolocation of the IP address.
- Monitors and identifies running Google Chrome processes.
- Automatically closes Google Chrome if the IP address is from a specified country.
- Simple and user-friendly GUI using Tkinter.

## Requirements

- Python 3.6 or higher
- `requests` library
- `psutil` library
- `tkinter` library (usually included with Python)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/ip-checker-chrome-closer.git
    cd ip-checker-chrome-closer
    ```

2. Install the required libraries:
    ```bash
    pip install requests psutil
    ```

## Usage

1. Run the script:
    ```bash
    python main.py
    ```

2. The GUI window will open. Click the "Start" button to begin checking the IP address and monitoring Google Chrome processes.

3. The application will periodically check the IP address and, if the IP is from the specified country (e.g., Iran), it will close any running instances of Google Chrome.

## Code Description

### `main.py`

This is the main script that initializes the Tkinter GUI and contains the core functionality of the application.

#### Classes and Methods:

- **App**: Main application class that initializes the GUI and handles the functionality.
  - `__init__(self, root)`: Initializes the GUI components.
  - `get_ip_address(self)`: Retrieves the current IP address using the `requests` library.
  - `get_geolocation(self, ip)`: Gets the geolocation information for the given IP address.
  - `is_chrome_running(self)`: Checks if any Google Chrome processes are running.
  - `close_chrome(self)`: Attempts to close any running Google Chrome processes.
  - `check_ip(self)`: Periodically checks the IP address and closes Chrome if the IP is from a specified country.
  - `start(self)`: Starts the IP checking and Chrome monitoring process.
  - `stop(self)`: Stops the IP checking and Chrome monitoring process.

### How It Works:

1. **IP Retrieval**: The application retrieves the current IP address using the `requests` library and the `https://api.ipify.org?format=json` endpoint.
2. **Geolocation Check**: It then checks the geolocation of the IP address using the `http://ip-api.com/json/{ip}` endpoint.
3. **Chrome Monitoring**: If the IP address is from the specified country, the application checks for any running Google Chrome processes using the `psutil` library.
4. **Process Termination**: If Google Chrome is running, the application attempts to close the Chrome processes.

## Troubleshooting

- **Permissions**: Ensure the script is run with sufficient permissions to manage processes. On Windows, you might need to run the script as an administrator.
- **Dependencies**: Make sure all required libraries are installed. You can install them using the provided `pip` commands.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

