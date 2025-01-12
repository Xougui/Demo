import discord
from discord.ext import commands
from discord import app_commands
import json

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

class Counter(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog loaded: Counter")

    def charger_compteurs(self):
        try:
            with open('counter.json', 'r') as f:
                data = json.load(f)
            return data.get('guilds', {})
        except FileNotFoundError:
            return {}

    def ajouter_serveur(self, guild_id, channel_id):
        compteurs = self.charger_compteurs()
        if guild_id not in compteurs:
            compteurs[guild_id] = {"channel_id": channel_id, "value": 0}
        with open('counter.json', 'w') as f:
            json.dump({"guilds": compteurs}, f, indent=4)

    def mettre_a_jour_compteur(self, guild_id, nouvelle_valeur):
        compteurs = self.charger_compteurs()
        if guild_id in compteurs:
            compteurs[guild_id]["value"] = nouvelle_valeur
            with open('counter.json', 'w') as f:
                json.dump({"guilds": compteurs}, f, indent=4)

    @app_commands.command(name="compteur", description="Configurer un compteur de serveur")
    async def envoyer(self, interaction: discord.Interaction, salon: discord.TextChannel):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Vous devez avoir la permission d'administrateur pour utiliser cette commande.", ephemeral=True)
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

        self.ajouter_serveur(interaction.guild.id, salon.id)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return  

        compteurs = self.charger_compteurs()

        if message.guild and message.guild.id in compteurs:
            compteur_info = compteurs[message.guild.id]

            if message.channel.id == compteur_info["channel_id"]:
                if message.content.isdigit():
                    nouvelle_valeur = int(message.content)
                    ancienne_valeur = compteur_info["value"]

                    if nouvelle_valeur == ancienne_valeur + 1:
                        self.mettre_a_jour_compteur(message.guild.id, nouvelle_valeur)
                        
                       
                        await message.add_reaction('✅') 
                    else:
                        
                        await message.channel.send(
                            "Tu sais compter de 1 en 1 ?? !!!! Retourne en CP et quitte Discord si tu sais pas compter.",
                            ephemeral=True
                        )
                        await message.delete()
                else:
                    
                    await message.delete()

async def setup(bot):
    await bot.add_cog(Counter(bot))

@bot.event
async def setup_hook() -> None:
    synced = await bot.tree.sync() #sync ici
    print(f"Synced {len(synced)} commands")
