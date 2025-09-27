import discord
from discord.ext import commands
from discord import app_commands

class Exemple(commands.Cog):
    """An example cog to demonstrate basic cog structure."""

    def __init__(self, bot: commands.Bot):
        """Initializes the Exemple cog.

        Args:
            bot (commands.Bot): The bot instance.
        """
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Called when the cog is ready."""
        print("Cog loaded : cog_exemple")

    @app_commands.command(name="exemple", description="An example command")
    async def exemple(self, interaction: discord.Interaction):
        """Responds with a simple 'Exemple' message.

        Args:
            interaction (discord.Interaction): The interaction object.
        """
        await interaction.response.send_message("Exemple")

async def setup(bot: commands.Bot):
    """Sets up the Exemple cog.

    Args:
        bot (commands.Bot): The bot instance.
    """
    
    await bot.add_cog(Exemple(bot))