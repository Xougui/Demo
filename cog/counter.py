import discord
from discord.ext import commands
from discord import app_commands
import json
import os

COUNTER_FILE = "data/counter.json"

def load_counter_data():
    """Loads counter data from the JSON file.

    Returns:
        dict: A dictionary containing counter data for each guild.
    """
    if os.path.exists(COUNTER_FILE):
        try:
            with open(COUNTER_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}  # Return empty dict if JSON is corrupted
    return {}

def save_counter_data(data):
    """Saves counter data to the JSON file.

    Args:
        data (dict): The counter data to save.
    """
    with open(COUNTER_FILE, 'w') as f:
        json.dump(data, f, indent=4)

class Counter(commands.Cog):
    """A cog for managing a counting channel in a guild."""
    def __init__(self, bot: commands.Bot):
        """Initializes the Counter cog.

        Args:
            bot (commands.Bot): The bot instance.
        """
        self.bot = bot
        self.guild_counters = load_counter_data()

    @commands.Cog.listener()
    async def on_ready(self):
        """Called when the cog is ready."""
        print("Cog loaded: Counter")

    @app_commands.command(name="counter", description="Sets the channel for the counting game.")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_counter_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """Sets the channel for counting.

        This command requires administrator permissions.

        Args:
            interaction (discord.Interaction): The interaction object.
            channel (discord.TextChannel): The text channel to be used for counting.
        """
        guild_id = str(interaction.guild.id)

        if guild_id not in self.guild_counters:
            self.guild_counters[guild_id] = {"last_number": 0, "last_user_id": None}

        self.guild_counters[guild_id]['counter_channel_id'] = channel.id
        save_counter_data(self.guild_counters)

        embed_counter = discord.Embed(
            title="Counter Channel Set",
            description=f"The counting channel has been set to {channel.mention}.\nStart by sending the number `1`!",
            color=discord.Color.green()
        )

        await channel.send(embed=embed_counter)
        await interaction.response.send_message(
            f"The counter has been set up in {channel.mention}. You can start counting now!", ephemeral=True
        )

    def get_counter_channel(self, guild_id: int) -> int | None:
        """Gets the counting channel ID for a guild.

        Args:
            guild_id (int): The ID of the guild.

        Returns:
            int | None: The channel ID, or None if not set.
        """
        guild_data = self.guild_counters.get(str(guild_id))
        if guild_data:
            return guild_data.get('counter_channel_id')
        return None

    def get_last_number(self, guild_id: int) -> int:
        """Gets the last number counted in a guild.

        Args:
            guild_id (int): The ID of the guild.

        Returns:
            int: The last number counted.
        """
        guild_data = self.guild_counters.get(str(guild_id))
        if guild_data:
            return guild_data.get('last_number', 0)
        return 0

    def get_last_user(self, guild_id: int) -> int | None:
        """Gets the last user who counted in a guild.

        Args:
            guild_id (int): The ID of the guild.

        Returns:
            int | None: The user ID, or None if not set.
        """
        guild_data = self.guild_counters.get(str(guild_id))
        if guild_data:
            return guild_data.get('last_user_id')
        return None

    def set_last_number(self, guild_id: int, number: int):
        """Sets the last number counted in a guild.

        Args:
            guild_id (int): The ID of the guild.
            number (int): The number to set.
        """
        if str(guild_id) in self.guild_counters:
            self.guild_counters[str(guild_id)]['last_number'] = number
            save_counter_data(self.guild_counters)

    def set_last_user(self, guild_id: int, user_id: int):
        """Sets the last user who counted in a guild.

        Args:
            guild_id (int): The ID of the guild.
            user_id (int): The user ID to set.
        """
        if str(guild_id) in self.guild_counters:
            self.guild_counters[str(guild_id)]['last_user_id'] = user_id
            save_counter_data(self.guild_counters)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Handles the counting logic in the designated channel.

        Args:
            message (discord.Message): The message object.
        """
        if message.author.bot or not message.guild:
            return

        counter_channel_id = self.get_counter_channel(message.guild.id)
        if not counter_channel_id or message.channel.id != counter_channel_id:
            return

        content = message.content
        if content.isdigit():
            number = int(content)
            last_number = self.get_last_number(message.guild.id)
            last_user = self.get_last_user(message.guild.id)

            if number == last_number + 1 and message.author.id != last_user:
                self.set_last_number(message.guild.id, number)
                self.set_last_user(message.guild.id, message.author.id)
                await message.add_reaction('✅')
            else:
                await message.delete()
        else:
            await message.delete()

async def setup(bot: commands.Bot):
    """Sets up the Counter cog.

    Args:
        bot (commands.Bot): The bot instance.
    """
    await bot.add_cog(Counter(bot))