import discord
from discord.ext import commands
from discord import ui, app_commands
from discord.ui import LayoutView, Section, TextDisplay

class MyButton(ui.Button):
    """A custom button that sends a test message."""
    def __init__(self):
        """Initializes the MyButton button."""
        super().__init__(label="test", style=discord.ButtonStyle.green, emoji="➕")

    async def callback(self, interaction: discord.Interaction):
        """The callback for the button press.

        Sends an ephemeral "test" message.

        Args:
            interaction (discord.Interaction): The interaction from the button press.
        """
        await interaction.response.send_message("test", ephemeral=True)

class Reactionsv2(LayoutView):
    """A layout view that displays a container with a button."""
    def __init__(self):
        """Initializes the Reactionsv2 layout view."""
        super().__init__(timeout=None)

        container = ui.Container(accent_color=discord.Color.blurple())

        text_img_section = Section(ui.TextDisplay("This is a test section."), accessory=MyButton())
        container.add_item(text_img_section)

        self.add_item(container)

class Reactions(commands.Cog):
    """A cog for testing layout views."""
    def __init__(self, bot: commands.Bot):
        """Initializes the Reactions cog.

        Args:
            bot (commands.Bot): The bot instance.
        """
        self.bot = bot
 
    @app_commands.command(name="test-layout", description="Sends a test message with a layout view.")
    @app_commands.guild_only()
    async def auto_reacts(self, interaction: discord.Interaction):
        """Sends a message with a layout view for testing.

        Args:
            interaction (discord.Interaction): The interaction object.
        """
        await interaction.response.defer()
        await interaction.followup.send(view=Reactionsv2())

async def setup(bot: commands.Bot):
    """Sets up the Reactions cog.

    Args:
        bot (commands.Bot): The bot instance.
    """
    await bot.add_cog(Reactions(bot))