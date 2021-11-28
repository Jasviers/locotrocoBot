from discord.ext import commands
from discord.utils import get
from discord import Embed, Color
from DiscordUtils import Pagination

class fighting_commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.voice = None
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        self.framedata_url = "https://fullmeter.com/fatonline/#/framedata/SFV/"
        self.sfv_characters = ["Ryu", "Chun-Li", "Nash", "M.Bison", "Cammy",
        "Birdie", "Ken", "Necalli", "Vega", "R.Mika", "Rashid", "Karin", "Zangief",
        "Laura", "Dhalsim", "F.A.N.G", "Alex", "Guile", "Ibuki", "Balrog", "Juri",
        "Urien", "Akuma", "Kolin", "Ed", "Abigail", "Menat", "Zeku (Old)",
        "Zeku (Young)", "Sakura", "Blanka", "Falke", "Cody", "G", "Sagat", "Kage",
        "E.Honda", "Lucia", "Poison", "Gill", "Seth", "Dan", "Rose", "Oro", "Akira"]
        self.sfv_zeku_hate = ["Ryu", "Chun-Li", "Nash", "M.Bison", "Cammy",
        "Birdie", "Ken", "Necalli", "Vega", "R.Mika", "Rashid", "Karin", "Zangief",
        "Laura", "Dhalsim", "F.A.N.G", "Alex", "Guile", "Ibuki", "Balrog", "Juri",
        "Urien", "Akuma", "Kolin", "Ed", "Abigail", "Menat", "Zeku%20(Old)",
        "Zeku%20(Young)", "Sakura", "Blanka", "Falke", "Cody", "G", "Sagat", "Kage",
        "E.Honda", "Lucia", "Poison", "Gill", "Seth", "Dan", "Rose", "Oro", "Akira"]
        self.sfv_characters.sort()
        self.sfv_zeku_hate.sort()

    ## tiratela command correspond to this place

    @commands.command(name="moneymatch", aliases=["mm"])
    async def money_match(self, ctx):
        await ctx.send(f'Work In Progress')

    @commands.command(name="chaparrin", aliases=["chpn"])
    async def chaparrin(self, ctx):
        await ctx.send(f'Work In Progress')

    @commands.command(name="framedata", aliases=["fd"])
    async def frame_data(self, ctx):
        kekos = "\n".join(f"[{keko}]({self.framedata_url+keko_url})" for keko, keko_url in zip(self.sfv_characters, self.sfv_zeku_hate))
        kekos_embed = Embed(title="FrameData from Street Fighter V:", description=kekos, color=Color.green())
        await ctx.send(embed=kekos_embed)
    