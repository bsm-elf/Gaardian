
# Gaardian

![Gaardian Logo](./Gaardian.png)

Gaardian is a management tool for *Arr applications (Sonarr, Radarr, Sonarr4K, Radarr4K) designed to automatically clean up problematic items from the queues. It supports multiple instances and can be run locally or in a Kubernetes environment.

## Features
- Automated removal of problematic queue items (stalled, failed, unparsable)
- Supports multiple Sonarr and Radarr instances
- Easily configurable settings through the UI and JSON file
- Dockerized for easy deployment
- Modern, responsive frontend dashboard

## Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/gaardian.git
   ```
2. Update the `settings.json` file with your *Arr instances and API keys.
3. Build and run using Docker:
   ```bash
   docker-compose up --build
   ```

## Configuration
Gaardian settings can be modified from the UI or by editing the `settings.json` file directly.

## License
MIT License
