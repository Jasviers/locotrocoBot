from discord.ext import commands

class game_commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="tictactoe", aliases=["ttt"])
    async def tictactoe(self, ctx):
        await ctx.send(f'Work In Progress')

    @commands.command(name="slots")
    async def slots(self, ctx):
        await ctx.send(f'Work In Progress')