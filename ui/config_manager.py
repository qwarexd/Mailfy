import json
import os

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "server_ip": "26.156.206.250",
    "away_timeout": 300
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return DEFAULT_CONFIG.copy()

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)