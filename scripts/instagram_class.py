import os
import utils

from dotenv import load_dotenv
from logger import CustomLogger
from instagrapi import Client

class InstagramClass:
    def __init__(self, logger=None, credentials=None):
        self.logger = logger or CustomLogger().get_logger()
        self.instagram_client = self.authenticate(credentials)

    def authenticate(self, credentials):
        try:
            instagram_client = Client()
            instagram_client.login(credentials.get('username'), credentials.get('password'))
            self.logger.info(f'Instagram has logged in.')
            return instagram_client
        except instagrapi.exceptions as e:
            return None

    def upload_post(self, post_data):
        post = self.instagram_client.photo_upload(path='/home/simao/Desktop/hustle-bots/media/Nature.png', caption='Teste')
        self.logger.info(f'UPLOAD POST: {post}')
    
    def process_next_post(self):
        # Read the next post from x_posts.json
        post_data = utils.get_next_post(file_path='instagram_posts.json', logger=self.logger)
        if post_data:
            
            # Upload post
            # tweet_text = f"{post_data['title']} {post_data['url']}"
            self.upload_post(post_data)

            # Remove the posted post from x_posts.json
            utils.remove_post_from_file(file_path='instagram_posts.json', post_data=post_data, logger=self.logger)
        else:
            self.logger.warning(f'No posts available to process.')