from utils.main import Bot
import config
from discord.ext.commands import when_mentioned_or
from pathlib import Path
import sys
bot = Bot(when_mentioned_or(config.prefixes))

def format_cog(path):
    replacements = (('/', '.'), ('\\', '.'), ('.py', ''))
    for r in replacements:
        path = path.replace(*r)
    return path

if __name__ == "__main__":
    for cog_path in Path("cogs").glob('**/*.py'):
        formatted_cog = format_cog(str(cog_path))
        cog_name = formatted_cog.split(".")[-1]
        try:
            bot.load_extension(formatted_cog)
            print(f"Loaded cog {cog_name}")
        except Exception as e:
            print(f"{e.__class__.__name__} when loading cog {cog_name}: \n{e}")
    bot.run(config.token)