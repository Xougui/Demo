import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

class Exemple(commands.Cog): # essaye de mettre le nom du cog avc un MAJUSCULE au debut
	
    def __init__(self, bot):
        self.bot = bot
            
    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog loaded : cog_exemple")

    # -------------------------------------------------------------------------
    # -----------------------code ici------------------------------------------
    @bot.tree.command(name="exemple", description="exemple")
    async def ping(self,interaction: discord.Interaction): # toujours mettre "self" dans la parenthèse quand c'est dans un cog sinon ca crash.
        await interaction.response.send_message("Exemple")
    # -------------------------------------------------------------------------

@bot.event
async def setup_hook() -> None:
    synced = await bot.tree.sync() # sync ici
    print(f"Synced {len(synced)} commands")

async def setup(bot):
    await bot.add_cog(Exemple(bot)) # changer "Exemple" par le nom de votre cog sinon ca marche pas