import discord
from discord.ext import commands
import string
import random
from utils.embeds import em


class Rep(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_cmd = {
            "name" : "Rep Commands",
            "description" : "Commands related to the rep command!",
            "emoji" : "🤝"
        }
    
    async def add_rep(self, id, from_id, reason):
        letters = [le for le in string.ascii_lowercase]
        for let in string.ascii_uppercase:
            letters.append(let)
        for i in range(10):
            letters.append(str(i))
        rep_id = ''.join(random.choice(letters) for i in range(12))
        await self.bot.db.reps.insert_one({"id" : id, "from_id" : from_id, "rep_id" : rep_id, "reason" : reason})
        return rep_id

    async def remove_rep(self, rep_id):
        return await self.bot.db.reps.find_one_and_delete({"rep_id" : rep_id})
    
    async def get_reps(self, user_id):
        return await (self.bot.db.reps.find({"id": user_id})).to_list(length=1000)

    def format_rep(self, rep):
        return f"<@{rep['from_id']}> | <@{rep['id']}> | {rep['rep_id']} | {rep['reason']}"

    def format_reps(self, reps):
        text = "\n".join([self.format_rep(rep) for rep in reps])
        if text == "": return "No reps found."
        text = f"Reps ({len(reps)}):\n\n" + text
        return text
    
    @commands.command()
    async def rep(self, ctx, user:discord.Member, *, reason):
        if user == ctx.author:
            raise commands.CommandError("You cannot rep yourself.")
        rep_id = await self.add_rep(user.id, ctx.author.id, reason)
        try: await user.send(embed=em("You have recived a rep.", f"{ctx.author.mention} has given you a rep for {reason}"))
        except: pass
        await ctx.em(f"You have given {user.name} a rep!", f"Rep id: {rep_id}")


    @commands.command()
    async def reps(self, ctx, user:discord.Member=None):
        if not user:
            user = ctx.author
        reps = await self.get_reps(user.id)
        await ctx.em(f"{user.name}'s reps!", self.format_reps(reps))

    @commands.command(aliases=["remove_rep", "delete_rep", "del_rep"])
    @commands.has_permissions(manage_messages=True)
    async def rm_rep(self, ctx, rep_id):
        rep = await self.remove_rep(rep_id)
        await ctx.em("Rep Removed!", self.format_rep(rep))


def setup(bot):
    bot.add_cog(Rep(bot))