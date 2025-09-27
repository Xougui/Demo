import discord
from discord.ext import commands
from discord import app_commands

class MP(commands.Cog):
    """A cog for sending private messages to users as the bot."""

    def __init__(self, bot: commands.Bot):
        """Initializes the MP cog.

        Args:
            bot (commands.Bot): The bot instance.
        """
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Called when the cog is ready."""
        print("Cog loaded : mp")

    @app_commands.command(name="mp", description="Sends a private message to a user as the bot.")
    @app_commands.checks.has_permissions(administrator=True)
    async def mp(self, interaction: discord.Interaction, member: discord.Member, content: str):
        """Sends a private message to a user.

        This command requires administrator permissions.

        Args:
            interaction (discord.Interaction): The interaction object.
            member (discord.Member): The member to send the message to.
            content (str): The content of the message.
        """
        try:
            server_name = interaction.guild.name
            message_to_send = f"{content}\n-# Sent from **{server_name}**"
            await member.send(message_to_send)
            await interaction.response.send_message(f"The message has been sent via DM to {member.mention}!", ephemeral=True)

        except discord.Forbidden:
            await interaction.response.send_message("I cannot send DMs to this user. Please ensure their DMs are enabled.", ephemeral=True)
        except discord.HTTPException as e:
            await interaction.response.send_message(f"An error occurred while sending the message: {str(e)}", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}", ephemeral=True)

    @mp.error
    async def mp_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        """Handles errors for the mp command."""
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("You must have administrator permissions to use this command.", ephemeral=True)
        else:
            print(f"An unexpected error occurred in 'mp' command: {error}")
            await interaction.response.send_message("An unexpected error occurred.", ephemeral=True)

async def setup(bot: commands.Bot):
    """Sets up the MP cog.

    Args:
        bot (commands.Bot): The bot instance.
    """
    await bot.add_cog(MP(bot))