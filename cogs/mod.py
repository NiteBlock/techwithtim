import discord
from discord.ext import commands
from utils.embeds import em

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_cmd = {
            "name" : "Moderation Commands",
            "description" : "Commands only staff can use.",
            "emoji" : "🛠"
        }

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user:discord.Member, *, reason:str="No given reason!"):
        try:
            await user.send(embed=em(f"{ctx.author.name} has banned you from {ctx.guild.name} with the reason '{reason}''", f"{user.name}, You have been banned!"))
        except: pass
        await user.ban(reason=reason)
        await ctx.em(f"You have banned {user.name} for '{reason}''", f"{user.name} was banned!")
    
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user:discord.Member, *, reason:str="No given reason!"):
        try:
            await user.send(embed=em(f"{ctx.author.name} has kicked you from {ctx.guild.name} with the reason '{reason}''", f"{user.name}, You have been kicked!"))
        except: pass
        await user.kick(reason=reason)
        await ctx.em(f"You have kicked {user.name} for '{reason}'", f"{user.name} was kicked!")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount:int=100):
        await ctx.channel.purge(limit=amount)
        await ctx.em("This message will delete itself in 10 seconds!", f"{amount} messages purged!", delete_after=10)


def setup(bot):
    bot.add_cog(Moderation(bot))