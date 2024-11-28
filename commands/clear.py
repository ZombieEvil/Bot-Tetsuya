# commands/clear.py

from discord.ext import commands

class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='clear')
    @commands.has_permissions(manage_messages=True)
    async def clear_command(self, ctx, amount: int = 10):
        await ctx.channel.purge(limit=amount)
        confirmation = await ctx.send(f"{amount} messages ont été supprimés.", delete_after=5)

async def setup(bot):
    await bot.add_cog(Clear(bot))
