from dotenv import load_dotenv

import logging
import praw
import os

def init_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    logging.info(f"Logger created.")

def access_reddit(read_only=True):
    # Load environment variables from .env file
    load_dotenv()

    # Access environment variables
    REDDIT_USERNAME_ENV = os.getenv("REDDIT_USERNAME")
    REDDIT_PASSWORD_ENV = os.getenv("REDDIT_PASSWORD")
    CLIENT_ID_ENV = os.getenv("CLIENT_ID")
    CLIENT_SECRET_ENV = os.getenv("CLIENT_SECRET")

    # print(f"username: {CLIENT_SECRET_ENV}\
    #       \npassword: {REDDIT_PASSWORD_ENV}\
    #       \nclient_id: {CLIENT_ID_ENV}\
    #       \nclient_secret: {CLIENT_SECRET_ENV}")
    
    # Access Reddit API
    try:
        reddit = praw.Reddit(
            username=REDDIT_USERNAME_ENV,
            password=REDDIT_PASSWORD_ENV,
            client_id=CLIENT_ID_ENV,
            client_secret=CLIENT_SECRET_ENV,
            user_agent="reig"
        )
        reddit.read_only = read_only
        logging.info("Reddit API connection successful.")
        return reddit
    
    except Exception as e:
        logging.error(f"Error connecting to Reddit API: {e}")
        return None

def access_subreddit(reddit, subreddit="NatureIsFuckingLit"):
    # Access a subreddit
    logging.info(f"Accessing subreddit: {subreddit}")
    return reddit.subreddit(subreddit)

def get_posts(subreddit):
    posts = subreddit.search(query="desert", sort='new', time_filter='all', limit=1)

    # Iterate through posts
    for post in posts:
        print(post.url)

if __name__ == "__main__":
    # Init Logget
    init_logger()

    # Access Reddit API
    reddit = access_reddit()
    if not reddit:
        logging.error("Reddit API connection failed. Exiting.")
        exit(1)

    # Access subreddit
    subreddit = access_subreddit(reddit)

    # Get posts
    get_posts(subreddit)

    # Successful exiting
    exit(0)