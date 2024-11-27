import time
import json
import os
import aiohttp
import asyncio
from datetime import datetime
from utils.config_helper import load_config

LAST_ANIME_FILE = 'last_anime.json'


def save_last_anime(anime_data):
    """Sauvegarde les informations du dernier anime annoncé dans un fichier."""
    with open(LAST_ANIME_FILE, 'w') as f:
        json.dump(anime_data, f, indent=4)


def get_last_anime():
    """Récupère les informations du dernier anime annoncé depuis un fichier."""
    if os.path.exists(LAST_ANIME_FILE):
        with open(LAST_ANIME_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return None
    return None


async def fetch_anime_data():
    """Récupère les données des animes depuis l'API AniList."""
    current_timestamp = int(time.time())
    query = '''
    query {
      Page(perPage: 50) {
        airingSchedules(airingAt_greater: %d, sort: TIME) {
          media {
            id
            title {
              romaji
              english
            }
            season
            coverImage {
              extraLarge
            }
          }
          episode
          airingAt
        }
      }
    }
    ''' % current_timestamp

    url = 'https://graphql.anilist.co'
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json={'query': query}) as response:
            return await response.json()


async def display_next_anime_timer(airing_schedules, bot):
    """Gère l'annonce des épisodes et met à jour le timer pour le prochain."""
    while airing_schedules:
        # Prendre le premier anime de la liste
        next_anime = airing_schedules.pop(0)
        title = next_anime['media']['title']['romaji'] or next_anime['media']['title']['english']
        episode = next_anime['episode']
        airing_time = next_anime['airingAt']
        formatted_time = datetime.fromtimestamp(airing_time).strftime('%Y-%m-%d %H:%M:%S')

        print(f"\nLancement du timer pour : {title} (Épisode {episode}) (Diffusion prévue à {formatted_time})")

        # Timer avant l'annonce
        while time.time() < airing_time:
            remaining_time = airing_time - time.time()
            hours, remainder = divmod(int(remaining_time), 3600)
            minutes, seconds = divmod(remainder, 60)
            print(f"Prochain anime : {title} dans : {hours}h {minutes}m {seconds}s", end="\r")
            await asyncio.sleep(1)

        print(f"\nLe prochain anime ({title}, Épisode {episode}) est en cours d'annonce.")
        await announce_anime_now(next_anime, bot)

    print("Aucun autre anime à venir pour le moment.")


async def announce_anime_now(schedule, bot):
    """Envoie immédiatement une annonce pour un anime."""
    config = load_config()
    anime_title = schedule['media']['title']['romaji'] or schedule['media']['title']['english']
    episode = schedule['episode']
    season = schedule['media'].get('season', "Inconnue")
    airing_time = datetime.fromtimestamp(schedule['airingAt']).strftime('%Y-%m-%d %H:%M:%S')

    embed = discord.Embed(
        title=f"{anime_title}",
        description=f"L'épisode **{episode}** de la saison **{season}** de **{anime_title}** vient de sortir !",
        color=discord.Color.blue(),
    )
    embed.set_image(url=schedule['media']['coverImage']['extraLarge'])
    embed.set_footer(text=f"Sorti le : {airing_time}")

    for guild_id, guild_config in config.items():
        channel = bot.get_channel(guild_config['channel_id'])
        if channel:
            try:
                await channel.send(embed=embed)
                print(f"Annonce envoyée pour {anime_title} dans {channel.name}.")
                # Sauvegarder le dernier anime annoncé
                save_last_anime({
                    'title': anime_title,
                    'episode': episode,
                    'airingAt': schedule['airingAt']
                })
            except Exception as e:
                print(f"Erreur lors de l'envoi de l'annonce pour {anime_title} : {e}")
