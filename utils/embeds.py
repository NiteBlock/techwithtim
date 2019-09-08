import discord
import config
from datetime import datetime as dt

def em(title, description, **kw):
    embed = discord.Embed()
    embed.title = title
    embed.description = description
    embed.timestamp = kw.get("timestamp", dt.utcnow())
    embed.colour = kw.get("colour", kw.get("color", config.embed["colour"]))
    
    embed.set_footer(text=kw.get("footer", embed.footer.text), icon_url=kw.get("footer_icon", config.embed["footer"]["icon_url"]))
    embed.set_thumbnail(url=kw.get("thumbnail", config.embed["thumbnail"]))
    for field in kw.get("fields", []): embed.add_field(**field)
    return embed