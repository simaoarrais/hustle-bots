import praw
from prawcore import NotFound, Forbidden
from pymongo import MongoClient
from logger import CustomLogger

class RedditClass:
    """Class for interacting with the Reddit API."""

    def __init__(self, read_only=True, logger=None, credentials=None):
        self.read_only = read_only
        self.logger = logger or CustomLogger().get_logger()
        self.reddit = self.access_reddit(credentials)

    def access_reddit(self, credentials):
        try:
            reddit = praw.Reddit(
                username=credentials.get('username'),
                password=credentials.get('password'),
                client_id=credentials.get('client_id'),
                client_secret=credentials.get('client_secret'),
                user_agent="RedXIg"
            )
            reddit.read_only = self.read_only
            self.logger.info("Reddit API connected.")
            return reddit
        except praw.exceptions.APIException as e:
            self.logger.error(f"Reddit API connection failed: {e}")
            return None

    def access_subreddit(self, subreddit_name=None):
        subreddit_client = self.reddit.subreddit(subreddit_name)
        if subreddit_client.id:
            return subreddit_client
            
    def get_top_posts(self, subreddit_client, search_limit=10):
        top_posts = subreddit_client.top(time_filter='week', limit=search_limit)

        posts_list = []
        for post in top_posts:
            post_data = {
                'id': post.id,
                'title': post.title,
                'score': post.score,
                'url': post.url,
                'author': post.author.name,
                'created_utc': post.created_utc,
                'is_video': post.is_video,
                'permalink': post.permalink,
                'num_comments': post.num_comments,
                'thumbnail': post.thumbnail
            }
            posts_list.append(post_data)
            self.logger.info("Post URL: %s | Score: %d", post.url, post.score)
        
        


        return posts_list