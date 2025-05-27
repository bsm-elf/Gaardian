import os
import json
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

        # Override URLs with environment variables if set
        for instance in settings.get("arr_instances", []):
            env_url = os.getenv(f"{instance['name'].upper()}_URL")
            if env_url:
                instance["url"] = env_url

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
    return settings

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

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

@app.get("/api/queue")
def get_queue():
    all_queue = []
    for instance in settings.get("arr_instances", []):
        try:
            response = requests.get(f"{instance['url']}/api/v3/queue", headers={"X-Api-Key": instance["api_key"]})
            response.raise_for_status()
            queue_items = response.json()
            all_queue.extend(queue_items)
        except requests.RequestException as e:
            print(f"Error fetching queue from {instance['name']}: {e}")
            return {"error": f"Error fetching queue from {instance['name']}"}
    return {"queue": all_queue}

@app.get("/api/logs")
def get_logs():
    try:
        with open("/app/data/arrguardian.log", "r") as f:
            logs = f.readlines()
        return {"logs": logs}
    except FileNotFoundError:
        return {"error": "Log file not found"}
