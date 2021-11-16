import discord
from discord.ext import commands
from youtube_dl import YoutubeDL

import asyncio
from async_timeout import timeout
import random
from functools import partial
from urllib.parse import urlparse


ytdlopts = {
    'format': 'bestaudio',
    'noplaylist': 'True'}

ffmpegopts = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = YoutubeDL(ytdlopts)


class VoiceConnectionError(commands.CommandError):
    """Custom Exception class for connection errors."""


class InvalidVoiceChannel(VoiceConnectionError):
    """Exception for cases of invalid Voice Channels."""

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester

        self.title = data.get('title')
        self.web_url = data.get('webpage_url')
        self.duration = data.get('duration')

    def __getitem__(self, item: str):
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop):
        loop = loop or asyncio.get_event_loop()

        url_result = urlparse(search)
        if all([url_result.scheme, url_result.netloc, url_result.path]):
            to_run = partial(ytdl.extract_info, url=search, download=False)
            data = await loop.run_in_executor(None, to_run)
        else:
            to_run = partial(ytdl.extract_info, url=f"ytsearch:{search}", download=False)
            data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            data = data['entries'][0]

        embed = discord.Embed(title="", description=f"Queued [{data['title']}]({data['webpage_url']}) [{ctx.author.mention}]", color=discord.Color.green())
        await ctx.send(embed=embed, delete_after=60)

       
        return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}

    @classmethod
    async def regather_stream(cls, data, *, loop):
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url']), data=data, requester=requester)


class MusicPlayer:
    def __init__(self, ctx):
        self.bot = ctx.bot
        self.ctx = ctx
        self.channel = self.ctx.channel
        self.guild = self.ctx.guild
        self.cog = self.ctx.cog

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.actual_song = None
        self.np = None
        self.volume = 0.5

        self.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try:
                async with timeout(300):
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                return self.destroy(self.guild)

            if not isinstance(source, YTDLSource):
                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except Exception as e:
                    await self.channel.send(f'There was an error processing your song.\n'
                                             f'```css\n[{e}]\n```')
                    continue

            source.volume = self.volume
            self.actual_song = source

            self.guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            embed = discord.Embed(title="Now playing", description=f"[{source.title}]({source.web_url}) [{source.requester.mention}]", color=discord.Color.green())
            self.np = await self.channel.send(embed=embed)
            await self.next.wait()

            source.cleanup()
            await self.np.delete()
            self.actual_song = None

    def shuffle(self):
        random.shuffle(self.queue)

    def destroy(self, guild):
        return self.bot.loop.create_task(self.cog.cleanup(guild))