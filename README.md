# ArrGuardian

## Project Overview

ArrGuardian is an automated management tool for Sonarr and Radarr queues, designed to help users maintain a clean and efficient download environment. It automatically handles common queue issues and removes problematic items based on user-defined settings.

## Features

* Automated removal of problematic queue items from Sonarr and Radarr.
* Support for multiple instances: Sonarr, Sonarr4K, Radarr, Radarr4K.
* Auto-import for manually approved items and custom format upgrades.
* Handles common errors, including unparsable items and qBittorrent errors.
* Web-based dashboard for real-time monitoring and configuration.
* Easy-to-use settings management through the UI.

## Requirements

* Docker
* Docker Compose
* Node.js and npm (for development)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/ArrGuardian.git
   cd ArrGuardian
   ```
2. Make sure Docker and Docker Compose are installed:

   ```bash
   docker --version
   docker-compose --version
   ```

## Running the App

1. Build and start the containers:

   ```bash
   docker-compose up --build
   ```
2. Access the frontend at:

   ```
   ```

[http://localhost:3000](http://localhost:3000)

```
3. Access the backend API (for testing) at:
```

[http://localhost:8000/api/health](http://localhost:8000/api/health)

```

## Configuration
- The settings file is automatically generated at startup and stored in the `/data` directory as `settings.json`.
- Settings can be modified through the web UI or by directly editing the JSON file.
- Available settings include:
- Dry Run (preview actions without executing)
- Enable Removal
- Auto Import Manual
- Auto Handle Custom Format
- Auto Remove Unparsable
- Auto Remove qBittorrent Error
- Log Level (info, debug, warning, error)

## Usage
- Open the ArrGuardian dashboard at `http://localhost:3000`.
- Enable or disable features via the settings page.
- Monitor queue items and remove problematic ones with a single click.

## Contributing
Contributions are welcome! Feel free to open issues and submit pull requests.

## License
This project is licensed under the MIT License.

```
