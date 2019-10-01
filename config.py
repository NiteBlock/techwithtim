import discord

prefixes = ("t!")
import json
with open("secret.json", "r") as f:
    secerts = json.loads(f.read())
token = secerts["token"]

database_login = secerts["db_login"]
database_name = "twt"

youtube_api_key = secerts["youtube_api_key"]

yt_channel_id = "UC4JX40jDee_tINbkjycV4Sg"

poll_channel = 628295950099808297

embed = {
    "colour" : 0xB7D535,
    "footer" : {
        "text" : "Tech with Tim 2.0",
        "icon_url" : "https://cdn.discordapp.com/avatars/501089409379205161/77834aea21f4c2ea93379c7dd46a0fa8.png?size=256"
    },
    "thumbnail" : "https://cdn.discordapp.com/avatars/501089409379205161/77834aea21f4c2ea93379c7dd46a0fa8.png?size=1024"
}
