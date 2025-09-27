import discord
from discord.ext import commands
from discord import app_commands

class DirectMessage(commands.Cog):
    """A cog for sending direct messages to users as the bot."""

    def __init__(self, bot: commands.Bot):
        """Initializes the DirectMessage cog.

        Args:
            bot (commands.Bot): The bot instance.
        """
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Called when the cog is ready."""
        print("Cog loaded: DirectMessage")

    @app_commands.command(name="dm", description="Sends a direct message to a user as the bot.")
    @app_commands.checks.has_permissions(administrator=True)
    async def dm(self, interaction: discord.Interaction, member: discord.Member, content: str):
        """Sends a direct message to a user.

        This command requires administrator permissions.

        Args:
            interaction (discord.Interaction): The interaction object.
            member (discord.Member): The member to send the message to.
            content (str): The content of the message.
        """
        try:
            server_name = interaction.guild.name
            message_to_send = f"**Message from the moderators of {server_name}:**\n\n{content}"
            await member.send(message_to_send)
            await interaction.response.send_message(f"The message has been sent to {member.mention}!", ephemeral=True)

        except discord.Forbidden:
            await interaction.response.send_message("I cannot send DMs to this user. They may have DMs disabled.", ephemeral=True)
        except discord.HTTPException as e:
            print(f"An error occurred while sending the DM: {e}")
            await interaction.response.send_message("An error occurred while trying to send the message.", ephemeral=True)
        except Exception as e:
            print(f"An unexpected error occurred in the 'dm' command: {e}")
            await interaction.response.send_message("An unexpected error occurred.", ephemeral=True)

    @dm.error
    async def dm_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        """Handles errors for the dm command."""
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("You must have administrator permissions to use this command.", ephemeral=True)
        else:
            print(f"An unexpected error occurred in the 'dm' command: {error}")
            await interaction.response.send_message("An unexpected error occurred. Please check the console.", ephemeral=True)

async def setup(bot: commands.Bot):
    """Sets up the DirectMessage cog.

    Args:
        bot (commands.Bot): The bot instance.
    """
    await bot.add_cog(DirectMessage(bot))