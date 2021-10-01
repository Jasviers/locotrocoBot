from discord import channel
from discord.ext import commands
from discord.utils import get
from youtube_dl import YoutubeDL
from discord import FFmpegPCMAudio

class music_commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.voice = None
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    @commands.command(name="play", aliases=["p"])
    async def play(self, ctx, arg1):
        await self.join(ctx)

        if not self.voice.is_playing():
            with YoutubeDL(self.YDL_OPTIONS) as ydl:
                info = ydl.extract_info(arg1, download=False)
            URL = info['formats'][0]['url']
            self.voice.play(FFmpegPCMAudio(URL, **self.FFMPEG_OPTIONS))
            self.voice.is_playing()

        else:
            await ctx.send("Ya hay musica TONTO")
            return

    @commands.command(name="stop", aliases=["st"])
    async def stop(self, ctx):
        if self.voice.is_playing():
            self.voice.stop()
            await ctx.send('Parando tremendo musicardo')

    @commands.command(name="resume", aliases=["rs"])
    async def resume(self, ctx):
        if not self.voice.is_playing():
            self.voice.resume()

    @commands.command(name="pause", aliases=["ps"])
    async def pause(self, ctx):
        if self.voice.is_playing():
            self.voice.pause()

    @commands.command(name="join", aliases=["jn"])
    async def join(self, ctx):
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

    @commands.command(name="leave", aliases=["lv"])
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()