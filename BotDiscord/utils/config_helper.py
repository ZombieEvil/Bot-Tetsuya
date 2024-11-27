# utils/config_helper.py

import json
import os

CONFIG_FILE = 'config.json'

def load_config():
    if not os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as f:
            json.dump({}, f)
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Fichier vide ou JSON invalide
        print("Le fichier config.json est vide ou corrompu. Réinitialisation du fichier.")
        with open(CONFIG_FILE, 'w') as f:
            json.dump({}, f)
        return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def save_channel_id(guild_id, channel_id):
    config = load_config()
    config[guild_id] = {'channel_id': channel_id}
    save_config(config)

def get_channel_id(guild_id):
    config = load_config()
    return config.get(guild_id, {}).get('channel_id')
