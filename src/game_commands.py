from discord.ext import commands
from random import choice

class game_commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.slot_icons = ["🍑", "🍐", "🍆"]

    @commands.command(name="tictactoe", aliases=["ttt"])
    async def tictactoe(self, ctx):
        await ctx.send(f'Work In Progress')

    @commands.command(name="slots")
    async def slots(self, ctx):
        selection = [choice(self.slot_icons) for _ in range(3)]
        result = "[{} {} {}]\n".format(*selection)
        if selection[0]==selection[1] and selection[1]==selection[2]:
            await ctx.send(f'{result}You win!!!')
        else:
            await ctx.send(f'{result}Try again')