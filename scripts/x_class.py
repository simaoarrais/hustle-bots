import tweepy
import db_utils
import utils
from logger import CustomLogger

class XClass:
    def __init__(self, logger=None, credentials=None, db_credentials=None):
        self.logger = logger or CustomLogger().get_logger()
        self.x_client, self.x_api = self.authenticate(credentials)
        self.db = self.authenticate_db(db_credentials)

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
            x_api = tweepy.API(auth, wait_on_rate_limit=True)

            self.logger.info(f'X has logged in.')
            return x_client, x_api
        except tweepy.TweepyException as e:
            return None

    def authenticate_db(self, db_credentials):
        host = db_credentials.get('host')
        port = db_credentials.get('port')
        db_name = db_credentials.get('db_name')
        return db_utils.get_db(host, port, db_name)

    def upload_next_post(self):
        collection = self.db['posts']
        post = db_utils.get_next_post_x(collection)

        try:
            
            title = utils.standardize_title(post['title'])
            if post['is_video']:
                media_path = utils.download_video(post)
                print(media_path)
                media = self.x_api.media_upload(media_path, chunked=True, media_category="tweet_video")
            else:
                media_path = utils.download_photo(post)
                media = self.x_api.media_upload(media_path)

            print(media)
            
            tweet = self.x_api.update_status(status=title, media_ids=[media.media_id_string])
            self.logger.info(f'UPLOAD POST: {tweet}')

        except Exception as e:
            self.logger.error(f'Error uploading post: {e}')