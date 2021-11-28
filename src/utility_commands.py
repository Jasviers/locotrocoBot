from discord.ext import commands
from discord.utils import get
from discord import Embed, Color
from DiscordUtils import Pagination
from musicPlayer import MusicPlayer, YTDLSource

import requests
import os

class utility_commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.w2endpoint = "https://w2g.tv/rooms/create.json"
        self.w2g_key = os.getenv("W2G_TOKEN")
        self.w2room_url = "https://w2g.tv/rooms/"

    @commands.command(name="watch2gether", aliases=["w2g"])
    async def watch2gether(self, ctx, *args):
        if not args:
            await ctx.send(embed=Embed(title="", description="Url resource is required", color=Color.green()), delete_after=60)
            return
        query = " ".join(args)
        data = {
            "w2g_api_key" : self.w2g_key,
            "share" : query,
            "bg_color" : "#ffffff",
            "bg_opacity" : "50"
        }
        response = requests.post(self.w2endpoint, data=data)
        response = response.json()
        streamkey = response.get("streamkey")
        await ctx.send(embed=Embed(title="Your Watch2gether room", description=f"{self.w2room_url+streamkey}", color=Color.green()))
