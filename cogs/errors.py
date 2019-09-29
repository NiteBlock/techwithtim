from discord.ext import commands
import discord



class errorCatching(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure) or isinstance(error, commands.MissingPermissions):
            await ctx.em("Error!", "You dont have permissions to do this!", color=discord.Color.red())
        elif isinstance(error, commands.CommandNotFound):
            await ctx.em("Error!", "This is not a command!", color=discord.Color.red())
        elif isinstance(error, commands.CommandError):
            await ctx.em("Error!", str(error), color=discord.Color.red())
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.em("Error!", f"You are missing the parameter {error.param.name.title()}!", color=discord.Color.red())
        elif isinstance(error, commands.BadUnionArgument):
            await ctx.em("Error!", "You are using this command wrong!", color=discord.Color.red())
        elif isinstance(error, commands.BadArgument):
            await ctx.em("Error!", "You are using this command wrong!", color=discord.Color.red())
        elif isinstance(error, discord.Forbidden):
            await ctx.em("Error!", "I cant do this!", color=discord.Color.red())
        else:
            await ctx.em("Error!", f"""Invalid command usage!
            ```py
            {error.__class__.__name__}:
            {error}
            ```
            
            **Please contact staff if you think this is an error.**""", color=discord.Color.red())

def setup(bot):
    bot.add_cog(errorCatching(bot))