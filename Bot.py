import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
from utils.keep_alive import keep_alive
from utils.scheduler_helper import fetch_anime_data, display_next_anime_timer

# Charger le fichier .env pour récupérer le token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Vérifier si le token est bien chargé
if not TOKEN:
    raise ValueError("Le token Discord n'a pas été trouvé. Assurez-vous qu'il est défini dans le fichier .env.")

# Intents Discord
intents = discord.Intents.default()
intents.message_content = True  # Nécessaire pour permettre au bot de lire le contenu des messages

# Initialiser le bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Charger les extensions
async def load_extensions():
    for extension in ["commands.setchannel", "commands.clear", "commands.last", "commands.upcoming"]:
        try:
            await bot.load_extension(extension)
            print(f"Extension {extension} chargée avec succès.")
        except Exception as e:
            print(f"Erreur lors du chargement de l'extension {extension}: {e}")

# Événement prêt
@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user.name}")
    # Charger les extensions après la connexion
    await load_extensions()
    # Afficher le dernier anime annoncé (via last_anime.json)
    try:
        from utils.scheduler_helper import get_last_anime
        last_anime = get_last_anime()
        if last_anime:
            title = last_anime.get("title", "Inconnu")
            episode = last_anime.get("episode", "Inconnu")
            print(f"Le dernier anime annoncé est : {title} (Épisode {episode})")
        else:
            print("Aucun anime n'a été annoncé précédemment.")
    except Exception as e:
        print(f"Erreur lors de la récupération du dernier anime annoncé : {e}")

    # Afficher le temps restant pour le prochain épisode
    try:
        print("Récupération des informations pour le prochain épisode...")
        data = await fetch_anime_data()
        if data and 'data' in data and 'Page' in data['data']:
            airing_schedules = data['data']['Page']['airingSchedules']
            if airing_schedules:
                print("Liste des animes récupérée avec succès.")
                await display_next_anime_timer(airing_schedules, bot)
            else:
                print("Aucun anime à venir trouvé.")
        else:
            print("Erreur : Impossible de récupérer les données des animes.")
    except Exception as e:
        print(f"Erreur lors de la récupération des informations pour le prochain épisode : {e}")

# Garder le bot actif (Flask serveur)
keep_alive()

# Lancer le bot
try:
    bot.run(TOKEN)
except discord.errors.LoginFailure as e:
    print(f"Erreur de connexion : {e}")
