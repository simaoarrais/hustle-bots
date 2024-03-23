import praw

from logger import CustomLogger

class RedditClass:
    """Class for interacting with the Reddit API."""

    def __init__(self, read_only=True, logger=None, credentials=None):
        """
        Initialize the RedditClass.

        Args:
            read_only (bool): Whether to operate in read-only mode (default is True).
            logger (Logger): Optional logger object for logging messages.
            credentials (dict): Dictionary containing Reddit API credentials.
                Should include keys 'username', 'password', 'client_id', 'client_secret'.

        """
        self.read_only = read_only
        self.logger = logger or CustomLogger().get_logger()
        self.reddit = self.access_reddit(credentials)

    def access_reddit(self, credentials):
        """
        Access Reddit API with provided credentials.

        Args:
            credentials (dict): Dictionary containing Reddit API credentials.

        Returns:
            praw.Reddit: Initialized Reddit API instance or None if connection fails.

        """
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
        """
        Access a specific subreddit using the provided Reddit instance.

        Args:
            subreddit_name (str): Name of the subreddit to access (default is None).

        Returns:
            praw.models.Subreddit: Subreddit object corresponding to the provided name.

        """
        subreddit_name = subreddit_name or "NatureIsFuckingLit"
        self.logger.info("Accessing subreddit: %s", subreddit_name)
        return self.reddit.subreddit(subreddit_name)

    def get_top_posts(self, subreddit_client, threshold=1000, search_limit=15):
        """
        Get top posts from a subreddit based on specified criteria.

        Args:
            subreddit_client (praw.models.Subreddit): Subreddit object to fetch posts from.
            threshold (int): Minimum score threshold for posts to be considered (default is 1000).
            search_limit (int): Maximum number of posts to search (default is 15).

        Returns:
            list: List of dictionaries containing data for top posts.

        """
        top_posts = subreddit_client.top(time_filter='all', limit=search_limit)

        top_posts_above_threshold = []
        for post in top_posts:
            if post.score > threshold and not post.is_video:
                top_posts_above_threshold.append(post)
                self.logger.info("Post URL: %s | Score: %d", post.url, post.score)

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