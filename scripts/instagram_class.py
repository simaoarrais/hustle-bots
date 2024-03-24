import os
import utils

from dotenv import load_dotenv
from logger import CustomLogger
from instagrapi import Client

class InstagramClass:
    def __init__(self, logger=None, credentials=None):
        self.logger = logger or CustomLogger().get_logger()
        self.instagram_client = self.access_instagram(credentials)

    def access_instagram(self, credentials):
        try:
            instagram_client = Client()
            instagram_client.login(credentials.get('username'), credentials.get('password'))
            self.logger.info(f'Instagram has logged in.')
            return instagram_client
        except instagrapi.exceptions as e:
            return None


    def upload_post(self):
        post = self.instagram_client.photo_upload(path='/home/simao/Desktop/hustle-bots/media/Nature.png', caption='Teste')
        self.logger.info(f'UPLOAD POST: {post}')
    
    def process_next_post(self):
        # Read the next post from x_posts.json
        post_data = self.get_next_post()
        if post_data:
            # Post the tweet
            tweet_text = f"{post_data['title']} {post_data['url']}"
            self.upload_post()

            # Remove the posted post from x_posts.json
            self.remove_post_from_file(post_data)
        else:
            self.logger.warning(f'No posts available to process.')
        
    def get_next_post(self):
        # Read x_posts.json and get the next post
        if utils.check_file_exists_output('instagram_posts.json'):
            post_data = utils.read_json_file('instagram_posts.json')
            if isinstance(post_data, list) and len(post_data) > 0:
                self.logger.info(f'Fetch new post from instagram_posts.json')
                return post_data[0]  # Assuming the posts are stored as a list of dictionaries
        return None

    def remove_post_from_file(self, post_data):
        # Remove the posted post from x_posts.json
        if utils.check_file_exists_output('instagram_posts.json'):
            posts = utils.read_json_file('instagram_posts.json')
            updated_posts = [post for post in posts if post != post_data]
            utils.save_json_file(logger=self.logger, file_path='instagram_posts.json', data=updated_posts, overwrite=True)
            self.logger.info(f'Removed posted post from instagram_posts.json.')