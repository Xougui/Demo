import discord
from discord.ext import commands
from discord import ui, app_commands
from discord.ui import LayoutView, Section, TextDisplay

class InfoButton(ui.Button):
    """A custom button that provides more information."""
    def __init__(self):
        """Initializes the InfoButton."""
        super().__init__(label="More Info", style=discord.ButtonStyle.primary, emoji="ℹ️")

    async def callback(self, interaction: discord.Interaction):
        """The callback for the button press."""
        await interaction.response.send_message(
            "Layout views allow for advanced message formatting!",
            ephemeral=True
        )

class ExampleLayoutView(LayoutView):
    """An example layout view that displays a container with text and a button."""
    def __init__(self):
        """Initializes the ExampleLayoutView."""
        super().__init__(timeout=None)

        container = ui.Container(accent_color=discord.Color.blurple())
        text_display = TextDisplay(
            "This is a `LayoutView` with a `Container`.\n"
            "It holds a `Section` with this text and a button."
        )
        text_img_section = Section(text_display, accessory=InfoButton())
        container.add_item(text_img_section)

        self.add_item(container)

class LayoutExamples(commands.Cog):
    """A cog for demonstrating layout views."""
    def __init__(self, bot: commands.Bot):
        """Initializes the LayoutExamples cog."""
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Called when the cog is ready."""
        print("Cog loaded: LayoutExamples")

    @app_commands.command(name="layout_example", description="Shows an example of a layout view.")
    @app_commands.guild_only()
    async def show_layout_example(self, interaction: discord.Interaction):
        """Sends a message with a layout view for demonstration."""
        await interaction.response.send_message(
            "Here is an example of a message with a custom layout:",
            view=ExampleLayoutView()
        )

async def setup(bot: commands.Bot):
    """Sets up the LayoutExamples cog."""
    await bot.add_cog(LayoutExamples(bot))