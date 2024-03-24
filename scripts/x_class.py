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
        self.x_client = self.access_x(credentials)

    def access_x(self, credentials):
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
        post_data = self.get_next_post()
        if post_data:
            # Post the tweet
            tweet_text = f"{post_data['title']} {post_data['url']}"
            self.upload_post(tweet_text)

            # Remove the posted post from x_posts.json
            self.remove_post_from_file(post_data)
        else:
            self.logger.warning(f'No posts available to process.')

    def get_next_post(self):
        """
        Reads the next post from x_posts.json and returns it.

        Returns:
            dict: Dictionary representing the next post data.
        """
        # Read x_posts.json and get the next post
        if utils.check_file_exists_output('x_posts.json'):
            post_data = utils.read_json_file('x_posts.json')
            if isinstance(post_data, list) and len(post_data) > 0:
                self.logger.info(f'Fetch new post from x_posts.json')
                return post_data[0]  # Assuming the posts are stored as a list of dictionaries
        return None

    def remove_post_from_file(self, post_data):
        """
        Removes the posted post from x_posts.json.

        Args:
            post_data (dict): Dictionary representing the post data to be removed.
        """
        # Remove the posted post from x_posts.json
        if utils.check_file_exists_output('x_posts.json'):
            posts = utils.read_json_file('x_posts.json')
            updated_posts = [post for post in posts if post != post_data]
            utils.save_json_file(logger=self.logger, file_path='x_posts.json', data=updated_posts, overwrite=True)
            self.logger.info(f'Removed posted post from x_posts.json.')