import discord
from discord.ext import commands, tasks
from discord import app_commands
from datetime import timedelta, datetime


class Bouton(discord.ui.Button):
   @discord.ui.button(label="Bouton", style=discord.ButtonStyle.green, custom_id="obligatoire") # custon id obligatoire pour les persistent views
   async def bouton(self, interaction: discord.Interaction, button: discord.ui.Button):
       await interaction.response.send_message("Vous avez cliqué sur le bouton !", ephemeral=True)


class Macommande(commands.Cog):
    def __init__(self, bot: commands.Bot): # "bot : commands.Bot"  est obligatoire pour la vue persistante
        self.bot = bot
        bot.add_view(Bouton()) # Obligatoire pour les persistent views
    
    @app_commands.command(name="testbouton", description="Commande de test pour le bouton")
    async def testbouton(self, interaction: discord.Interaction):
        await interaction.response.send_message("Voici un bouton :", view=Bouton()) # appel de la la vue



def setup(bot):
    bot.add_cog(Macommande(bot))
