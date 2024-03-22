
import discord
import os
import utils

from logger import CustomLogger
from reddit_class import RedditClass

from discord.ext import commands
from dotenv import load_dotenv


# Load environment
load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))
logger = CustomLogger().get_logger()

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

async def send_message(channel, message):
    if await channel.send(message):
        logger.info(f'Message was sent: {message}')

# ---------------------------------------------------------------------------- #
#                                    Events                                    #
# ---------------------------------------------------------------------------- #


# --------------------------------- On Ready --------------------------------- #


@bot.event
async def on_ready():
    logger.info(f'{bot.user} is logged in.')

    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    message = f'**Hello G, we up and ready!**\n' \
                f'```For further help, type \"{bot.command_prefix}h\" to check commands.```\n'
    
    await send_message(channel, message)

# ---------------------------------------------------------------------------- #
#                                   Commands                                   #
# ---------------------------------------------------------------------------- #


# -------------------------------- Help & Test ------------------------------- #
@bot.command()
async def h(ctx):
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    message = f'**!test** - To test the bot.\n' \
                f'**Score:** {1}'
    
    await send_message(channel, message)

@bot.command()
async def test(ctx):
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    message = f'I will give you a test back!'

    await send_message(channel, message)

# ---------------------------------- Reddit ---------------------------------- #
@bot.command()
async def reddit(ctx, subreddit_name, search_limit):
    channel = bot.get_channel(DISCORD_CHANNEL_ID)

    reddit = RedditClass(logger=logger)
    subreddit = reddit.access_subreddit(subreddit_name)
    top_posts = reddit.get_top_posts(subreddit_client=subreddit, search_limit=int(search_limit))

    utils.save_json_file(data=top_posts, logger=logger)
    message = 'Reddit!'
    await send_message(channel, message)

# ----------------------------------- Give ----------------------------------- #
@bot.command()
async def give(ctx):
    channel = bot.get_channel(DISCORD_CHANNEL_ID)

    # Read the JSON data from the file
    json_data = utils.read_json_file('../output/default.json')

    # Process the post information and send a formatted message to the Discord channel
    for post in json_data:
        title = post['title']
        score = post['score']
        url = post['url']
        author = post['author']
        permalink = post['permalink']

        # Format the message
        message = f"**Title:** {title}\n" \
                            f"**Score:** {score}\n" \
                            f"**URL:** {url}\n" \
                            f"**Author:** {author}\n" \
                            f"**Permalink:** https://www.reddit.com{permalink}"

        # Send the message to the Discord channel
        await send_message(channel, message)

bot.run(DISCORD_TOKEN, log_handler=None)
