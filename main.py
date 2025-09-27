import discord
import random
import os
from discord.ext import commands, tasks
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


# List of cogs to load on startup
EXTENSIONS = ("cog.mp",
              "cog.example_cog",
              "cog.selector",
              "cog.button",
              "cog.layout_example",
              "cog.counter",
              "cog.persistent",
              "cog.logging")


def isOwner(ctx):
    """Checks if the command author is the owner of the bot.

    Args:
        ctx (commands.Context): The context of the command.

    Returns:
        bool: True if the author is the owner, False otherwise.
    """
    return ctx.author.id == OWNER_ID

@bot.command()
@commands.check(isOwner)
async def start(ctx, seconds: int = 3):
    """Starts the status changing task with a new interval.

    This command can only be used by the bot owner.

    Args:
        ctx (commands.Context): The context of the command.
        seconds (int, optional): The interval in seconds for the status change. Defaults to 3.
    """
    change_status.change_interval(seconds=seconds)

@tasks.loop(seconds=10)
async def change_status():
    """Changes the bot's presence periodically.

    Cycles through a list of statuses and sets them as the bot's activity.
    """
    status = ["Watching over the server", "Use /help for commands", "Developed by the community"]
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(random.choice(status)))

# -------------------------------------------------------------------------
# ----------------------- Main Commands -----------------------------------

@bot.tree.command(name="ping", description="Displays the bot's latency.")
async def ping(interaction: discord.Interaction):
    """Displays the bot's latency.

    Args:
        interaction (discord.Interaction): The interaction object.
    """
    latency = bot.latency * 1000
    await interaction.response.send_message(f"Pong!🏓 My latency is {latency:.2f}ms!")

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
            title="Did someone mention me?",
            description=(
                "Here are some helpful links:\n"
                "- [GitHub Repository](https://github.com/Xougui/demobot)\n"
                "- [Discord.py Documentation](https://discordpy.readthedocs.io/en/latest/)"
            ),
            color=discord.Color.blue()
        )
        embed.set_footer(text="This bot is a learning project.")
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
        await ctx.send(f"Here is a permanent invite to the server: {invite.url}")
    else:
        await ctx.send("You don't have the required permissions to create an invite.")

# -------------------------------------------------------------------------

@bot.event
async def on_command_error(ctx, error):
    """Handles errors that occur during command execution.

    Args:
        ctx (commands.Context): The context of the command.
        error (commands.CommandError): The error that was raised.
    """
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("That command was not found.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("A required argument is missing.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have the necessary permissions to use this command.")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("You cannot use this command.")
    elif hasattr(error, "original") and isinstance(error.original, discord.Forbidden):
        await ctx.send("I don't have the permissions required to perform this command.")
    else:
        await ctx.send(f"An unexpected error occurred: {error}")

# The on_interaction event for logging is now handled in cog/logging.py

@bot.event
async def on_ready():
    """Called when the bot is ready and online."""
    change_status.start()
    print('Bot is ready.')
    print("Bot running with:")
    print("Username: ", bot.user.name)
    print("User ID: ", bot.user.id)

@bot.event # Load cogs
async def setup_hook() -> None:
    """Asynchronously sets up the bot by loading extensions and syncing the command tree."""
    for extension in EXTENSIONS:
        await bot.load_extension(extension)
    synced = await bot.tree.sync() # Sync commands
    print(f"Synced {len(synced)} commands")

bot.run(TOKEN)
