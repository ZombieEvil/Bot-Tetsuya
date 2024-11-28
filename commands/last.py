# commands/last.py

from discord.ext import commands
from utils.scheduler_helper import get_last_anime

class Last(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='last')
    async def last_command(self, ctx):
        last_anime = get_last_anime()
        if last_anime:
            embed = self.create_last_anime_embed(last_anime)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Aucun anime n'a été annoncé récemment.")

    def create_last_anime_embed(self, anime_data):
        """Crée un embed pour afficher le dernier anime annoncé."""
        embed = discord.Embed(
            title=anime_data['title'],
            description=f"Épisode {anime_data['episode']} a été annoncé.",
            color=discord.Color.blue()
        )
        embed.set_image(url=anime_data['image'])
        embed.set_footer(text="Dernière annonce")
        return embed

async def setup(bot):
    await bot.add_cog(Last(bot))
