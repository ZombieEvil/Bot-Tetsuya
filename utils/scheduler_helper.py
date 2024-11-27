# utils/scheduler_helper.py

import time
import aiohttp
from utils.config_helper import load_config
from utils.embed_helper import create_anime_embed
import asyncio

last_anime_announced = None

async def fetch_anime_data():
    current_timestamp = int(time.time())

    query = '''
    query {
      Page(perPage: 10) {
        airingSchedules(sort: TIME, airingAt_greater: %d) {
          media {
            title {
              romaji
              english
            }
            coverImage {
              extraLarge
            }
          }
          episode
          airingAt
        }
      }
    }
    ''' % (current_timestamp)

    url = 'https://graphql.anilist.co'
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json={'query': query}) as response:
            return await response.json()

async def check_for_new_episodes(bot):
    global last_anime_announced
    data = await fetch_anime_data()
    if data and 'data' in data and 'Page' in data['data']:
        if data['data']['Page']['airingSchedules']:
            new_episode = data['data']['Page']['airingSchedules'][0]
            if new_episode != last_anime_announced:
                last_anime_announced = new_episode
                embed = create_anime_embed(new_episode)
                config = load_config()
                for guild_id, guild_config in config.items():
                    channel = bot.get_channel(guild_config['channel_id'])
                    if channel:
                        await channel.send(embed=embed)

def get_last_anime_embed():
    if last_anime_announced:
        return create_anime_embed(last_anime_announced)
    return None

async def fetch_upcoming_episodes():
    data = await fetch_anime_data()
    current_timestamp = int(time.time())
    upcoming_episodes = []

    if data and 'data' in data and 'Page' in data['data']:
        for episode in data['data']['Page']['airingSchedules']:
            if episode['airingAt'] > current_timestamp:
                upcoming_episodes.append(episode)

    return upcoming_episodes
