import json
import os

CONFIG_FILE = "config.json"
LAST_ANIME_FILE = "last_anime.json"


def load_config():
    """Charge la configuration depuis le fichier JSON."""
    if not os.path.exists(CONFIG_FILE):
        print(f"Le fichier {CONFIG_FILE} n'existe pas. Création d'un nouveau fichier.")
        save_config({})
        return {}

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Le fichier {CONFIG_FILE} est corrompu. Réinitialisation.")
        save_config({})
        return {}


def save_config(config):
    """Sauvegarde la configuration dans le fichier JSON."""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)


def load_last_anime():
    """Charge le dernier anime annoncé depuis le fichier JSON."""
    if not os.path.exists(LAST_ANIME_FILE):
        print(f"Le fichier {LAST_ANIME_FILE} n'existe pas. Aucun dernier anime enregistré.")
        return None

    try:
        with open(LAST_ANIME_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Le fichier {LAST_ANIME_FILE} est corrompu. Réinitialisation.")
        save_last_anime({})
        return None


def save_last_anime(last_anime):
    """Sauvegarde le dernier anime annoncé dans le fichier JSON."""
    with open(LAST_ANIME_FILE, "w", encoding="utf-8") as f:
        json.dump(last_anime, f, indent=4, ensure_ascii=False)
