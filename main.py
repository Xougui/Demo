import discord
import random
from discord.ext import commands, tasks
from discord import app_commands


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


# Mettre les extentiions une par une ou créer une fonction qui les charge toutes automatiquement 
# ici on les met une par une ( ne pas oublier la VIRGULE entre chaque cog )
EXTENSIONS = ("cog.mp",
               "cog.exemple_cog",
               "cog.selecteur",
               "cog.button", 
               "cog.test_compteur",
                "cog.tests", 
                "cog.Layout_exemple",
                "cog.counter",
                "cog.persistant")


def isOwner(ctx):
    """Checks if the command author is the owner of the bot.

    Args:
        ctx (commands.Context): The context of the command.

    Returns:
        bool: True if the author is the owner, False otherwise.
    """
    return ctx.author.id == 1178647820052467823

@bot.command()
@commands.check(isOwner)
async def start(ctx, secondes: int = 3):
    """Starts the status changing task with a new interval.

    This command can only be used by the bot owner.

    Args:
        ctx (commands.Context): The context of the command.
        secondes (int, optional): The interval in seconds for the status change. Defaults to 3.
    """
    change_status.change_interval(seconds=secondes)

@tasks.loop(seconds=10)
async def change_status():
    """Changes the bot's presence periodically.

    Cycles through a list of statuses and sets them as the bot's activity.
    """
    status = ["mets tes statuts ici", "par exemple !help", "ou autre chose"]
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(random.choice(status)))

# -------------------------------------------------------------------------
# -----------------------reste du code ici------------------------------------------

@bot.tree.command(name="ping", description="Affiche le ping du bot (latence).")
async def ping(interaction: discord.Interaction):
    """Displays the bot's latency.

    Args:
        interaction (discord.Interaction): The interaction object.
    """
    latency = bot.latency * 1000
    await interaction.response.send_message(f"Pong!🏓 J'ai une latence de {latency:.2f} millisecondes !")

@bot.event
async def on_message(message):
    """Handles messages sent in the server.

    If the bot is mentioned, it sends an embed with useful links.

    Args:
        message (discord.Message): The message object.
    """
    if message.author == bot.user:
        return

    if bot.user in message.mentions:
        embed = discord.Embed(
            title="Who mentioned me?",
            description=(
                "Here is a list of links that might be useful to you!\n"
                "- Link 1\n"
                "- Link 2"
            ),
            color=discord.Color.blue()
        )
        embed.set_footer(text="Created with love by my developer.")
        await message.channel.send(embed=embed)

@bot.command()
async def create_invite(ctx):
    """Creates a permanent invite to the server.

    This command can only be used by users with the 'manage_guild' permission.

    Args:
        ctx (commands.Context): The context of the command.
    """
    if ctx.author.guild_permissions.manage_guild:
        invite = await ctx.guild.create_invite(max_age=0, max_uses=0)
        await ctx.send(f"Voici l'invitation pour rejoindre le serveur : {invite.url}")
    else:
        await ctx.send("Vous n'avez pas la permission de créer des invitations pour ce serveur.")

# -------------------------------------------------------------------------

@bot.event
async def on_command_error(ctx, error):
    """Handles errors that occur during command execution.

    Args:
        ctx (commands.Context): The context of the command.
        error (commands.CommandError): The error that was raised.
    """
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

log_channel_id = 1267467310445236224  # ID du salon où envoyer les logs
log_server_id = 1046104471089983568  # ID du serveur où envoyer les logs

# Créez un événement qui écoute les commandes bot.tree
@bot.event
async def on_interaction(interaction):
    """Logs application command usage to a specific channel.

    Args:
        interaction (discord.Interaction): The interaction object.
    """
    # Vérifiez si l'interaction est une commande bot.tree
    if interaction.type == discord.InteractionType.application_command:
        # Récupérez les informations de la commande
        command_name = interaction.data.get('name')
        command_content = interaction.data.get('options', [{}])[0].get('value') if interaction.data.get('options') else None
        author = interaction.user
        channel = interaction.channel
        guild = interaction.guild
        options = interaction.data.get('options', [])

        # Créez un embed pour les logs
        log_embed = discord.Embed(
            title=f"Commande {command_name} exécutée",
            color=0x00ff00
        )
        log_embed.add_field(name="Auteur", value=author.mention, inline=True)
        log_embed.add_field(name="Salon", value=channel.mention, inline=True)
        log_embed.add_field(name="Serveur", value=guild.name, inline=True)

        for option in options:
            log_embed.add_field(name=option.get('name'), value=option.get('value'), inline=False)

        # Récupérez le message de la commande
        message = await interaction.original_response()

        # Ajoutez le lien du message de la commande aux logs
        if message:
            log_embed.add_field(name="Lien du message", value=message.jump_url, inline=False)

        # Envoyez les logs dans le salon spécifique
        log_channel = bot.get_channel(log_channel_id)
        await log_channel.send(embed=log_embed)

@bot.event
async def on_ready():
    """Called when the bot is ready and online."""
    change_status.start()
    print('Bot prêt')
    print("Bot running with:")
    print("Username: ", bot.user.name)
    print("User ID: ", bot.user.id)

@bot.event # load des cogs
async def setup_hook() -> None:
    """Asynchronously sets up the bot by loading extensions and syncing the command tree."""
    for extension in EXTENSIONS:
        await bot.load_extension(extension)
    synced = await bot.tree.sync() # sync ici
    print(f"Synced {len(synced)} commands")

bot.run('token')
