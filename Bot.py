import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
from utils.keep_alive import keep_alive
from utils.scheduler_helper import fetch_anime_data, display_next_anime_timer, start_scheduler

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
    last_anime = await fetch_anime_data()
    if last_anime:
        print(f"Le dernier anime annoncé est : {last_anime.get('title', 'Aucun')}")

    # Lancer le planificateur
    await start_scheduler(bot)

# Lancer le bot
if __name__ == "__main__":
    keep_alive()
    asyncio.run(load_extensions())
    bot.run(TOKEN)
