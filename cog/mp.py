import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

class MP(commands.Cog):  # essaye de mettre le nom du cog avc un MAJUSCULE au debut

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog loaded : mp")

    @bot.tree.command(name="mp", description="Envoyer un message privé à un utilisateur sous mon identité")
    async def mp(self, interaction: discord.Interaction, membre: discord.Member, contenu: str):
        try:
            server_name = interaction.guild.name
            serveur_envoi = f"{contenu}\n-# Envoyé depuis **{server_name}**"
            await membre.send(serveur_envoi)
            await interaction.response.send_message(f"Le message a été envoyé en MP à {membre.mention} !", ephemeral=True)

            if not isinstance(interaction.user, discord.Member) or not interaction.user.guild_permissions.administrator:
                if not interaction.user.guild_permissions.administrator:
                    await interaction.response.send_message("Vous devez avoir la permission d'administrateur pour utiliser cette commande.", ephemeral=True)
                return
            if not interaction.channel or not isinstance(interaction.channel, discord.TextChannel):
                if not isinstance(interaction.channel, discord.TextChannel):
                    if isinstance(interaction.channel, discord.DMChannel):
                        await interaction.response.send_message("Cette commande ne peut pas être utilisée en MP.", ephemeral=True)
                return
            if not isinstance(membre, discord.Member) or not membre.dm_channel:
                await interaction.response.send_message("Je ne peux pas envoyer de MP à cet utilisateur. Assurez-vous que ses MP sont activés.", ephemeral=True)
                return

        except discord.Forbidden:
            await interaction.response.send_message("Je ne peux pas envoyer de MP à cet utilisateur. Assurez-vous que ses MP sont activés.", ephemeral=True)
        except discord.HTTPException as e:
            await interaction.response.send_message(f"Une erreur s'est produite lors de l'envoi du message : {str(e)}", ephemeral=True)
        except AttributeError as e:
            await interaction.response.send_message(f"Erreur : {str(e)}", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Une erreur s'est produite : {str(e)}", ephemeral=True)

@bot.event
async def setup_hook() -> None:
    synced = await bot.tree.sync() #sync ici
    print(f"Synced {len(synced)} commands")

async def setup(bot):
    await bot.add_cog(MP(bot))