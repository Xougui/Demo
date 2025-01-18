import discord
import random
from discord.ext import commands, tasks
from discord import app_commands
from discord.ui import View
import Token
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
EXTENSIONS = ("cog.mp","cog.counter","cog.SL",)  

#----------------------------------------- Lien -------------------------------------------------------------------------------
@bot.command()
async def invite(self, ctx):
    if ctx.author.permissions_in(ctx.channel).create_instant_invite:
        invite = await ctx.channel.create_invite(max_age=0, max_uses=0)
        await ctx.send(f"Voici votre lien qui n'expirera absolument **jamais** !\n{invite.url}")
        await ctx.send("<:Error:1328033968381100125> Humm il faudra penser à changer mes perms pour que je puisse répondre à touts vos besoins")
    else:
        await ctx.send("<:Error:1328033968381100125> Malheureusement, tu n'as pas les perms pour partager ce beau serveur")



# ---------------------------------- Status ------------------------------------------------------------------------------------
@tasks.loop(seconds=10)
async def change_status():
    status = ["Bonjour a tous ! en dev "]
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(random.choice(status)))
# ----------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------- Latence du bot  ---------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------
@bot.tree.command(name="ping", description="Affiche le ping du bot (latence).")
async def ping(interaction: discord.Interaction):
    latency = bot.latency * 1000
    await interaction.response.send_message(f"Pong 🏓 ! \nJ'ai une latence de `{latency:.2f}` ms !")
# ----------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------- Réponsse aux pings ---------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user in message.mentions:
        embed = discord.Embed(
            title="Qui donc m'a mentionné ?",
            description=("Besoin d'aide ? utilise ''/help'' dans ce cas\nVoici quelques liens qui peuvent t'être utiles "
            ),
            color=discord.Color.blue()
        )
        embed.set_footer("test")
        await message.channel.send(embed=embed)
# ----------------------------------------------------------------------------------------------------------------------------------
# --------------------------------- Nouveaux membres ( Zera )-----------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_member_join(member):
    guild = member.guild
    channel_id = 1312729327837773887
    channel = guild.get_channel(channel_id)
    if channel is None:
        print(f"Le canal avec l'ID {channel_id} n'existe pas ou est inaccessible.")
        return
    member_count = guild.member_count
    serveur = guild.name
    message = f"{member.mention}"
    await channel.send(message)
    embed = discord.Embed(title="Bienvenue sur Zera !", description=f"Grace a toi nous sommes désormais **{member_count}**!\nTu peux aller prendre tes rôles dans <#1313029571444211712>", color = discord.Color.blue())
    embed.set_image(url="https://i.imgur.com/juLvbAq.jpg")
    await channel.send(embed=embed)



# -------------------------------------------------------------------------

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Cette commande n'existe pas.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Il manque un argument.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Vous n'avez pas les permissions nécessaires.")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("Vous ne pouvez pas utiliser cette commande.")
    elif hasattr(error, "original") and isinstance(error.original, discord.Forbidden):
        await ctx.send("Je n'ai pas les permissions nécessaires pour exécuter cette commande.")
    else:
        await ctx.send(f"Une erreur inattendue s'est produite : {error}")




@bot.event
async def on_ready():
    change_status.start()
    print("-------------------------------------------------------------------------------------------------------------------")
    print("Non : ", bot.user.name)
    print("ID : ", bot.user.id)
    print('Bot prêt !\n-------------------------------------------------------------------------------------------------------')

@bot.event
async def setup_hook() -> None:
    for extension in EXTENSIONS:
        await bot.load_extension(extension)
    synced = await bot.tree.sync()
    print(f"Commandes sycrronisés : {len(synced)} !")

bot.run(Token.token)