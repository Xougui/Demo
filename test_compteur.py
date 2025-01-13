import discord
import random
from discord.ext import commands, tasks
from discord import app_commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
# EXTENSIONS = ("cog.mp", "cog.exemple_cog", "cog.sélecteur", "cog.button")  # Spécifie le chemin avec le sous-dossier "cog"

def isOwner(ctx):
    return ctx.author.id == 1178647820052467823

@bot.command()
@commands.check(isOwner)
async def start(ctx, secondes: int = 3):
    change_status.change_interval(seconds=secondes)

@tasks.loop(seconds=10)
async def change_status():
    status = ["mets tes statuts ici"]
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(random.choice(status)))

@bot.event
async def on_message(message):
    if message.author == 1:
        return
    
    await message.channel.send("ok")

@bot.event
async def on_ready():
    change_status.start()
    print('Bot prêt')
    print("Bot running with:")
    print("Username: ", bot.user.name)
    print("User ID: ", bot.user.id)

@bot.event # load des cogs
async def setup_hook() -> None:
    synced = await bot.tree.sync() # sync ici
    print(f"Synced {len(synced)} commands")

bot.run('MTE3MDI3MTEzNTU5MDUzNTIyOA.GC_eUF.6urFzKh3_WM09sn6JorFxlhvibx9CWSIxzt-dY')