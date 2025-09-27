import discord
from discord.ext import commands
from discord import app_commands

v = discord.ui.View
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


class Invite(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog loaded : sélecteur")

@bot.event
async def setup_hook() -> None:
    synced = await bot.tree.sync() #sync ici
    print(f"Synced {len(synced)} commands")

async def setup(bot):
    await bot.add_cog(Invite(bot))