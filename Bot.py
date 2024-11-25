import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from utils.keep_alive import keep_alive
from commands.ping import setup_ping
from commands.planning import setup_planning
from commands.anilist import setup_anilist
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Initialisation du bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Scheduler pour les tâches périodiques
scheduler = AsyncIOScheduler()

# Charger les commandes
setup_ping(bot)
setup_planning(bot)
setup_anilist(bot, scheduler)

# Lancer Flask pour garder le bot actif
keep_alive()

# Lancer le bot
@bot.event
async def on_ready():
    print(f"{bot.user} est connecté et prêt !")
    scheduler.start()

bot.run(TOKEN)