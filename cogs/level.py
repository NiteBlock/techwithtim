import discord
from discord.ext import commands
import random
import asyncio
import motor

class Level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.on_cooldown = []
        self.MessageLock = asyncio.Lock()
        self.help_cmd = {
            "name" : "Leveling",
            "description" : "Find out people's levels and rank up with daily xp!",
            "emoji" : "⏫"
        }

    async def ensure_user(self, id):
        if id not in [u["user"] for u in await self.bot.db.levels.find({}).to_list(length=100000)]:
            await self.bot.db.levels.insert_one({"user" : id, "level" : 0, "xp" : 0})

    async def get_level(self, user_id):
        await self.ensure_user(user_id)
        return await self.bot.db.levels.find_one({"user": user_id})

    async def add_xp(self, user_id, amount=random.randint(15,25)):
        await self.ensure_user(user_id)
        data = await self.bot.db.levels.find_one_and_update({"user" : user_id}, {"$inc" : {"xp" : amount}}, return_document=motor.pymongo.ReturnDocument.AFTER)
        l = data["level"] + 1
        xp_req = 5 / 6 * l * (2 * l * l + 27 * l + 91)
        if data["xp"] >= xp_req:
            data = await self.bot.db.levels.find_one_and_update({"user" : user_id}, {"$inc" : {"level" : 1}}, return_document=motor.pymongo.ReturnDocument.AFTER)
            return True, data
        return False, data
    
    @commands.Cog.listener()
    async def on_message(self, message):
        ctx = await self.bot.get_context(message)
        async with self.MessageLock:
            if ctx.author.id in self.on_cooldown:
                return
            self.on_cooldown.append(ctx.author.id) 
            await self.add_xp(ctx.author.id)
def setup(bot):
    bot.add_cog(Level(bot))