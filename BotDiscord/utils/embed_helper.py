# utils/embed_helper.py

import discord
from datetime import datetime, timezone, timedelta

def create_anime_embed(anime_data):
    title = anime_data['media']['title']['romaji'] or anime_data['media']['title']['english']
    episode = anime_data['episode']
    # Convertir le timestamp en datetime avec fuseau horaire
    airing_time = datetime.fromtimestamp(anime_data['airingAt'], tz=timezone.utc)
    # Ajuster pour le fuseau horaire de Paris (UTC+1 ou UTC+2 en été)
    paris_timezone = timezone(timedelta(hours=2))  # Changez à 1 si c'est l'heure d'hiver
    airing_time = airing_time.astimezone(paris_timezone)
    cover_image = anime_data['media']['coverImage']['extraLarge']

    embed = discord.Embed(
        title=title,
        description=f"Le nouvel épisode {episode} sera diffusé.",
        color=discord.Color.blue()
    )
    embed.set_image(url=cover_image)
    embed.set_footer(text=airing_time.strftime("%d/%m/%Y %H:%M:%S"))
    return embed

def create_upcoming_embed(episodes):
    embed = discord.Embed(
        title="Animes à venir",
        color=discord.Color.green()
    )
    paris_timezone = timezone(timedelta(hours=2))  # Changez à 1 si c'est l'heure d'hiver
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
