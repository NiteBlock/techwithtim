import discord

prefixes = ("t!")

with open("token.txt", "r") as f:
    token = f.read()

embed = {
    "colour" : 0xB7D535,
    "footer" : {
        "text" : "Tech with Tim 2.0",
        "icon_url" : "https://cdn.discordapp.com/avatars/501089409379205161/77834aea21f4c2ea93379c7dd46a0fa8.png?size=256"
    },
    "thumbnail" : "https://cdn.discordapp.com/avatars/501089409379205161/77834aea21f4c2ea93379c7dd46a0fa8.png?size=1024"
}
