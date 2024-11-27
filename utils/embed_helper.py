# utils/embed_helper.py

import discord
from datetime import datetime, timezone, timedelta

def create_anime_embed(anime_data):
    title = anime_data['media']['title']['romaji'] or anime_data['media']['title']['english']
    episode = anime_data['episode']
    cover_image = anime_data['media']['coverImage']['extraLarge']

    embed = discord.Embed(
        title=title,
        description=f"L'épisode {episode} est maintenant disponible !",
        color=discord.Color.blue()
    )
    embed.set_image(url=cover_image)
    embed.set_footer(text=f"Annonce automatique")
    return embed

def create_upcoming_embed(episodes):
    embed = discord.Embed(
        title="Animes à venir",
        color=discord.Color.green()
    )
    paris_timezone = timezone(timedelta(hours=2))  # Ajustez selon le fuseau horaire
    for episode in episodes:
        title = episode['media']['title']['romaji'] or episode['media']['title']['english']
        airing_time = datetime.fromtimestamp(episode['airingAt'], tz=timezone.utc)
        airing_time = airing_time.astimezone(paris_timezone)
        embed.add_field(
            name=title,
            value=f"Épisode {episode['episode']} - Diffusion le {airing_time.strftime('%d/%m/%Y %H:%M:%S')}",
            inline=False
        )
    return embed
