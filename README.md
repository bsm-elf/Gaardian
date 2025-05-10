
# Gaardian

![Gaardian Logo](https://github.com/bsm-elf/ArrGuardian/raw/main/frontend/src/Gaardian.png)

Gaardian is an automated queue management tool for Sonarr and Radarr instances. It monitors *Arr queues to detect stalled or problematic items and can automatically clean up these items, improving the efficiency of your media server.

## Features

- Automated removal of stalled, failed, or unparsable items
- Supports multiple Sonarr and Radarr instances (including 4K versions)
- Configurable settings via a modern web UI
- Real-time queue monitoring and management
- Docker and Kubernetes ready for easy deployment

## Installation

### Prerequisites
- Docker installed on your system
- Access to Sonarr and Radarr instances with API keys

### Docker Compose Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/bsm-elf/ArrGuardian.git
   cd ArrGuardian
   ```
2. Update the API keys and instance URLs in `settings.json`:
   ```json
   "arr_instances": [
       {"name": "Sonarr", "url": "http://sonarr:8989", "api_key": "YOUR_SONARR_API_KEY"},
       {"name": "Sonarr4K", "url": "http://sonarr4k:8989", "api_key": "YOUR_SONARR4K_API_KEY"},
       {"name": "Radarr", "url": "http://radarr:7878", "api_key": "YOUR_RADARR_API_KEY"},
       {"name": "Radarr4K", "url": "http://radarr4k:7878", "api_key": "YOUR_RADARR4K_API_KEY"}
   ]
   ```
3. Build and run the Docker containers:
   ```bash
   docker-compose up --build
   ```
4. Access the web UI at:
   ```
   http://localhost:3000
   ```

## Configuration
You can customize the settings directly from the web UI, including:
- Enabling/Disabling removal of stalled or problematic items
- Log level adjustment (info, debug, warning, error)
- Managing multiple *Arr instances

## Usage
Simply navigate to the Gaardian web UI and manage your *Arr queues. Toggle the settings as needed to customize your automation preferences.

## Contributing
Feel free to open issues and pull requests on [GitHub](https://github.com/bsm-elf/ArrGuardian).

## License
This project is licensed under the MIT License.
