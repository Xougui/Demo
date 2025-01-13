import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

class Test_Compteur(commands.Cog):  # essaye de mettre le nom du cog avc un MAJUSCULE au debut

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog loaded : test_compteur")

    def get_dernier_nombre(self):
        try:
            with open('compteur.txt', 'r') as f:
                contenu = f.read()
                if contenu == '':
                    dernier_nombre = 0
                else:
                    dernier_nombre = int(contenu)
        except FileNotFoundError:
            dernier_nombre = 0
        return dernier_nombre

    def set_dernier_nombre(self, nombre):
        with open('compteur.txt', 'w') as f:
            f.write(str(nombre))

    def get_dernier_utilisateur(self):
        try:
            with open('dernier_utilisateur.txt', 'r') as f:
                dernier_utilisateur = int(f.read())
        except FileNotFoundError:
            dernier_utilisateur = None
        return dernier_utilisateur

    def set_dernier_utilisateur(self, utilisateur):
        with open('dernier_utilisateur.txt', 'w') as f:
            f.write(str(utilisateur))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 1267467304623407167:  # ID du salon spécifique
            if not message.author.bot:  # Ne pas compter les messages des bots
                contenu = message.content
                if contenu.isdigit():  # Vérifier si le message est un nombre
                    nombre = int(contenu)
                    dernier_nombre = self.get_dernier_nombre()  # Récupérer le dernier nombre du compteur
                    dernier_utilisateur = self.get_dernier_utilisateur()  # Récupérer l'utilisateur précédent
                    if dernier_nombre is None or (nombre == dernier_nombre + 1 and message.author.id != dernier_utilisateur):
                        self.set_dernier_nombre(nombre)  # Mettre à jour le dernier nombre du compteur
                        self.set_dernier_utilisateur(message.author.id)  # Mettre à jour l'utilisateur précédent
                        await message.add_reaction('✅')  # Réagir avec un émoji si le nombre est correct
                    else:
                        await message.delete()  # Supprimer le message si le nombre ne suit pas le précédent
                else:
                    await message.delete()  # Supprimer le message si ce n'est pas un nombre

@bot.event
async def setup_hook() -> None:
    synced = await bot.tree.sync() #sync ici
    print(f"Synced {len(synced)} commands")

async def setup(bot):
    await bot.add_cog(Test_Compteur(bot))