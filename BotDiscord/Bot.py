# bot.py

import os
import discord
from discord.ext import commands, tasks
from utils.scheduler_helper import check_for_new_episodes
from utils.keep_alive import keep_alive  # Importer keep_alive
from dotenv import load_dotenv
import asyncio
import logging

# Activer les logs de débogage
logging.basicConfig(level=logging.DEBUG)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Configurer les intents
intents = discord.Intents.default()
intents.message_content = True  # Doit être défini sur True pour recevoir le contenu des messages
intents.guilds = True  # Nécessaire pour les événements liés aux guildes
intents.members = True  # Si vous interagissez avec les membres

bot = commands.Bot(command_prefix='!', intents=intents)

# Charger les extensions
initial_extensions = [
    'commands.setchannel',
    'commands.clear',
    'commands.last',
    'commands.upcoming'
]

# Tâche récurrente pour les annonces automatiques
@tasks.loop(minutes=5)
async def scheduled_task():
    await check_for_new_episodes(bot)

@scheduled_task.before_loop
async def before():
    await bot.wait_until_ready()

# Événement on_ready pour démarrer la tâche planifiée
@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user.name}')
    if not scheduled_task.is_running():
        scheduled_task.start()

# Gestionnaire d'événements pour on_message (pour le débogage)
@bot.event
async def on_message(message):
    print(f"Received message from {message.author}: {message.content}")
    await bot.process_commands(message)

async def main():
    # Appeler keep_alive pour démarrer le serveur web
    keep_alive()
    async with bot:
        # Charger les extensions de manière asynchrone avec gestion des exceptions
        for extension in initial_extensions:
            try:
                await bot.load_extension(extension)
                print(f'Extension {extension} chargée avec succès.')
            except Exception as e:
                print(f'Erreur lors du chargement de l\'extension {extension}: {e}')
        # Démarrer le bot
        await bot.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())
