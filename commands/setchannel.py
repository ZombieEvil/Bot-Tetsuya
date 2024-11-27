# commands/setchannel.py

from discord.ext import commands
from utils.config_helper import save_channel_id

class SetChannelCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='setchannel')
    async def setchannel_command(self, ctx):
        print("setchannel_command invoked")  # Pour le débogage
        try:
            guild_id = str(ctx.guild.id)
            channel_id = ctx.channel.id
            save_channel_id(guild_id, channel_id)
            await ctx.send(f"Salon configuré pour les annonces : {ctx.channel.mention}")
        except Exception as e:
            print(f"Erreur dans setchannel_command: {e}")
            await ctx.send("Une erreur s'est produite lors de la configuration du salon.")

async def setup(bot):
    print("Setup function in setchannel.py called")  # Pour le débogage
    await bot.add_cog(SetChannelCog(bot))
