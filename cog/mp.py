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
    async def mp(self, interaction: discord.Interaction, membre: discord.Member, contenu: str):
        """Sends a private message to a user.

        This command requires administrator permissions.

        Args:
            interaction (discord.Interaction): The interaction object.
            membre (discord.Member): The member to send the message to.
            contenu (str): The content of the message.
        """
        try:
            server_name = interaction.guild.name
            serveur_envoi = f"{contenu}\n-# Envoyé depuis **{server_name}**"
            await membre.send(serveur_envoi)
            await interaction.response.send_message(f"Le message a été envoyé en MP à {membre.mention} !", ephemeral=True)

        except discord.Forbidden:
            await interaction.response.send_message("Je ne peux pas envoyer de MP à cet utilisateur. Assurez-vous que ses MP sont activés.", ephemeral=True)
        except discord.HTTPException as e:
            await interaction.response.send_message(f"Une erreur s'est produite lors de l'envoi du message : {str(e)}", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Une erreur s'est produite : {str(e)}", ephemeral=True)

    @mp.error
    async def mp_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        """Handles errors for the mp command."""
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("Vous devez avoir la permission d'administrateur pour utiliser cette commande.", ephemeral=True)
        else:
            print(f"An unexpected error occurred in 'mp' command: {error}")
            await interaction.response.send_message("Une erreur inattendue s'est produite.", ephemeral=True)

async def setup(bot: commands.Bot):
    """Sets up the MP cog.

    Args:
        bot (commands.Bot): The bot instance.
    """
    await bot.add_cog(MP(bot))