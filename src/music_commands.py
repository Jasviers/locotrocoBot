from discord import Embed, Color
from discord.ext import commands
from discord.utils import get
import discord
from youtube_dl import YoutubeDL
from urllib.parse import urlparse
from DiscordUtils import Pagination
import lyricsgenius
from musicPlayer import MusicPlayer, InvalidVoiceChannel, VoiceConnectionError, YTDLSource

import traceback
import itertools
import asyncio
import math
import sys
import re
import os

class music_commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.players = {}
        self.genius = lyricsgenius.Genius(os.getenv("GENIUS_TOKEN"))
        self.tiratela_url = "https://www.youtube.com/watch?v=lHvPohMa_ak"
        self.a = "https://www.youtube.com/watch?v=A30gsOSHswM"
        self.fart = "https://www.youtube.com/watch?v=W_FRPoJIrlI"
        self.LIMIT = 150
        self.MAX_CHARACTERS = 1000
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.ytdl = YoutubeDL(self.YDL_OPTIONS)
        self.playlist_re = re.compile(r"\b(list)\b")
        self.watch_re = re.compile(r"\b(watch)\b")

    @commands.command(name="play", aliases=["p"])
    async def play(self, ctx, *args):
        if not args:
            await ctx.send("Song name is required", delete_after=15)
            return
        query = " ".join(args)
        voice = ctx.voice_client

        if not voice:
            await ctx.invoke(self.join)

        player = self._get_player(ctx)

        source = await YTDLSource.create_source(ctx, query, loop=self.bot.loop)

        await player.queue.put(source)

    @commands.command(name="tiratela")
    async def tiratela(self, ctx):
        voice = ctx.voice_client
        if not voice:
            await ctx.invoke(self.join)

        player = self._get_player(ctx)

        source = await YTDLSource.create_source(ctx, self.tiratela_url, loop=self.bot.loop)

        await player.queue.put(source)

    @commands.command(name="a")
    async def a(self, ctx):
        voice = ctx.voice_client
        if not voice:
            await ctx.invoke(self.join)

        player = self._get_player(ctx)

        source = await YTDLSource.create_source(ctx, self.a, loop=self.bot.loop)

        await player.queue.put(source)

    @commands.command(name="fart")
    async def fart(self, ctx):
        voice = ctx.voice_client
        if not voice:
            await ctx.invoke(self.join)

        player = self._get_player(ctx)

        source = await YTDLSource.create_source(ctx, self.fart, loop=self.bot.loop)

        await player.queue.put(source)

    @commands.command(name="queue", aliases=["q"])
    async def queue_function(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="I'm not connected to a voice channel", color=discord.Color.green())
            return await ctx.send(embed=embed, delete_after=60)

        player = self._get_player(ctx)
        if player.queue.empty():
            embed = discord.Embed(title="", description="queue is empty", color=discord.Color.green())
            return await ctx.send(embed=embed, delete_after=60)

        seconds = vc.source.duration % (24 * 3600) 
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        if hour > 0:
            duration = "%dh %02dm %02ds" % (hour, minutes, seconds)
        else:
            duration = "%02dm %02ds" % (minutes, seconds)

        # Grabs the songs in the queue...
        upcoming = list(itertools.islice(player.queue._queue, 0, int(len(player.queue._queue))))
        fmt = '\n'.join(f"`{(upcoming.index(_)) + 1}.` [{_['title']}]({_['webpage_url']}) | ` {duration} Requested by: {_['requester']}`\n" for _ in upcoming)
        fmt = f"\n__Now Playing__:\n[{vc.source.title}]({vc.source.web_url}) | ` {duration} Requested by: {vc.source.requester}`\n\n__Up Next:__\n" + fmt + f"\n**{len(upcoming)} songs in queue**"
        embed = Embed(title=f'Queue for {ctx.guild.name}', description=fmt, color=discord.Color.green())

        await ctx.send(embed=embed, delete_after=90)

    @commands.command(name="shuffle", aliases=["shff"])
    async def shuffle(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            embed = Embed(title="", description="I'm not connected to a voice channel", color=Color.green())
            return await ctx.send(embed=embed, delete_after=60)
        player = self._get_player(ctx)
        if player.queue.empty():
            embed = Embed(title="", description="queue is empty", color=Color.green())
            return await ctx.send(embed=embed, delete_after=60)
        player.shuffle()

    @commands.command(name="skip", aliases=["s", "next", "nxt"])
    async def skip(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            embed = Embed(title="", description="I'm not connected to a voice channel", color=Color.green())
            return await ctx.send(embed=embed, delete_after=60)

        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return
        vc.stop()

    @commands.command(name="stop", aliases=["st", "clear", "clr"])
    async def stop(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            embed = Embed(title="", description="I'm not connected to a voice channel", color=Color.green())
            return await ctx.send(embed=embed, delete_after=60)

        player = self._get_player(ctx)
        player.queue._queue.clear()
        vc.stop()
        await ctx.send(embed=Embed(title="", description="Stoped", color=Color.green()), delete_after=60)

    @commands.command(name="resume", aliases=["rs"])
    async def resume(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            embed = Embed(title="", description="I'm not connected to a voice channel", color=discord.Color.green())
            return await ctx.send(embed=embed, delete_after=60)
        elif not vc.is_paused():
            return

        vc.resume()
        await ctx.send(embed=Embed(title="", description="Resuming", color=discord.Color.green()), delete_after=60)

    @commands.command(name="pause", aliases=["ps"])
    async def pause(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_playing():
            embed = Embed(title="", description="I am currently not playing anything", color=discord.Color.green(), delete_after=60)
            return await ctx.send(embed=embed)
        elif vc.is_paused():
            return

        vc.pause()
        await ctx.send(embed=Embed(title="", description="Paused", color=discord.Color.green()), delete_after=60)

    @commands.command(name="join", aliases=["jn"])
    async def join(self, ctx, channel=None):
        if not channel:       
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                embed = Embed(title="", description="No channel to join. Please call `¡join` from a voice channel.", color=Color.green())
                await ctx.send(embed=embed, delete_after=60)
                raise InvalidVoiceChannel('No channel to join. Please either specify a valid channel or join one.')
        voice = ctx.voice_client
        if voice:
            if voice.channel.id == channel.id:
                return
            else:
                try:
                    await voice.move_to(channel)
                except asyncio.TimeoutError:
                    raise VoiceConnectionError(f'Connecting to channel: <{channel}> timed out.')
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Connecting to channel: <{channel}> timed out.')
        await ctx.send(f'**Joined `{channel}`**', delete_after=15)

    @commands.command(name="leave", aliases=["lv"])
    async def leave(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            embed = Embed(title="", description="I'm not connected to a voice channel", color=Color.green())
            return await ctx.send(embed=embed, delete_after=60)

        await ctx.send(embed=Embed(title="", description="Syccesfully disconnected", color=Color.green()), delete_after=60)
        await self.cleanup(ctx.guild)

    @commands.command(name="lyrics", aliases=["lcs"])
    async def lyrics(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            embed = Embed(title="", description="I'm not connected to a voice channel", color=Color.green())
            return await ctx.send(embed=embed, delete_after=60)
        player = self._get_player(ctx)
        if not player.actual_song:
            embed = Embed(title="", description="I am currently not playing anything", color=Color.green())
            return await ctx.send(embed=embed, delete_after=60)

        try:
            song = self.genius.search_song(player.actual_song.title)
        except:
            await ctx.send(embed=Embed(title="", description="Song lyrics not found", color=Color.green()), delete_after=60)
            return
        embed_list = []
        pages = math.ceil(len(song.lyrics)/self.MAX_CHARACTERS)
        for i in range(pages):
            if i+1 < pages:
                embed_list.append(Embed(color=Color.green()).add_field(
                    name=player.actual_song.title, value=song.lyrics[self.MAX_CHARACTERS*i:self.MAX_CHARACTERS*(i+1)]+f"\nPage {i+1}/{pages}"))
            else:
                embed_list.append(Embed(color=Color.green()).add_field(
                    name=player.actual_song.title, value=song.lyrics[self.MAX_CHARACTERS*i::]+f"\nPage {i+1}/{pages}"))
                print(song.lyrics[self.MAX_CHARACTERS*i::])
        paginator = Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
        paginator.add_reaction('⏮️', "first")
        paginator.add_reaction('⏪', "back")
        paginator.add_reaction('⏩', "next")
        paginator.add_reaction('⏭️', "last")
        await paginator.run(embed_list)

    
    def _get_player(self, ctx):
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player

    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    async def __local_check(self, ctx):
        """A local check which applies to all commands in this cog."""
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True

    async def __error(self, ctx, error):
        """A local error handler for all errors arising from commands in this cog."""
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.send('This command can not be used in Private Messages.')
            except discord.HTTPException:
                pass
        elif isinstance(error, InvalidVoiceChannel):
            await ctx.send('Error connecting to Voice Channel. '
                           'Please make sure you are in a valid channel or provide me with one')

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

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
