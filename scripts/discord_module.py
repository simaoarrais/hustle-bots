import discord
import os
import utils

from dotenv import load_dotenv
from logger import init_logger

# Load environment
env_path = '../.env'
load_dotenv(env_path)

# Discord
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Instagram
INSTA_USERNAME = os.getenv('INSTA_USERNAME')
INSTA_PASSWORD = os.getenv('INSTA_PASSWORD')

# Reddit
REDDIT_USERNAME = os.getenv('REDDIT_USERNAME')
REDDIT_PASSWORD = os.getenv('REDDIT_PASSWORD')
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')

# X
X_BEARER_TOKEN = os.getenv('X_BEARER_TOKEN')
X_API_KEY = os.getenv('X_API_KEY')
X_API_SECRET = os.getenv('X_API_SECRET')
X_ACCESS_TOKEN = os.getenv('X_ACCESS_TOKEN')
X_ACCESS_TOKEN_SECRET = os.getenv('X_ACCESS_TOKEN_SECRET')
X_CLIENT_ID = os.getenv('X_CLIENT_ID')
X_CLIENT_SECRET = os.getenv('X_CLIENT_SECRET')

# LOGGER
global LOGGER 
global console_handler

# Initialize Discord client
def init_discord_client(DISCORD_TOKEN):
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        LOGGER.info(f'{client.user} is logged in.')

    @client.event
    async def on_message(message):
        # Apply lower case to message
        message.content = message.content.lower()

        # Catch if bot is the messenger
        if message.author == client.user:
            return

        ## Check for channel
        if message.channel.name == 'redxig':

            ## Simple hello 
            if message.content.startswith('hello'):
                await message.channel.send('Hello!')

            ## Init Reddit
            if message.content.startswith('init reddit'):
                await message.channel.send('Reddit!')

            elif message.content.startswith('give'):
                # Read the JSON data from the file
                json_data = utils.read_json_file('test.json')

                # Process the post information and send a formatted message to the Discord channel
                for post in json_data:
                    title = post['title']
                    score = post['score']
                    url = post['url']
                    author = post['author']
                    permalink = post['permalink']

                    # Format the message
                    post_info_message = f"**Title:** {title}\n" \
                                        f"**Score:** {score}\n" \
                                        f"**URL:** {url}\n" \
                                        f"**Author:** {author}\n" \
                                        f"**Permalink:** https://www.reddit.com{permalink}"

                    # Send the message to the Discord channel
                    await message.channel.send(post_info_message)

    client.run(DISCORD_TOKEN, log_handler=None)


if __name__ == "__main__":
    # Init logger
    LOGGER = init_logger()

    # Init Discord client
    init_discord_client(DISCORD_TOKEN)


