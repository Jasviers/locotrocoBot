from discord import channel
from discord.ext import commands
from discord.utils import get
from youtube_dl import YoutubeDL
from discord import FFmpegPCMAudio
from urllib.parse import urlparse
import random

class music_commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.actual_song = ""
        self.voice = None
        self.tiratela_url = "https://www.youtube.com/watch?v=lHvPohMa_ak"
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    @commands.command(name="play", aliases=["p"])
    async def play(self, ctx, *args):
        query = " ".join(args)
        try:
            await self.join(ctx)
        except:
            return
        try:
            self.queue.append(self._search(query))
        except:
            await ctx.send("Song not found")
        if not self.voice.is_playing():
            self._play()    

    @commands.command(name="tiratela")
    async def tiratela(self, ctx):
        try:
            await self.join(ctx)
        except:
            return

        try:
            self.queue = [self._search(self.tiratela_url)] + self.queue
        except:
            await ctx.send("Unexpected error")
        if not self.voice.is_playing():
            self._play()
        else:
            await self.skip(ctx)

    @commands.command(name="queue", aliases=["q"])
    async def queue_function(self, ctx):
        if self.queue or self.actual_song:
            song_list = f"1- {self.actual_song}\n"+"\n".join(f"{i+2}- {j['title']}" for i, j in enumerate(self.queue))
            await ctx.send(song_list)
        else:
            await ctx.send("Queue is empty")

    @commands.command(name="shuffle", aliases=["shff"])
    async def shuffle(self, ctx):
        if self.queue:
            random.shuffle(self.queue)

    @commands.command(name="skip", aliases=["s", "next", "nxt"])
    async def skip(self, ctx):
        if self.voice and self.voice.is_playing():
            self.voice.stop()
            self._play()

    @commands.command(name="stop", aliases=["st", "clear", "clr"])
    async def stop(self, ctx):
        if self.voice.is_playing():
            self.voice.stop()
            self.queue = []
            self.actual_song = ""

    @commands.command(name="resume", aliases=["rs"])
    async def resume(self, ctx):
        if self.voice and not self.voice.is_playing():
            self.voice.resume()

    @commands.command(name="pause", aliases=["ps"])
    async def pause(self, ctx):
        if self.voice and self.voice.is_playing():
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
        if self.voice and self.voice.is_connected():
            await self.stop(ctx)
            await ctx.voice_client.disconnect()

    def _play(self):
        if self.queue:
            self.actual_song = self.queue[0]["title"]
            next_song = self.queue[0]["source"]
            self.queue.pop(0)
            self.voice.play(FFmpegPCMAudio(next_song, **self.FFMPEG_OPTIONS), after=lambda x: self._play())
        else:
            self.actual_song = ""

    def _search(self, query):
        result = urlparse(query)
        if all([result.scheme, result.netloc, result.path]):
            with YoutubeDL(self.YDL_OPTIONS) as ydl:
                info = ydl.extract_info(query, download=False)
        else:
            with YoutubeDL(self.YDL_OPTIONS) as ydl:
                info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
        return {'source': info['formats'][0]['url'], 'title': info['title']}
