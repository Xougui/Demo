import discord
import random
from discord.ext import commands, tasks
from discord import app_commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
EXTENSIONS = ("cog.cog_exemple", "cog.button") #pr le nom des fichiers pas obligé de mettre un "_" pr les espaces. t'as le droit d'ne mettre

def isOwner(ctx):
    return ctx.message.author.id == 946098490654740580 #ton identifiant

@bot.command()
@commands.check(isOwner) #commande à ne pas utiliser car seul le bot utiliseras pour l'interval (mais je sais pas si depuis la v2 c'est tjrs utlie on sait jamais :)
async def start(ctx, secondes = 3):
    change_status.change_interval(seconds = secondes)

@tasks.loop(seconds = 10)
async def change_status():
    status = ["statut"]
    await bot.change_presence(status = discord.Status.online, activity = discord.Game(random.choice(status)))

# COMMANDE DU BOT qu'on peut pas mettre dans un cog ⬇

@bot.tree.command(name="ping", description="Affiche le ping du bot (latence).")
async def ping(interaction: discord.Interaction):    
    latency = bot.latency
    truelatency = latency * 1000
    await interaction.response.send_message(f"Pong!🏓 J'ai une latence de {truelatency} millisecondes !")
    
# -------------------------------------------------------------------------
# -----------------------code ici------------------------------------------
# -------------------------------------------------------------------------

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		await ctx.send("Mmmmmmh, j'ai bien l'impression que cette commande n'existe pas :/")

	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("Il manque un argument.")
	elif isinstance(error, commands.MissingPermissions):
		await ctx.send("Vous n'avez pas les permissions pour faire cette commande.")
	elif isinstance(error, commands.CheckFailure):
		await ctx.send("Oups vous ne pouvez iutilisez cette commande.")
	if isinstance(error.original, discord.Forbidden):
		await ctx.send("Oups, je n'ai pas les permissions nécéssaires pour faire cette commmande")

@bot.event
async def on_ready():
    change_status.start()
    print('Bot prêt')
    print("Bot running with:")
    print("Username: ", bot.user.name)
    print("User ID: ", bot.user.id)

@bot.event
async def setup_hook() -> None:
    for extension in EXTENSIONS:
        await bot.load_extension(extension)
    synced = await bot.tree.sync() #sync ici
    print(f"Synced {len(synced)} commands")

bot.run('token')