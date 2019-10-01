import discord
from discord.ext import commands
from utils.embeds import em
import yaml
from motor.motor_asyncio import AsyncIOMotorClient
import config
import aiohttp

class Context(commands.Context):
    async def em(self, *args, **kw):
        return await self.send(embed=em(*args, **kw))

class Help(commands.HelpCommand):
    def get_command_signature(self, command):
        return f"`{self.clean_prefix}{command.qualified_name} {command.signature}`\n"
    
    async def send_command_help(self, command):
        embed = em(command.name, command.description)
        if len(command.aliases) > 0:
            embed.add_field(name="Aliases", value=', '.join(command.aliases))
        embed.add_field(name="Usage", value=self.get_command_signature(command))
        await self.context.send(embed=embed)

    async def send_bot_help(self, mapping):
        embed = em("Help", "Choose a category to send help about them.")
        items = dict(mapping.items())
        rm = []
        for item in items:
            if not item:
                print(item)
                rm.append(item)
            elif not item.help_cmd:
                print(item)
                rm.append(item)
        print(rm)
        for item in rm: del items[item]
        new = []
        for item in items:
            new.append((item, items[item]))
        print(new)
        items = new[:]
        li1 = []
        li2 = []
        for c, cmds in items: 
            li1.append((c, cmds))
            li2.append((c.help_cmd["emoji"]))
        
        msg = await self.context.em("Please wait...", "Getting the commands ready...")
        for cog, cog_commands in items:
            if not cog.help_cmd:
                continue

            command_signatures = '\n'.join([self.get_command_signature(c) for c in cog_commands])


            embed.add_field(name=cog.help_cmd["emoji"]+" "+cog.help_cmd["name"], value=cog.help_cmd["description"], inline=False)
            await msg.add_reaction(cog.help_cmd["emoji"])
        await msg.add_reaction("🏠")
        embed.add_field(name="🏠 Home", value="Go back to this screen.")
        await msg.edit(embed=embed)
        while True:
            def check(r, u):
                return r.message.id == msg.id and not u.bot and (str(r.emoji) in li2 or str(r.emoji) == "🏠") and u.id == self.context.author.id
            try: r,u = await self.context.bot.wait_for("reaction_add", check=check, timeout=300)
            except: break
            await msg.remove_reaction(str(r.emoji), self.context.author)
            if str(r.emoji) == "🏠":
                await msg.edit(embed=embed)
                continue
            cog, cmds = li1[li2.index(str(r.emoji))]

            command_signatures = '\n'.join([self.get_command_signature(c) for c in cmds])
            if command_signatures:
                await msg.edit(embed=em(cog.help_cmd["emoji"]+" "+cog.help_cmd["name"], cog.help_cmd["description"], fields=[{"name" : "Commands", "value" : command_signatures}]))
            else:
                await msg.edit(embed=em(cog.help_cmd["emoji"]+" "+cog.help_cmd["name"], cog.help_cmd["description"]))
        await msg.delete()
    async def send_group_help(self, group):
        embed = em("Help for the group "+ group.name, "A list of all the commands:")
        for command in group.commands:
            embed.add_field(name=command.qualified_name, value=self.get_command_signature(command))

        await self.context.send(embed=embed)

class Bot(commands.Bot):
    def __init__(self, cmdpre=config.prefixes, **kw):
        self.ctx_cls = kw.get("ctx_cls", Context)
        self.db = AsyncIOMotorClient(config.database_login)[config.database_name]
        kw["help_command"] = kw.get("help_command", Help())

        super().__init__(commands.when_mentioned_or(cmdpre), **kw)
        self.session = aiohttp.ClientSession(loop=self.loop)

    async def get_context(self, message, **kw):
        return await super().get_context(message, cls=kw.get("cls", self.ctx_cls))