from dotenv import load_dotenv
import logging
import praw
import os

def init_logger():
    # Initialize the logger with INFO log level and a specific log message format
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    logging.info(f"Logger created.")  # Log a message to indicate that the logger is created

def access_reddit(read_only=True):
    # Load environment variables from .env file
    load_dotenv()

    # Access environment variables required for Reddit API authentication
    REDDIT_USERNAME_ENV = os.getenv("REDDIT_USERNAME")
    REDDIT_PASSWORD_ENV = os.getenv("REDDIT_PASSWORD")
    CLIENT_ID_ENV = os.getenv("CLIENT_ID")
    CLIENT_SECRET_ENV = os.getenv("CLIENT_SECRET")

    # Access Reddit API with the provided credentials
    try:
        reddit = praw.Reddit(
            username=REDDIT_USERNAME_ENV,
            password=REDDIT_PASSWORD_ENV,
            client_id=CLIENT_ID_ENV,
            client_secret=CLIENT_SECRET_ENV,
            user_agent="reig"
        )
        reddit.read_only = read_only
        logging.info("Reddit API connection successful.")  # Log a message when the connection is successful
        return reddit
    
    except Exception as e:
        logging.error("Error connecting to Reddit API: %s", e)  # Log an error message with the specific exception
        return None

def access_subreddit(reddit, subreddit="NatureIsFuckingLit"):
    # Access a specific subreddit using the provided Reddit instance
    logging.info("Accessing subreddit: %s", subreddit)  # Log a message to indicate which subreddit is being accessed
    return reddit.subreddit(subreddit)

def get_top_posts(subreddit, threshold=1000, n_posts=5, search_limit=15):
    # Fetch the top posts from the subreddit based on the specified threshold and number of posts
    posts = subreddit.top(time_filter='all', limit=search_limit)

    top_posts_above_threshold = []

    for post in posts:
        if len(top_posts_above_threshold) >= n_posts:
            break  # Stop iterating when the desired number of posts is reached

        if post.score > threshold and not post.is_video:
            # Check if the post's score is above the threshold and if it is not a video
            top_posts_above_threshold.append(post)
            logging.info("Post URL: %s | Score: %d", post.url, post.score)  # Log the URL and score of each valid post

    return top_posts_above_threshold

if __name__ == "__main__":
    # Initialize the logger
    init_logger()

    # Access Reddit API
    reddit = access_reddit()
    if not reddit:
        logging.error("Reddit API connection failed. Exiting.")  # Log an error message if the Reddit API connection fails
        exit(1)

    # Access subreddit
    subreddit = access_subreddit(reddit)

    # Get posts
    get_top_posts(subreddit)

    # Successful exiting
    exit(0)  # Log an INFO message to indicate successful exiting of the program