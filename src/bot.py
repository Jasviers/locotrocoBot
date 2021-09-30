from discord import channel
from discord.ext import commands
from discord.utils import get
from youtube_dl import YoutubeDL
from discord import FFmpegPCMAudio

with open("token.txt", "r") as token:
    TOKEN = token.readline()

bot = commands.Bot(command_prefix="-")

@bot.event
async def on_ready():
    print(f'{bot.user.name} on ready')

@bot.command(name="foo")
async def foo(ctx):
    await ctx.send("bar")

### MUSIC COMMANDS ###

@bot.command(name="play", aliases=["p"])
async def play(ctx, arg1):
    await join(ctx)
    voice = get(bot.voice_clients, guild=ctx.guild)

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(arg1, download=False)
        URL = info['formats'][0]['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
        await ctx.send(f'Musica sonando')

    else:
        await ctx.send("Ya hay musica TONTO")
        return

@bot.command(name="stop", aliases=["st"])
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.stop()
        await ctx.send('Parando tremendo musicardo')

@bot.command(name="resume", aliases=["rs"])
async def resume(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if not voice.is_playing():
        voice.resume()

@bot.command(name="pause", aliases=["ps"])
async def pause(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()

@bot.command(name="join", aliases=["jn"])
async def join(ctx):
    channel = ctx.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if not channel:
        return
    if voice and voice.is_connected():
        if voice.channel == channel:
            pass
        else:
            await voice.move_to(channel)
    else:
        voice = await channel.connect()

@bot.command(name="leave", aliases=["lv"])
async def leave(ctx):
    await ctx.voice_client.disconnect()

bot.run(TOKEN)