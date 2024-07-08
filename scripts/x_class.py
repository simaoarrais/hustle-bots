import tweepy
import utils

from logger import CustomLogger

class XClass:
    def __init__(self, logger=None, credentials=None):
        self.logger = logger or CustomLogger().get_logger()
        self.x_client, self.x_api = self.authenticate(credentials)

    def authenticate(self, credentials):
        try:
            x_client = tweepy.Client(
                bearer_token=credentials.get('bearer_token'),
                consumer_key=credentials.get('api_key'),
                consumer_secret=credentials.get('api_secret'),
                access_token=credentials.get('access_token'),
                access_token_secret=credentials.get('access_token_secret')
            )

            auth = tweepy.OAuthHandler(consumer_key=credentials.get('api_key'), consumer_secret=credentials.get('api_secret'))
            auth.set_access_token(credentials.get('access_token'), credentials.get('access_token_secret'))
            x_api = tweepy.API(auth)

            self.logger.info(f'X has logged in.')
            return x_client, x_api
        except tweepy.TweepyException as e:
            return None

    def upload_next_post(self, tweet_text, media_id):
        post = self.x_client.create_tweet(text=tweet_text, media_ids=[media_id])
        self.logger.info(f'UPLOAD POST: {post}')