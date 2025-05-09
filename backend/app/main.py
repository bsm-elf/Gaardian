# ArrGuardian - Automated *Arr Queue Management

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests
import json

app = FastAPI(title='ArrGuardian')

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Configuration from Environment Variables
SONARR_URL = os.getenv('SONARR_URL', 'http://sonarr:8989')
SONARR4K_URL = os.getenv('SONARR4K_URL', 'http://sonarr4k:8989')
RADARR_URL = os.getenv('RADARR_URL', 'http://radarr:7878')
RADARR4K_URL = os.getenv('RADARR4K_URL', 'http://radarr4k:7878')
QBITTORRENT_HOST = os.getenv('QBITTORRENT_HOST', 'qBittorrent')
QBITTORRENT_PORT = os.getenv('QBITTORRENT_PORT', '8080')

# Settings file location
SETTINGS_FILE = '/data/settings.json'

# Save settings to file
def save_settings(new_settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(new_settings, f)

# Load or initialize settings
def load_settings():
    default_settings = {
        'dry_run': False,
        'enable_removal': True,
        'auto_import_manual': True,
        'auto_handle_custom_format': True,
        'auto_remove_unparsable': True,
        'auto_remove_qbt_error': True,
        'log_level': 'info'
    }
    try:
        if not os.path.exists(SETTINGS_FILE):
            save_settings(default_settings)
            return default_settings
        with open(SETTINGS_FILE, 'r') as f:
            loaded_settings = json.load(f)
            # Ensure all settings exist
            for key, value in default_settings.items():
                if key not in loaded_settings:
                    loaded_settings[key] = value
            save_settings(loaded_settings)
            return loaded_settings
    except (FileNotFoundError, json.JSONDecodeError):
        save_settings(default_settings)
        return default_settings

settings = load_settings()

# Basic Health Check
@app.get('/api/health')
def health_check():
    return {'status': 'ArrGuardian is running'}

# Get Settings
@app.get('/api/settings')
def get_settings():
    return settings

# Update Settings
@app.post('/api/settings')
def update_settings(new_settings: dict):
    global settings
    settings.update(new_settings)
    save_settings(settings)
    return {'message': 'Settings updated successfully'}

# Model for Queue Item
class QueueItem(BaseModel):
    title: str
    status: str
    message: str

# Fetching Queue Items from Sonarr and Radarr
@app.get('/api/queue')
def get_queue():
    try:
        sonarr_queue = requests.get(f'{SONARR_URL}/api/v3/queue').json()
        radarr_queue = requests.get(f'{RADARR_URL}/api/v3/queue').json()
        return {'sonarr_queue': sonarr_queue, 'radarr_queue': radarr_queue}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Removing Problematic Item from qBittorrent
@app.post('/api/queue/remove')
def remove_item(item: QueueItem):
    try:
        if settings.get('dry_run', False):
            return {'message': f'Dry run: {item.title} would be removed'}

        # Handle specific removal scenarios
        if "Manual Import required" in item.message and settings.get('auto_import_manual', False):
            return {'message': f'Auto approved: {item.title} for import'}
        if "Not a Custom Format upgrade" in item.message and settings.get('auto_handle_custom_format', False):
            return {'message': f'Auto approved: {item.title} as similar content'}
        if "Unable to Parse" in item.message and settings.get('auto_remove_unparsable', False):
            return {'message': f'Removed unparsed item: {item.title}'}
        if "qBittorrent is reporting an error" in item.message and settings.get('auto_remove_qbt_error', False):
            return {'message': f'Removed qBittorrent error item: {item.title}'}

        response = requests.delete(f'http://{QBITTORRENT_HOST}:{QBITTORRENT_PORT}/api/v2/torrents/delete?hash={item.title}')
        if response.status_code == 200:
            return {'message': f'Removed item: {item.title}'}
        else:
            raise HTTPException(status_code=500, detail='Failed to remove item')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
