from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import requests
from pydantic import BaseModel

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

SETTINGS_FILE = "/app/data/settings.json"

class Settings(BaseModel):
    dry_run: bool = False
    enable_removal: bool = True
    auto_import_manual: bool = True
    auto_handle_custom_format: bool = True
    auto_remove_unparsable: bool = True
    auto_remove_qbt_error: bool = True
    log_level: str = "info"
    arr_instances: list = []

def load_settings():
    try:
        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {
            "dry_run": False,
            "enable_removal": True,
            "auto_import_manual": True,
            "auto_handle_custom_format": True,
            "auto_remove_unparsable": True,
            "auto_remove_qbt_error": True,
            "log_level": "info",
            "arr_instances": [
                {"name": "Sonarr", "url": "http://sonarr:8989", "api_key": "YOUR_SONARR_API_KEY"},
                {"name": "Sonarr4K", "url": "http://sonarr4k:8989", "api_key": "YOUR_SONARR4K_API_KEY"},
                {"name": "Radarr", "url": "http://radarr:7878", "api_key": "YOUR_RADARR_API_KEY"},
                {"name": "Radarr4K", "url": "http://radarr4k:7878", "api_key": "YOUR_RADARR4K_API_KEY"}
            ]
        }
        save_settings(settings)
    return settings

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

settings = load_settings()

@app.get("/api/health")
def health_check():
    return {"status": "Gaardian is running"}

@app.get("/api/settings")
def get_settings():
    return settings

@app.post("/api/settings")
def update_settings(new_settings: Settings):
    global settings
    settings = new_settings.dict()
    save_settings(settings)
    return {"message": "Settings updated"}

@app.get("/api/queue")
def get_queue():
    all_queue = []
    for instance in settings.get("arr_instances", []):
        try:
            response = requests.get(f"{instance['url']}/api/v3/queue", headers={"X-Api-Key": instance["api_key"]})
            response.raise_for_status()
            all_queue.extend(response.json())
        except requests.RequestException as e:
            print(f"Error fetching queue from {instance['name']}: {e}")
    return all_queue
