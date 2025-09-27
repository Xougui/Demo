import discord
from discord.ext import commands
from discord import ui, app_commands
from discord.ui import LayoutView, Section, TextDisplay, Thumbnail, Separator

from datetime import datetime, timedelta, timezone
import os 






class Mon_bouton(ui.Button):
    def __init__(self):
        super().__init__(label="test", style=discord.ButtonStyle.green, emoji="➕")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("test", ephemeral=True)
      


class Reactionsv2(LayoutView):
    def __init__(self):
        super().__init__(timeout=None)


        container = ui.Container(accent_color=discord.Color.blurple())

        text_img_section = Section(ui.TextDisplay("This is a test section."), accessory=Mon_bouton())
        container.add_item(text_img_section)

        self.add_item(container)

        

            


class Reactions(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
 
    @app_commands.command(name="Test-layout", description="Embed v2")
    @app_commands.guild_only()
    async def auto_reacts(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.followup.send(view=Reactionsv2())

    






async def setup(bot):
    await bot.add_cog(Reactions(bot))