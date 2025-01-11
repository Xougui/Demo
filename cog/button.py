import discord
from discord.ui import View
from discord.ext import commands
from discord import app_commands

v = discord.ui.View
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

class Boutton(View):
    @discord.ui.button(
        label="Blurple Button", 
        style=discord.ButtonStyle.blurple
    )
    async def blurple_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Gray Button", style=discord.ButtonStyle.gray)  # ou .secondary/.grey
    async def gray_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Green Button", style=discord.ButtonStyle.green)  # ou .success
    async def green_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Red Button", style=discord.ButtonStyle.red)  # ou .danger
    async def red_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="desactiver tout", style=discord.ButtonStyle.success)
    async def color_changing_button(self, interaction: discord.Interaction, child: discord.ui.Button):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)

class CogButton(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog loaded : button")
        
    @bot.tree.command(name="button", description="jsp")
    async def button(self, interaction: discord.Interaction):
        view = Boutton()
        view.add_item(discord.ui.Button(label="URL Button", style=discord.ButtonStyle.link, url="https://github.com/Xougui/kadbot/tree/master"))
        await interaction.response.send_message("Ce message a des boutons!", view=view)

@bot.event
async def setup_hook() -> None:
    synced = await bot.tree.sync() # sync ici
    print(f"Synced {len(synced)} commands")

async def setup(bot):
    await bot.add_cog(CogButton(bot))