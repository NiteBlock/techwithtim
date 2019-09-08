import discord
from discord.ext import commands
import time
import sys
from datetime import datetime as dt, timedelta as td

class PingCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()

    @commands.command(aliases=["version", "uptime", "lib", "bot"])
    async def ping(self, ctx):
        ver = f"{sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}"
        fields = [
            {"name" : "Bot latency", "value" : f"{round(self.bot.latency *1000)}ms", "inline" : False},
            {"name" : "Python version", "value": f"Python {ver}"},
            {"name" : "Libarary", "value" : f"Discord.py {discord.__version__}", "inline" : False},
            {"name" : "Uptime", "value" : str(td(seconds=int(round(time.time() - self.start_time))))}
        ]
        await ctx.em("Bot information!", "Here you can see info about the bot:", fields=fields)

def setup(bot):
    bot.add_cog(PingCommand(bot))