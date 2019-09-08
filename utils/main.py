import discord
from discord.ext import commands
from utils.embeds import em
import yaml

class Context(commands.Context):
    async def em(self, *args, **kw):
        return await self.send(embed=em(*args, **kw))

class Help(commands.HelpCommand):
    pass

class Bot(commands.Bot):
    def __init__(self, cmdpre, **kw):

        self.ctx_cls = kw.get("ctx_cls", Context)
        kw["help_command"] = kw.get("help_command", Help())
        super().__init__(cmdpre, **kw)
    
    async def get_context(self, message, **kw):
        return await super().get_context(message, cls=kw.get("cls", self.ctx_cls))