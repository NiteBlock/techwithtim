import discord
from discord.ext import commands

class Level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def ensure_user(self, id):
        if id not in [u["user"] for u in await self.bot.db.levels.find({}).tolist(lenght=100000)]:
            await self.bot.db.levels.insert_one({"user" : id, "level" : 0, "xp" : 0})

    async def get_level(self, user_id):
        await self.ensure_user(user_id)
        return await self.bot.db.levels.find_one({"user": user_id})

    async def add_level(self, user_id, amount):
        await self.ensure_user(user_id)
        data = await self.bot.db.levels.find_one_and_update({"user" : user_id}, {"$inc" : {"xp" : 5}})
        return 

def setup(bot):
    bot.add_cog(Level(bot))