import logging
import praw
import json
import os
import utils

from dotenv import load_dotenv

def init_logger():
    # Initialize the logger with INFO log level and a specific log message format
    logging.basicConfig(
        level=logging.INFO,
        format="[%(filename)s] %(asctime)s [%(levelname)s] %(message)s",
    )
    logging.info("Logger created.")  # Log a message to indicate that the logger is created

def access_reddit(read_only=True):
    # Load environment variables from .env file
    load_dotenv()

    # Access environment variables required for Reddit API authentication
    REDDIT_USERNAME_ENV = os.getenv("REDDIT_USERNAME")
    REDDIT_PASSWORD_ENV = os.getenv("REDDIT_REDDIT_PASSWORD")
    CLIENT_ID_ENV = os.getenv("REDDIT_CLIENT_ID")
    CLIENT_SECRET_ENV = os.getenv("REDDIT_CLIENT_SECRET")

    # Access Reddit API with the provided credentials
    try:
        reddit = praw.Reddit(
            username=REDDIT_USERNAME_ENV,
            password=REDDIT_PASSWORD_ENV,
            client_id=CLIENT_ID_ENV,
            client_secret=CLIENT_SECRET_ENV,
            user_agent="RedXIg"
        )
        reddit.read_only = read_only
        logging.info("Reddit API connection successful.")  # Log a message when the connection is successful
        return reddit
    
    except Exception as e:
        logging.error("Reddit API connection failed. Exiting.")  # Log an error message if the Reddit API connection fails
        return None

def access_subreddit(reddit, subreddit="NatureIsFuckingLit"):
    # Access a specific subreddit using the provided Reddit instance
    logging.info("Accessing subreddit: %s", subreddit)  # Log a message to indicate which subreddit is being accessed
    return reddit.subreddit(subreddit)

def get_top_posts(subreddit, threshold=1000, n_posts=5, search_limit=15):
    # Fetch the top posts from the subreddit based on the specified threshold and number of posts
    top_posts = subreddit.top(time_filter='all', limit=search_limit)

    top_posts_above_threshold = []

    for post in top_posts:
        if len(top_posts_above_threshold) >= n_posts:
            print("exit")
            break  # Stop iterating when the desired number of posts is reached

        if post.score > threshold and not post.is_video:
            # Check if the post's score is above the threshold and if it is not a video
            top_posts_above_threshold.append(post)
            logging.info("Post URL: %s | Score: %d", post.url, post.score)  # Log the URL and score of each valid post
    
    posts_data = []
    for post in top_posts_above_threshold:
        post_data = {
            "title": post.title,
            "score": post.score,
            "url": post.url,
            "author": post.author.name,
            "created_utc": post.created_utc,
            "is_video": post.is_video,
            "permalink": post.permalink,
            "num_comments": post.num_comments,
            "thumbnail": post.thumbnail
        }
        posts_data.append(post_data)

    return posts_data