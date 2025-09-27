import discord
from discord.ext import commands
from discord import app_commands

class TestCounter(commands.Cog):
    """A cog that implements a simple counting game in a specific channel.

    This version of the counter uses separate text files to store the
    last number and the last user.
    """

    def __init__(self, bot: commands.Bot):
        """Initializes the TestCounter cog.

        Args:
            bot (commands.Bot): The bot instance.
        """
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Called when the cog is ready."""
        print("Cog loaded : test_counter")

    def get_last_number(self) -> int:
        """Gets the last counted number from 'compteur.txt'.

        Returns:
            int: The last number, or 0 if the file doesn't exist or is empty.
        """
        try:
            with open('compteur.txt', 'r') as f:
                content = f.read()
                if content == '':
                    return 0
                return int(content)
        except FileNotFoundError:
            return 0

    def set_last_number(self, number: int):
        """Saves the last counted number to 'compteur.txt'.

        Args:
            number (int): The number to save.
        """
        with open('compteur.txt', 'w') as f:
            f.write(str(number))

    def get_last_user(self) -> int | None:
        """Gets the ID of the last user who counted from 'dernier_utilisateur.txt'.

        Returns:
            int | None: The user ID, or None if the file doesn't exist.
        """
        try:
            with open('dernier_utilisateur.txt', 'r') as f:
                return int(f.read())
        except (FileNotFoundError, ValueError):
            return None

    def set_last_user(self, user_id: int):
        """Saves the ID of the last user who counted to 'dernier_utilisateur.txt'.

        Args:
            user_id (int): The user ID to save.
        """
        with open('dernier_utilisateur.txt', 'w') as f:
            f.write(str(user_id))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Handles the counting logic when a message is sent in the designated channel.

        Args:
            message (discord.Message): The message that was sent.
        """
        # Note: The channel ID is hardcoded here.
        if message.channel.id == 1267467304623407167:
            if not message.author.bot:
                content = message.content
                if content.isdigit():
                    number = int(content)
                    last_number = self.get_last_number()
                    last_user = self.get_last_user()

                    if number == last_number + 1 and message.author.id != last_user:
                        self.set_last_number(number)
                        self.set_last_user(message.author.id)
                        await message.add_reaction('✅')
                    else:
                        await message.delete()
                else:
                    await message.delete()

async def setup(bot: commands.Bot):
    """Sets up the TestCounter cog.

    Args:
        bot (commands.Bot): The bot instance.
    """
    await bot.add_cog(TestCounter(bot))