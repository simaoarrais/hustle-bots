import praw
from prawcore import NotFound, Forbidden

import db_utils
from logger import CustomLogger

class RedditClass:
    """Class for interacting with the Reddit API."""

    def __init__(self, logger=None, credentials=None, db_credentials=None):
        self.logger = logger or CustomLogger().get_logger()
        self.reddit = self.access_reddit(credentials)
        self.db = self.access_db(db_credentials)

    def access_db(self, db_credentials):
        host = db_credentials.get('host')
        port = db_credentials.get('port')
        db_name = db_credentials.get('db_name')
        return db_utils.get_db(host, port, db_name)
    
    def access_reddit(self, credentials):
        try:
            reddit = praw.Reddit(
                username=credentials.get('username'),
                password=credentials.get('password'),
                client_id=credentials.get('client_id'),
                client_secret=credentials.get('client_secret'),
                user_agent="RedXIg"
            )
            reddit.read_only = True
            self.logger.info("Reddit API connected.")
            return reddit
        except praw.exceptions.APIException as e:
            self.logger.error(f"Reddit API connection failed: {e}")
            return None

    def access_subreddit(self, subreddit_name=None):
        subreddit_client = self.reddit.subreddit(subreddit_name)
        if subreddit_client.id:
            return subreddit_client
            
    def save_top_posts(self, subreddit_client, time_filter='week', search_limit=10):
        top_posts = subreddit_client.top(time_filter=time_filter, limit=search_limit)

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
            self.logger.info("Post URL: %s | Score: %d", post.url, post.score)

            collection = self.db['posts']
            if db_utils.insert_document(collection, post_data):
                posts_list.append(post_data)
    
        return posts_list