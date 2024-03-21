import discord
import os
from dotenv import load_dotenv
from logger import CustomLogger
import utils
from reddit_module import RedditClass

class DiscordClass:
    def __init__(self):
        self.discord_token = os.getenv('DISCORD_TOKEN')
        self.logger = CustomLogger().get_logger()

    def init_discord_client(self):
        intents = discord.Intents.default()
        intents.message_content = True
        self.client = discord.Client(intents=intents)

        @self.client.event
        async def on_ready():
            self.logger.info(f'{self.client.user} is logged in, waiting for requests.')

        @self.client.event
        async def on_message(message):
            # Apply lower case to message
            message.content = message.content.lower()

            # Catch if bot is the messenger
            if message.author == self.client.user:
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

        self.client.run(self.discord_token, log_handler=None)

if __name__ == "__main__":
    # Load environment
    env_path = '../.env'
    load_dotenv(env_path)

    # Initialize Discord bot
    discord_bot = DiscordClass()
    discord_bot.init_discord_client()
