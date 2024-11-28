import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv
from datetime import datetime  # Importation ajoutée
from utils.keep_alive import keep_alive
from utils.scheduler_helper import fetch_anime_data, display_next_anime_timer, start_scheduler, get_last_anime

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

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")
    # Afficher le dernier anime annoncé
    last_anime = get_last_anime()
    if last_anime:  # Vérifie si des données existent dans last_anime.json
        print(f"Le dernier anime annoncé est : {last_anime.get('title', 'Aucun')} (Épisode {last_anime.get('episode', 'Inconnu')})")
    else:
        print("Aucun anime annoncé précédemment.")
    
    # Récupération et affichage du prochain épisode
    anime_list = await fetch_anime_data()
    if anime_list:
        next_anime = anime_list[0]  # Le premier anime de la liste triée
        airing_time = datetime.fromtimestamp(next_anime["airing_time"]).strftime("%Y-%m-%d %H:%M:%S")
        print(f"Prochain anime : {next_anime['title']} (Épisode {next_anime['episode']}) à {airing_time}")
    else:
        print("Aucun anime à venir.")

    # Lancer le planificateur
    await start_scheduler(bot)

# Lancer le bot
if __name__ == "__main__":
    keep_alive()
    asyncio.run(load_extensions())
    bot.run(TOKEN)
