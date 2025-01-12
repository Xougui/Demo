import discord
import random
from discord.ext import commands, tasks
from discord import app_commands
import Token

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
EXTENSIONS = ("cog.mp", "cog.exemple_cog", "cog.sélecteur", "cog.button")  # Spécifie le chemin avec le sous-dossier "cog"

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

# -------------------------------------------------------------------------
# -----------------------reste du code ici------------------------------------------

@bot.tree.command(name="ping", description="Affiche le ping du bot (latence).")
async def ping(interaction: discord.Interaction):
    latency = bot.latency * 1000
    await interaction.response.send_message(f"Pong!🏓 J'ai une latence de {latency:.2f} millisecondes !")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user in message.mentions:
        embed = discord.Embed(
            title="Qui donc m'a mentionné ?",
            description=(
                "Voici toute une liste de liens qui pourraient t'être utiles\n "
                + "coucou mes bebous\n "
                + "mamamia"
            ),
            color=discord.Color.blue()
        )
        embed.set_footer(text="Créé avec amour par mon développeur @kadawatcha ?")
        await message.channel.send(embed=embed)

# -------------------------------------------------------------------------

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Cette commande n'existe pas.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Il manque un argument.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Vous n'avez pas les permissions nécessaires.")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("Vous ne pouvez pas utiliser cette commande.")
    elif hasattr(error, "original") and isinstance(error.original, discord.Forbidden):
        await ctx.send("Je n'ai pas les permissions nécessaires pour exécuter cette commande.")
    else:
        await ctx.send(f"Une erreur inattendue s'est produite : {error}")

@bot.event
async def on_ready():
    change_status.start()
    print('Bot prêt')
    print("Bot running with:")
    print("Username: ", bot.user.name)
    print("User ID: ", bot.user.id)

@bot.event # load des cogs
async def setup_hook() -> None:
    for extension in EXTENSIONS:
        await bot.load_extension(extension)
    synced = await bot.tree.sync() # sync ici
    print(f"Synced {len(synced)} commands")

bot.run(Token.token)