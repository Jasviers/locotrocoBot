from discord.ext import commands
import discord

from music_commands import music_commands
from fighting_commands import fighting_commands
from game_commands import game_commands
from utility_commands import utility_commands

import os
import asyncio

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
intents.members = True
intents.typing = True
intents.presences = True

bot = commands.Bot(command_prefix="-", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} on ready')

async def set_cogs():
    await bot.add_cog(music_commands(bot))
    await bot.add_cog(fighting_commands(bot))
    await bot.add_cog(game_commands(bot))
    await bot.add_cog(utility_commands(bot))

asyncio.run(set_cogs())
bot.run(TOKEN)
