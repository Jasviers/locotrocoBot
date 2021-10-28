from discord import channel, Embed
from discord.ext import commands
from discord.utils import get
from youtube_dl import YoutubeDL
from discord import FFmpegPCMAudio
from urllib.parse import urlparse
from DiscordUtils import Pagination
import lyricsgenius

import asyncio
import random
import math
import re
import os

class music_commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.genius = lyricsgenius.Genius(os.getenv("GENIUS_TOKEN"))
        self.tiratela_url = "https://www.youtube.com/watch?v=lHvPohMa_ak"
        self.a = "https://www.youtube.com/watch?v=A30gsOSHswM"
        self.LIMIT = 150
        self.MAX_CHARACTERS = 1000
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        self.playlist_re = re.compile(r"\b(list)\b")
        self.watch_re = re.compile(r"\b(watch)\b")

    @commands.command(name="play", aliases=["p"])
    async def play(self, ctx, *args):
        if not args:
            await ctx.send("Song name is required", delete_after=15)
            return
        query = " ".join(args)
        try:
            await self.join(ctx)
        except:
            return
        try:
            for s in self._search(query):
                self.queue.append(s)
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send("Song not found", delete_after=15)
        if not self.voice.is_playing():
            self._play(ctx)   

    @commands.command(name="tiratela")
    async def tiratela(self, ctx):
        try:
            await self.join(ctx)
        except:
            return
        try:
            self.queue = self._search(self.tiratela_url) + self.queue
        except:
            await ctx.send("Unexpected error", delete_after=15)
        if not self.voice.is_playing():
            await self._play(ctx)
        else:
            await self.skip(ctx)

    @commands.command(name="a")
    async def a_function(self, ctx):
        try:
            await self.join(ctx)
        except:
            return
        try:
            self.queue = self._search(self.a) + self.queue
        except:
            await ctx.send("Unexpected error", delete_after=15)
        if not self.voice.is_playing():
            await self._play(ctx)
        else:
            await self.skip(ctx)

    @commands.command(name="queue", aliases=["q"])
    async def queue_function(self, ctx):
        if self.queue or self.actual_song:
            song_list = f"1- {self.actual_song}\n"+"\n".join(f"{i+2}- {j['title']}" for i, j in enumerate(self.queue))
            await ctx.send(song_list, delete_after=15)
        else:
            await ctx.send("Queue is empty", delete_after=15)

    @commands.command(name='playing', aliases=['current', 'currentsong', 'crt'])
    async def now_playing(self, ctx):
        if not self.voice and not self.voice.is_connected:
            return await ctx.send("Not connected", delete_after=15)
        if not self.voice.is_playing():
            return await ctx.send("Not current play song", delete_after=15)
        return await ctx.send(f'**Now Playing:** `{self.actual_song}` ')

    @commands.command(name="shuffle", aliases=["shff"])
    async def shuffle(self, ctx):
        if self.queue:
            random.shuffle(self.queue)

    @commands.command(name="skip", aliases=["s", "next", "nxt"])
    async def skip(self, ctx):
        if self.voice and self.voice.is_playing():
            self.voice.stop()
            self._play(ctx)

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

    @commands.command(name="lyrics", aliases=["lcs"])
    async def lyrics(self, ctx):
        if self.actual_song:
            try:
                song = self.genius.search_song(self.actual_song)
            except:
                await ctx.send("Song not found", delete_after=15)
                return
            embed_list = []
            pages = math.ceil(len(song.lyrics)/self.MAX_CHARACTERS)
            print(pages)
            for i in range(pages):
                if i+1 < pages:
                    embed_list.append(Embed(color=ctx.author.color).add_field(
                        name=self.actual_song, value=song.lyrics[self.MAX_CHARACTERS*i:self.MAX_CHARACTERS*(i+1)]+f"\nPage {i+1}/{pages}"))
                else:
                    embed_list.append(Embed(color=ctx.author.color).add_field(
                        name=self.actual_song, value=song.lyrics[self.MAX_CHARACTERS*i::]+f"\nPage {i+1}/{pages}"))
                    print(song.lyrics[self.MAX_CHARACTERS*i::])
            paginator = Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
            paginator.add_reaction('⏮️', "first")
            paginator.add_reaction('⏪', "back")
            paginator.add_reaction('⏩', "next")
            paginator.add_reaction('⏭️', "last")
            await paginator.run(embed_list)
        else:
            await ctx.send("No song playing", delete_after=15)

    def _play(self, ctx):
        if self.queue:
            self.actual_song = self.queue[0]["title"]
            next_song = self.queue[0]["source"]
            self.queue.pop(0)
            self.voice.play(FFmpegPCMAudio(next_song, **self.FFMPEG_OPTIONS), after=lambda x: self._play(ctx))
        else:
            self.actual_song = ""

    def _search(self, query):
        url_result = urlparse(query)
        i = 0
        vlist = []
        if all([url_result.scheme, url_result.netloc, url_result.path]):
            if url_result.query and self.playlist_re.search(url_result.query):
                if self.watch_re.search(query):
                    list_query = [i for i in url_result.query.split("&") if self.playlist_re.search(i)]
                    query = "".join([url_result.netloc, "/playlist?", list_query[0]])
                with YoutubeDL(self.YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(query, download=False)
                entries_len = len(info['entries'])
                while i < entries_len and i < self.LIMIT:
                    elem = info['entries'][i]
                    vlist.append({'source': elem['formats'][0]['url'], 'title': elem['title']})
                    i += 1
                return vlist
            else:
                with YoutubeDL(self.YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(query, download=False)
        else:
            with YoutubeDL(self.YDL_OPTIONS) as ydl:
                info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
        return [{'source': info['formats'][0]['url'], 'title': info['title']}]
