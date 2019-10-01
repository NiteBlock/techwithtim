import discord
from discord.ext import commands
import aiohttp
import config
from utils.embeds import em

class YoutubeCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_cmd = {
            "name" : "Youtube Commands",
            "description" : "Search for videos and get tims sub count!",
            "emoji" : "📹"
        }
    
    @commands.command(aliases=["sub_count", "yt_stats", "video_list"])
    async def stats(self, ctx):
        r = await self.bot.session.get("https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + config.yt_channel_id + "&key="+ config.youtube_api_key)
        data = await r.json()
        stats = data["items"][0]["statistics"]
        await ctx.em("Tims Youtube statistics", f"Total Views: {stats['viewCount']}\nTotal Video Amount: {stats['videoCount']}\nTotal Subscribers: {stats['subscriberCount']}")

    @commands.command(aliases=["search_yt", "find_video"])
    async def videos(self, ctx, *, query):
        r = await self.bot.session.get("https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=" + config.yt_channel_id + str("&q=%s&key=" % (query)) + config.youtube_api_key)
        data = await r.json()
        videos = data["items"]
        li = []
        x = 0
        for video in videos:
            if x > 8:
                break
            try: li.append(f"[{video['snippet']['title']}](https://youtube.com/watch?v={video['id']['videoId']})")
            except: continue
            x+=1
        desc = "\n\n".join(li)
        if desc != "":
            await ctx.em("Video search results", desc)
        else:
            await ctx.em("No videos found", "There were no videos found with your search")
def setup(bot):
    bot.add_cog(YoutubeCommands(bot))