import discord
from discord.ui import View
from discord.ext import commands
from discord import app_commands

v = discord.ui.View
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='*', intents=intents)

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

class Sélecteur(View):

    @discord.ui.select(
            min_values=1, #peut pas mettre moins que 1 choix
            max_values=2, #peut pas mettre plus que 2
            placeholder="choisi un option de test", #ce qui est écris dans la case au début
            options = [
                discord.SelectOption(
                    label="Jour", #le texte
                    emoji="🌞", #l'émoji (facultatif
                    value="0x1", #la valeur pour la fonction d'après
                    description="Températutre du jour" #la description
                ),
                discord.SelectOption(
                    label="Nuit",
                    emoji="🌑",
                    description="Températutre de la nuit"
                ),
            ], #la liste des options qui sont des discord.SelectOption
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select): #la fonction pour détecter quelle choix est fait et faire les actions qui suivent
        if select.values[0] == "0x1": #là on vérifie que c'est jour (la value qu'on a vu en haut)
            print("Jour !")
            if "Cool" not in [x.label for x in select.options]: #il vérifie que l'option n'existe pas et l'ajoute (met à jour le select)
                select.append_option(discord.SelectOption(
                        label="Cool",
                        emoji="🆒",
                        description="C'est cool"
                    ))
            else:
                select.disabled = True #sinon il désactive le select
        await interaction.response.edit_message(view=self) #modifie le message avec la fonction (le self) il rajoute donc une select
        await interaction.followup.send(f"Tu as choisi: {select.values}") #la réponse qui te dit ce que tu as choisis

class Boutton(View):
    @discord.ui.button(
        label="Blurple Button", 
        style=discord.ButtonStyle.blurple
    )
    async def blurple_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Gray Button", style=discord.ButtonStyle.gray)  # or .secondary/.grey
    async def gray_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Green Button", style=discord.ButtonStyle.green)  # or .success
    async def green_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Red Button", style=discord.ButtonStyle.red)  # or .danger
    async def red_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="desactiver tout", style=discord.ButtonStyle.success)
    async def color_changing_button(self, interaction: discord.Interaction, child: discord.ui.Button):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)

class Test(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog loaded : button")

    @bot.tree.command(name="sélecteur", description="jsp")
    async def coucou(self, interaction: discord.Interaction):
        view = Sélecteur()
        await interaction.response.send_message("Ce message a un sélecteur", view=view)
        
    @bot.tree.command(name="button", description="jsp")
    async def button(self, interaction: discord.Interaction):
        view = Boutton()
        view.add_item(discord.ui.Button(label="URL Button", style=discord.ButtonStyle.link, url="https://github.com/Xougui/kadbot/tree/master"))
        await interaction.response.send_message("Ce message a des boutons!", view=view)

@bot.event
async def setup_hook() -> None:
    synced = await bot.tree.sync() #sync ici
    print(f"Synced {len(synced)} commands")

async def setup(bot):
    await bot.add_cog(Test(bot))