
import discord
import os
import utils
import asyncio

from logger import CustomLogger
from reddit_class import RedditClass
from x_class import XClass
from instagram_class import InstagramClass

from discord.ext import commands
from dotenv import load_dotenv

# Create log and output folders
output_folder_dir, logs_output_dir = utils.create_output_folders()
logger = CustomLogger().get_logger()

# Load Discord requisites
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# ---------------------------------------------------------------------------- #
#                                Check Functions                               #
# ---------------------------------------------------------------------------- #
async def post_check(ctx, post_url):
    content = f'**URL:** {post_url}\n' \
        f'```Do you want to upload this post?\n' \
        f'Agree: ✅\n' \
        f'Cancel: ❌```'
    message = await ctx.send(content)
    logger.info(f'Message was sent: {message}')

    # Pre-add reactions
    await message.add_reaction('✅')
    await message.add_reaction('❌')

    def check(reaction, user):
        return user != message.author and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '❌')

    # Check for reaction
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=20.0, check=check)
    except asyncio.TimeoutError:
        message = await ctx.send('❌ Action Canceled - Timeout.')
        logger.warning('TimeoutError')
        return False

    # On correct reaction
    else:
        if str(reaction.emoji) == '❌':
            message = await ctx.send('❌ Action Canceled.')
            logger.info(f'Message was sent: {message}')
            return False
    
    return True

# ---------------------------------------------------------------------------- #
#                                    Events                                    #
# ---------------------------------------------------------------------------- #

@bot.event
async def on_connect():
    logger.info(f'{bot.user} is logged in.')

@bot.event
async def on_ready():
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    content = f'**Hello G, we up and ready!**\n' \
                f'```For further help, type \"{bot.command_prefix}h\" to check commands.```\n'
    
    message = await channel.send(content=content, delete_after=10)
    if message:
        logger.info(f'Message was sent: {message}')

# ---------------------------------------------------------------------------- #
#                                   Commands                                   #
# ---------------------------------------------------------------------------- #


# ----------------------------------- Help ----------------------------------- #
@bot.command()
async def h(ctx):
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    content = f'**!test** - To test the bot.\n' \
                f'**Score:** {1}'

    if await channel.send(content, delete_after=10):
        logger.info(f'Message was sent: {content}')

# ---------------------------------- Reddit ---------------------------------- #
@bot.command()
async def reddit(ctx, subreddit_name, search_limit):
    credentials = {
                'username': os.getenv('REDDIT_USERNAME'),
                'password': os.getenv('REDDIT_PASSWORD'),
                'client_id': os.getenv('REDDIT_CLIENT_ID'),
                'client_secret': os.getenv('REDDIT_CLIENT_SECRET')
            }
    reddit_client = RedditClass(logger=logger, credentials=credentials)

    subreddit = reddit_client.access_subreddit(subreddit_name)
    top_post = reddit_client.get_top_posts(subreddit_client=subreddit, search_limit=int(search_limit))
    
# ------------------------------------- X ------------------------------------ #
@bot.command()
async def x(ctx):
    credentials = {
        'bearer_token': os.getenv('X_BEARER_TOKEN'),
        'api_key': os.getenv('X_API_KEY'),
        'api_secret': os.getenv('X_API_SECRET'),
        'access_token': os.getenv('X_ACCESS_TOKEN'),
        'access_token_secret': os.getenv('X_ACCESS_TOKEN_SECRET')
    }
    x_client = XClass(logger=logger, credentials=credentials)
    x_client.process_next_post()
    content = f'I will give you a test back!'
    message = await ctx.send(content)
    logger.info(f'Message was sent: {message}')

# ----------------------------------- Insta ---------------------------------- #
@bot.command()
async def instagram(ctx):
    credentials = {
        'username': os.getenv('INSTA_USERNAME'),
        'password': os.getenv('INSTA_PASSWORD')
    }
    instagram_client = InstagramClass(logger=logger, credentials=credentials)
    instagram_client.process_next_post()
    content = f'I will give you a test back!'
    message = await ctx.send(content)
    logger.info(f'Message was sent: {message}')

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
        if await channel.send(message):
            logger.info(f'Message was sent: {message}')

bot.run(DISCORD_TOKEN, log_handler=None)