
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
logger = CustomLogger().get_logger()
output_folder_dir, logs_output_dir = utils.create_output_folders()

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
        reaction, user = await bot.wait_for('reaction_add', timeout=60, check=check)
    except asyncio.TimeoutError:
        message = await ctx.send('❌ Action Canceled - Timeout.')
        logger.warning('TimeoutError')
        return None

    # On correct reaction
    else:
        if str(reaction.emoji) == '❌':
            message = await ctx.send('❌ Action Canceled.')
            logger.info(f'Message was sent: {message}')
            return False

    logger.info(f'POST ACCEPTED: {post_url}')
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
    
    db_credentials = {
                'host': os.getenv('DB_HOST'),
                'port': os.getenv('DB_PORT'),
                'db_name': os.getenv('DB_NAME')
            } 
    
    reddit_client = RedditClass(logger, credentials, db_credentials)
    subreddit = reddit_client.access_subreddit(subreddit_name)
    time_filter = 'week'
    top_posts = reddit_client.save_top_posts(subreddit, time_filter, int(search_limit))
    
# ------------------------------------- X ------------------------------------ #
@bot.command()
async def x(ctx):
    x = None

    credentials = {
        'bearer_token': os.getenv('X_BEARER_TOKEN'),
        'api_key': os.getenv('X_API_KEY'),
        'api_secret': os.getenv('X_API_SECRET'),
        'access_token': os.getenv('X_ACCESS_TOKEN'),
        'access_token_secret': os.getenv('X_ACCESS_TOKEN_SECRET')
    }

    db_credentials = {
                'host': os.getenv('DB_HOST'),
                'port': os.getenv('DB_PORT'),
                'db_name': os.getenv('DB_NAME')
            }
    
    if not x:
        x = XClass(logger, credentials, db_credentials)
    x.upload_next_post()

# ----------------------------------- Insta ---------------------------------- #
@bot.command()
async def instagram(ctx):
    instagram = None
    
    credentials = {
        'username': os.getenv('INSTA_USERNAME'),
        'password': os.getenv('INSTA_PASSWORD')
    }

    db_credentials = {
                'host': os.getenv('DB_HOST'),
                'port': os.getenv('DB_PORT'),
                'db_name': os.getenv('DB_NAME')
            }
    
    if not instagram:
        instagram = InstagramClass(logger, credentials, db_credentials)
    
    post = instagram.get_next_post()
    
    check = await post_check(ctx, post['url'])
    if check:
        instagram.upload_post(post)
        message = await ctx.send(f'Posted ✅')
        logger.info(f'Message was sent: {message}')
    elif check is False:
        instagram.reject_post(post)

bot.run(DISCORD_TOKEN, log_handler=None)