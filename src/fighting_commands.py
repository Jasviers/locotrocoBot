from discord import channel
from discord.ext import commands
from discord.utils import get
from youtube_dl import YoutubeDL
from discord import FFmpegPCMAudio

class fighting_commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.voice = None
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    ## tiratela command correspond to this place

    @commands.command(name="moneymatch", aliases=["mm"])
    async def money_match(self, ctx):
        await ctx.send(f'Work In Progress')

    @commands.command(name="chaparrin", aliases=["chpn"])
    async def chaparrin(self, ctx):
        await ctx.send(f'Work In Progress')

    @commands.command(name="framedata", aliases=["fd"])
    async def frame_data(self, ctx, character):
        await ctx.send(f'Work In Progress')
    