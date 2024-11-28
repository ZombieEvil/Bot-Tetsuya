import time
import json
import os
import asyncio
from datetime import datetime, timedelta
from discord.ext import tasks
from utils.config_helper import load_config

LAST_ANIME_FILE = 'last_anime.json'

# Sauvegarde et récupération des derniers animes
def save_last_anime(anime_data):
    with open(LAST_ANIME_FILE, 'w') as f:
        json.dump(anime_data, f, indent=4)

def get_last_anime():
    if os.path.exists(LAST_ANIME_FILE):
        with open(LAST_ANIME_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return None
    return None

# Simulation de récupération des données
async def fetch_anime_data():
    """Simule la récupération des données depuis une API."""
    # Ajouter ici une vraie requête HTTP si nécessaire
    return [
        {"title": "Wish Cat", "episode": 12, "airing_time": time.time() + 3600},
        {"title": "Jian Lai", "episode": 16, "airing_time": time.time() + 7200},
    ]

# Timer pour les prochaines annonces
async def display_next_anime_timer(bot):
    while True:
        anime_list = await fetch_anime_data()
        current_time = time.time()

        # Trier les animes par temps de diffusion
        upcoming_animes = sorted(anime_list, key=lambda x: x['airing_time'])

        if upcoming_animes:
            next_anime = upcoming_animes[0]
            time_remaining = int(next_anime['airing_time'] - current_time)

            print(f"Prochain anime : {next_anime['title']} dans : {timedelta(seconds=time_remaining)}")

            # Attendre jusqu'à l'heure d'annonce
            await asyncio.sleep(time_remaining)
            channel_id = load_config().get("channel_id")
            if channel_id:
                channel = bot.get_channel(channel_id)
                if channel:
                    await channel.send(f"L'**épisode {next_anime['episode']}** de **{next_anime['title']}** est maintenant disponible !")
                else:
                    print("Impossible de trouver le salon configuré.")
        else:
            print("Aucun anime prévu pour l'instant.")
            await asyncio.sleep(60)  # Vérifie toutes les minutes

# Lancer le planificateur
async def start_scheduler(bot):
    asyncio.create_task(display_next_anime_timer(bot))
