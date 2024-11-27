import discord
from discord.ext import commands
import time
from datetime import datetime
from utils.scheduler_helper import fetch_anime_data


class Upcoming(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="upcoming")
    async def upcoming_command(self, ctx):
        """Affiche les prochains animes à diffuser."""
        try:
            current_timestamp = int(time.time())  # Obtenir le timestamp actuel
            data = await fetch_anime_data()

            if data and 'data' in data and 'Page' in data['data']:
                airing_schedules = data['data']['Page']['airingSchedules']

                if airing_schedules:
                    embed = discord.Embed(
                        title="Animes à venir",
                        description="Voici les prochains épisodes d'animes à diffuser :",
                        color=discord.Color.blue(),
                    )
                    for schedule in airing_schedules[:10]:  # Limiter à 10 animes pour éviter une surcharge
                        title = schedule['media']['title']['romaji'] or schedule['media']['title']['english']
                        episode = schedule['episode']
                        airing_time = schedule['airingAt']
                        formatted_time = datetime.fromtimestamp(airing_time).strftime('%Y-%m-%d %H:%M:%S')
                        embed.add_field(
                            name=f"{title} (Épisode {episode})",
                            value=f"Diffusion prévue le {formatted_time}",
                            inline=False,
                        )

                    await ctx.send(embed=embed)
                else:
                    await ctx.send("Aucun anime à venir trouvé.")
            else:
                await ctx.send("Erreur : Impossible de récupérer les données des animes.")
        except Exception as e:
            print(f"Erreur dans la commande upcoming: {e}")
            await ctx.send("Une erreur s'est produite lors de l'exécution de la commande.")

async def setup(bot):
    """Ajoute la cog Upcoming au bot."""
    await bot.add_cog(Upcoming(bot))
