from discord.ext import commands

from music_commands import music_commands
from fighting_commands import fighting_commands
from game_commands import game_commands

import os

TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="-")

@bot.event
async def on_ready():
    print(f'{bot.user.name} on ready')

bot.add_cog(music_commands(bot))
bot.add_cog(fighting_commands(bot))
bot.add_cog(game_commands(bot))

bot.run(TOKEN)