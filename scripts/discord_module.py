from dotenv import load_dotenv

import discord
import json
import os
import utils

if __name__ == "__main__":

    # Load environment variables from .env file
    load_dotenv()

    # Access environment variables required for Discord authentication
    TOKEN = os.getenv('DISCORD_TOKEN')

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)



    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')

    @client.event
    async def on_message(message):

        if message.author == client.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')

        elif message.content.startswith('$post_info'):
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

    client.run(TOKEN)