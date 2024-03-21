
import discord
import os

from discord_commands import handle_discord_commands
from logger import CustomLogger


class DiscordClass:
    def __init__(self):
        self.discord_token = os.getenv('DISCORD_TOKEN')
        self.LOGGER = CustomLogger().get_logger()

    def init_discord_client(self):
        intents = discord.Intents.default()
        intents.message_content = True
        self.client = discord.Client(intents=intents)

        @self.client.event
        async def on_ready():
            self.LOGGER.info(f'{self.client.user} is logged in, waiting for requests.')

        @self.client.event
        async def on_message(message):
            # Apply lower case to message
            message.content = message.content.lower()

            # Catch if bot is the messenger
            if message.author == self.client.user:
                return

            # Handle Discord commands
            await handle_discord_commands(message, self.client, self.LOGGER)

        self.client.run(self.discord_token, log_handler=None)
