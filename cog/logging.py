import discord
from discord.ext import commands
import os

class Logging(commands.Cog):
    """A cog for logging command usage."""

    def __init__(self, bot: commands.Bot):
        """Initializes the Logging cog."""
        self.bot = bot
        self.log_channel_id = int(os.getenv("LOG_CHANNEL_ID"))
        self.log_server_id = int(os.getenv("LOG_SERVER_ID"))

    @commands.Cog.listener()
    async def on_ready(self):
        """Called when the cog is ready."""
        print("Cog loaded: Logging")

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        """Logs application command usage to a specific channel."""
        if interaction.type != discord.InteractionType.application_command:
            return

        command_name = interaction.data.get('name')
        author = interaction.user
        channel = interaction.channel
        guild = interaction.guild
        options = interaction.data.get('options', [])

        log_embed = discord.Embed(
            title=f"Command '{command_name}' executed",
            color=0x00ff00
        )
        log_embed.add_field(name="Author", value=author.mention, inline=True)
        log_embed.add_field(name="Channel", value=channel.mention, inline=True)
        log_embed.add_field(name="Server", value=guild.name, inline=True)

        for option in options:
            log_embed.add_field(name=f"Option: {option.get('name')}", value=option.get('value'), inline=False)

        try:
            message = await interaction.original_response()
            if message:
                log_embed.add_field(name="Message Link", value=message.jump_url, inline=False)
        except discord.NotFound:
            pass  # Interaction might not have a visible response

        log_channel = self.bot.get_channel(self.log_channel_id)
        if log_channel and guild.id == self.log_server_id:
            await log_channel.send(embed=log_embed)


async def setup(bot: commands.Bot):
    """Sets up the Logging cog."""
    await bot.add_cog(Logging(bot))