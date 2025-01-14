import discord
from discord.ext import commands
from discord import app_commands
import json
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Charge les données du fichier JSON
def load_counter_data():
    if os.path.exists('counter.json'):
        with open('counter.json', 'r') as f:
            return json.load(f)
    return {}

# Sauvegarde les données dans le fichier JSON
def save_counter_data(data):
    with open('counter.json', 'w') as f:
        json.dump(data, f, indent=4)

class Counter(commands.Cog):  
    def __init__(self, bot):
        self.bot = bot
        self.guild_counters = load_counter_data()  # Charger les données depuis le fichier JSON

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog loaded: Counter")

    @app_commands.command(name="counter", description="Définir le salon pour le comptage.")
    async def set_counter_channel(self, interaction: discord.Interaction, salon: discord.TextChannel):

        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "<:Error:1328033968381100125> Vous devez avoir la permission d'administrateur pour utiliser cette commande ! ",
                ephemeral=True
            )
            return
        
        embed_compteur = discord.Embed(
            title="Configuration du compteur",
            description=f"Le compteur a bien été défini dans {salon.mention}\nCommencez par envoyer le numéro 1 !",
            color=discord.Color.green()
        )

        await salon.send(embed=embed_compteur)  # Envoi le message dans le salon spécifié
        await interaction.response.send_message(
            f"Votre compteur a bien été défini dans {salon.mention}. Commencez par envoyer le numéro 1 !", ephemeral=True
        )
        """Définir le salon où le comptage doit être effectué"""
        user_id = interaction.user.id
        guild_id = str(interaction.guild.id)

        # Mettre à jour ou ajouter les informations du serveur
        if guild_id not in self.guild_counters:
            self.guild_counters[guild_id] = {"last_number": 0, "last_user_id": None}

        # Mettre à jour le salon de comptage
        self.guild_counters[guild_id]['counter_channel_id'] = salon.id
        save_counter_data(self.guild_counters)  # Sauvegarder les modifications dans le fichier JSON

        await interaction.response.send_message(f"Le salon de comptage a été défini sur {salon.name}.", ephemeral=True)

    def get_counter_channel(self, guild_id):
        """Récupère le salon de comptage du serveur"""
        guild_data = self.guild_counters.get(str(guild_id))
        if guild_data:
            return guild_data.get('counter_channel_id')
        return None

    def get_last_number(self, guild_id):
        """Récupère le dernier nombre du serveur"""
        guild_data = self.guild_counters.get(str(guild_id))
        if guild_data:
            return guild_data.get('last_number', 0)
        return 0

    def get_last_user(self, guild_id):
        """Récupère l'ID du dernier utilisateur qui a compté"""
        guild_data = self.guild_counters.get(str(guild_id))
        if guild_data:
            return guild_data.get('last_user_id')
        return None

    def set_last_number(self, guild_id, number):
        """Met à jour le dernier nombre du serveur"""
        if str(guild_id) in self.guild_counters:
            self.guild_counters[str(guild_id)]['last_number'] = number
            save_counter_data(self.guild_counters)

    def set_last_user(self, guild_id, user_id):
        """Met à jour l'ID du dernier utilisateur du serveur"""
        if str(guild_id) in self.guild_counters:
            self.guild_counters[str(guild_id)]['last_user_id'] = user_id
            save_counter_data(self.guild_counters)

    @commands.Cog.listener()
    async def on_message(self, message):
        """Gère le comptage dans le salon défini"""
        if message.author.bot:
            return

        # Vérifier si un salon a été défini pour le comptage
        counter_channel_id = self.get_counter_channel(message.guild.id)
        if not counter_channel_id or message.channel.id != counter_channel_id:
            return  # Ignore les messages dans un salon qui n'est pas le salon de comptage

        # Logique pour gérer le comptage
        contenu = message.content
        if contenu.isdigit():  # Vérifier si le message est un nombre
            nombre = int(contenu)
            dernier_nombre = self.get_last_number(message.guild.id)  # Récupérer le dernier nombre du compteur
            dernier_utilisateur = self.get_last_user(message.guild.id)  # Récupérer l'utilisateur précédent
            if dernier_nombre == nombre - 1 and message.author.id != dernier_utilisateur:
                self.set_last_number(message.guild.id, nombre)  # Mettre à jour le dernier nombre du compteur
                self.set_last_user(message.guild.id, message.author.id)  # Mettre à jour l'utilisateur précédent
                await message.add_reaction('<a:check:1328035248511909992>')  # Réagir avec un émoji si le nombre est correct
            else:
                await message.delete()  # Supprimer le message si le nombre ne suit pas le précédent
        else:
            await message.delete()  # Supprimer le message si ce n'est pas un nombre

@bot.event
async def setup_hook() -> None:
    synced = await bot.tree.sync() #sync ici
    print(f"Synced {len(synced)} commands")

async def setup(bot):
    await bot.add_cog(Counter(bot))