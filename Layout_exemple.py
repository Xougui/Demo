import discord
from discord.ext import commands
from discord import ui, app_commands
from discord.ui import LayoutView, Section, TextDisplay, Thumbnail, Separator
import sqlite3
from datetime import datetime, timedelta, timezone
import os 

import utils
from utils import verif_emoji
import config




color = config.couleur


class Mon_bouton(ui.Button):
    def __init__(self):
        super().__init__(label="test", style=discord.ButtonStyle.green, emoji="➕")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("test", ephemeral=True)
      


class Reactionsv2(LayoutView):
    def __init__(self):
        super().__init__(timeout=None)


        container = ui.Container(accent_color=color)

        text_img_section = Section(ui.TextDisplay("This is a test section."), accessory=Mon_bouton())
        container.add_item(text_img_section)

        self.add_item(container)

        

            


class Reactions(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.db_file = 'bdd/reactions.db'
        # self.init_db()

    @app_commands.command(name=macmvv2", description="Configure le module d'auto-réactions")
    @app_commands.guild_only()
    async def auto_reacts(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.followup.send(view=Reactionsv2())

    






async def setup(bot):
    await bot.add_cog(Reactions(bot))
