def setup_ping(bot):
    @bot.command()
    async def ping(ctx):
        latency = round(bot.latency * 1000)  # Convertir la latence en millisecondes
        await ctx.send(f"Pong ! 🏓 Latence : {latency}ms")