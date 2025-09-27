import discord
from discord.ui import View, Select
from discord.ext import commands
from discord import app_commands

class SelectorView(View):
    """A view that contains a select menu for users to interact with.

    This select menu demonstrates dynamic option adding and disabling.
    """

    @discord.ui.select(
        min_values=1,
        max_values=2,
        placeholder="Choose a test option",
        options=[
            discord.SelectOption(
                label="Day",
                emoji="🌞",
                value="day",
                description="Temperature for the day"
            ),
            discord.SelectOption(
                label="Night",
                emoji="🌑",
                value="night",
                description="Temperature for the night"
            ),
        ],
    )
    async def select_callback(self, interaction: discord.Interaction, select: Select):
        """Callback for the select menu.

        Handles user selections, dynamically adds an option, or disables the menu.

        Args:
            interaction (discord.Interaction): The interaction from the selection.
            select (discord.ui.Select): The select menu that was used.
        """
        if "day" in select.values:
            print("Day!")
            # Add a new option if it doesn't exist
            if "Cool" not in [opt.label for opt in select.options]:
                select.add_option(
                    label="Cool",
                    emoji="🆒",
                    description="It's cool"
                )
            # If the "Cool" option is also selected, disable the menu
            if len(select.values) > 1 and "Cool" in select.values:
                 select.disabled = True

        await interaction.response.edit_message(view=self)
        await interaction.followup.send(f"You chose: {', '.join(select.values)}", ephemeral=True)


class CogSelector(commands.Cog):
    """A cog for demonstrating discord.ui.Select functionality."""

    def __init__(self, bot: commands.Bot):
        """Initializes the CogSelector cog.

        Args:
            bot (commands.Bot): The bot instance.
        """
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Called when the cog is ready."""
        print("Cog loaded : selector")

    @app_commands.command(name="selector", description="Sends a message with a select menu.")
    async def selector_command(self, interaction: discord.Interaction):
        """Sends a message with a view containing a select menu.

        Args:
            interaction (discord.Interaction): The interaction object.
        """
        view = SelectorView()
        await interaction.response.send_message("This message has a select menu:", view=view)


async def setup(bot: commands.Bot):
    """Sets up the CogSelector cog.

    Args:
        bot (commands.Bot): The bot instance.
    """
    await bot.add_cog(CogSelector(bot))