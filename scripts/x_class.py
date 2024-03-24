import tweepy
import utils

from logger import CustomLogger

class XClass:
    def __init__(self, logger=None, credentials=None):
        """
        Initializes an instance of XClass.

        Args:
            logger (Logger, optional): Optional logger object for logging messages.
            credentials (dict, optional): Dictionary containing Twitter API credentials.
                Required keys: 'bearer_token', 'api_key', 'api_secret', 'access_token', 'access_token_secret'.
        """
        self.logger = logger or CustomLogger().get_logger()
        self.x_client = self.authenticate(credentials)

    def authenticate(self, credentials):
        """
        Authenticates and returns a Tweepy Client object for accessing the Twitter API.

        Args:
            credentials (dict): Dictionary containing Twitter API credentials.
                Required keys: 'bearer_token', 'api_key', 'api_secret', 'access_token', 'access_token_secret'.

        Returns:
            tweepy.Client: Tweepy Client object for accessing the Twitter API.
        """
        try:
            x_client = tweepy.Client(
                bearer_token=credentials.get('bearer_token'),
                consumer_key=credentials.get('api_key'),
                consumer_secret=credentials.get('api_secret'),
                access_token=credentials.get('access_token'),
                access_token_secret=credentials.get('access_token_secret')
            )
            self.logger.info(f'X has logged in.')
            return x_client
        except tweepy.TweepyException as e:
            return None

    def upload_post(self, tweet_text):
        """
        Uploads a post (tweet) using the Tweepy Client.

        Args:
            tweet_text (str): Text content of the tweet.
        """
        post = self.x_client.create_tweet(text=tweet_text)
        self.logger.info(f'UPLOAD POST: {post}')

    def process_next_post(self):
        """
        Processes the next post from x_posts.json by uploading it as a tweet and then removing it from the file.
        """
        # Read the next post from x_posts.json
        post_data = utils.get_next_post(file_path='x_posts.json', logger=self.logger)
        if post_data:
            title = post_data['title']
            # Post the tweet
            tweet_text = f'{title}'
            self.upload_post(tweet_text)

            # Remove the posted post from x_posts.json
            utils.remove_post_from_file(file_path='x_posts.json', post_data=post_data, logger=self.logger)
        else:
            self.logger.warning(f'No posts available to process.')