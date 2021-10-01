from discord import channel
from discord.ext import commands
from discord.utils import get
from youtube_dl import YoutubeDL
from discord import FFmpegPCMAudio

class fighting_commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.voice = None
        self.tiratela_url = "https://www.youtube.com/watch?v=lHvPohMa_ak"
        self.voice = None
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    @commands.command(name="tiratela")
    async def tiratela(self, ctx):
        channel = ctx.author.voice.channel
        if not channel:
            return
        if self.voice and self.voice.is_connected():
            if self.voice.channel == channel:
                pass
            else:
                await self.voice.move_to(channel)
        else:
            self.voice = await channel.connect()

        if not self.voice.is_playing():
            with YoutubeDL(self.YDL_OPTIONS) as ydl:
                info = ydl.extract_info(self.tiratela_url, download=False)
            URL = info['formats'][0]['url']
            self.voice.play(FFmpegPCMAudio(URL, **self.FFMPEG_OPTIONS))
            self.voice.is_playing()

    @commands.command(name="moneymatch", aliases=["mm"])
    async def money_match(self, ctx):
        await ctx.send(f'Work In Progress')

    @commands.command(name="chaparrin", aliases=["chpn"])
    async def chaparrin(self, ctx):
        await ctx.send(f'Work In Progress')

    @commands.command(name="framedata", aliases=["fd"])
    async def frame_data(self, ctx, character):
        await ctx.send(f'Work In Progress')
    