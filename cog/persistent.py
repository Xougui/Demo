import discord
from discord.ext import commands
from discord import app_commands

class PersistentView(discord.ui.View):
    """A persistent view with a single button.

    This view is persistent across bot restarts because it has a custom_id
    and is added to the bot in the cog's __init__.
    """
    def __init__(self):
        """Initializes the persistent view.

        The timeout is set to None to make it persistent.
        """
        super().__init__(timeout=None)

    @discord.ui.button(label="Button", style=discord.ButtonStyle.green, custom_id="persistent_button_example")
    async def button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """The callback for the button press.

        Responds with an ephemeral message when the button is clicked.

        Args:
            interaction (discord.Interaction): The interaction from the button press.
            button (discord.ui.Button): The button that was clicked.
        """
        await interaction.response.send_message("You clicked the button!", ephemeral=True)


class PersistentCog(commands.Cog):
    """A cog that demonstrates a persistent view."""
    def __init__(self, bot: commands.Bot):
        """Initializes the PersistentCog.

        This is where the persistent view is registered with the bot.

        Args:
            bot (commands.Bot): The bot instance.
        """
        self.bot = bot
        self.bot.add_view(PersistentView())

    @app_commands.command(name="testbutton", description="Test command for the persistent button.")
    async def testbutton(self, interaction: discord.Interaction):
        """Sends a message with a persistent button.

        Args:
            interaction (discord.Interaction): The interaction object.
        """
        await interaction.response.send_message("Here is a button:", view=PersistentView())

async def setup(bot: commands.Bot):
    """Sets up the PersistentCog.

    Args:
        bot (commands.Bot): The bot instance.
    """
    await bot.add_cog(PersistentCog(bot))