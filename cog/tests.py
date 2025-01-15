import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

class Tests(commands.Cog): # essaye de mettre le nom du cog avc un MAJUSCULE au debut
	
    def __init__(self, bot):
        self.bot = bot
            
    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog loaded : tests")
    
    @bot.tree.command(name="test", description="test")
    async def tests(self, interaction: discord.Interaction):
        server_names = [guild.name for guild in self.bot.guilds]
        await interaction.response.send_message(f"Serveurs : {', '.join(server_names)}")

@bot.event
async def setup_hook() -> None:
    synced = await bot.tree.sync() # sync ici
    print(f"Synced {len(synced)} commands")

async def setup(bot):
    await bot.add_cog(Tests(bot))