from logger import CustomLogger
import praw
import os


class RedditClass:
    def __init__(self, read_only=True, logger=CustomLogger()):
        self.read_only = read_only
        self.LOGGER = logger.get_logger()
        self.reddit = self.access_reddit(
            os.getenv('REDDIT_USERNAME'), 
            os.getenv('REDDIT_PASSWORD'), 
            os.getenv('REDDIT_CLIENT_ID'), 
            os.getenv('REDDIT_CLIENT_SECRET')
        )

    def access_reddit(self, reddit_username, reddit_password, client_id, client_secret):

        # Access Reddit API with the provided credentials
        try:
            reddit = praw.Reddit(
                username=reddit_username,
                password=reddit_password,
                client_id=client_id,
                client_secret=client_secret,
                user_agent="RedXIg"
            )
            reddit.read_only = self.read_only
            self.LOGGER.info("Reddit API connected.")  # Log a message when the connection is successful
            return reddit
        except Exception as e:
            self.LOGGER.error("Reddit API connection failed. Exiting.")  # Log an error message if the Reddit API connection fails
            return None

    def access_subreddit(self, subreddit="NatureIsFuckingLit"):
        # Access a specific subreddit using the provided Reddit instance
        self.LOGGER.info("Accessing subreddit: %s", subreddit)  # Log a message to indicate which subreddit is being accessed
        return self.reddit.subreddit(subreddit)

    def get_top_posts(self, subreddit, threshold=1000, n_posts=5, search_limit=15):
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
                self.LOGGER.info("Post URL: %s | Score: %d", post.url, post.score)  # Log the URL and score of each valid post
        
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
