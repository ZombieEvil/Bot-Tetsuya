# commands/last.py

from discord.ext import commands
from utils.scheduler_helper import get_last_anime_embed

class Last(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='last')
    async def last_command(self, ctx):
        embed = get_last_anime_embed()
        if embed:
            await ctx.send(embed=embed)
        else:
            await ctx.send("Aucun anime n'a été annoncé récemment.")

async def setup(bot):
    await bot.add_cog(Last(bot))
