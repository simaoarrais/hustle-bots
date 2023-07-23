from dotenv import load_dotenv

import praw
import os

def access_reddit():
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
    reddit = praw.Reddit(
        username=REDDIT_USERNAME_ENV,
        password=REDDIT_USERNAME_ENV,
        client_id=CLIENT_ID_ENV,
        client_secret=CLIENT_SECRET_ENV,
        user_agent="reig"
    )
    reddit.read_only = True

    # Access a subreddit and posts
    subreddit = reddit.subreddit("NatureIsFuckingLit")
    posts = subreddit.search(query="desert", sort='new', time_filter='all', limit=1)

    # Iterate through posts
    for post in posts:
        print(post.url)

    return 0

if __name__ == "__main__":
    access_reddit()