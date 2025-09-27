import discord
from discord.ui import View
from discord.ext import commands
from discord import app_commands

class ButtonView(View):
    """A view that displays several buttons with different styles.

    The buttons disable themselves when clicked.
    """
    def __init__(self):
        """Initializes the ButtonView."""
        super().__init__()

    @discord.ui.button(
        label="Blurple Button",
        style=discord.ButtonStyle.blurple
    )
    async def blurple_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """A blurple button that disables itself on click.

        Args:
            interaction (discord.Interaction): The interaction object.
            button (discord.ui.Button): The button that was clicked.
        """
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Gray Button", style=discord.ButtonStyle.gray)
    async def gray_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """A gray button that disables itself on click.

        Args:
            interaction (discord.Interaction): The interaction object.
            button (discord.ui.Button): The button that was clicked.
        """
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Green Button", style=discord.ButtonStyle.green)
    async def green_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """A green button that disables itself on click.

        Args:
            interaction (discord.Interaction): The interaction object.
            button (discord.ui.Button): The button that was clicked.
        """
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Red Button", style=discord.ButtonStyle.red)
    async def red_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """A red button that disables itself on click.

        Args:
            interaction (discord.Interaction): The interaction object.
            button (discord.ui.Button): The button that was clicked.
        """
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Disable All", style=discord.ButtonStyle.success)
    async def disable_all_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """A button that disables all other buttons in the view.

        Args:
            interaction (discord.Interaction): The interaction object.
            button (discord.ui.Button): The button that was clicked.
        """
        for child_button in self.children:
            child_button.disabled = True
        await interaction.response.edit_message(view=self)

class CogButton(commands.Cog):
    """A cog for demonstrating discord.ui.Button functionality."""

    def __init__(self, bot: commands.Bot):
        """Initializes the CogButton cog.

        Args:
            bot (commands.Bot): The bot instance.
        """
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Called when the cog is ready."""
        print("Cog loaded : button")

    @app_commands.command(name="button", description="Sends a message with buttons.")
    async def button(self, interaction: discord.Interaction):
        """Sends a message with a view containing several buttons.

        Args:
            interaction (discord.Interaction): The interaction object.
        """
        view = ButtonView()
        view.add_item(discord.ui.Button(label="URL Button", style=discord.ButtonStyle.link, url="https://github.com/Xougui/kadbot/tree/master"))
        await interaction.response.send_message("This message has buttons!", view=view)

async def setup(bot: commands.Bot):
    """Sets up the CogButton cog.

    Args:
        bot (commands.Bot): The bot instance.
    """
    await bot.add_cog(CogButton(bot))