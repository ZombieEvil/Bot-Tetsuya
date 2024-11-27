# commands/upcoming.py

from discord.ext import commands
from utils.embed_helper import create_upcoming_embed
from utils.scheduler_helper import fetch_upcoming_episodes

class Upcoming(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='upcoming')
    async def upcoming_command(self, ctx):
        upcoming_episodes = await fetch_upcoming_episodes()
        if upcoming_episodes:
            embed = create_upcoming_embed(upcoming_episodes)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Aucun épisode à venir n'a été trouvé.")

async def setup(bot):
    await bot.add_cog(Upcoming(bot))
