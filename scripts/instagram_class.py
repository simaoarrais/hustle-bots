import os
import utils
import db_utils

from logger import CustomLogger
from instagrapi import Client

class InstagramClass:
    def __init__(self, logger=None, credentials=None, db_credentials=None):
        self.logger = logger or CustomLogger().get_logger()
        self.instagram_client = self.authenticate(credentials)
        self.db = self.authenticate_db(db_credentials)

    def authenticate(self, credentials):
        try:
            instagram_client = Client()
            instagram_client.delay_range = [1, 3]
            instagram_client.login(credentials.get('username'), credentials.get('password'))
            self.logger.info(f'Instagram has logged in.')
            return instagram_client
        except instagrapi.exceptions as e:
            return None
    
    def authenticate_db(self, db_credentials):
        host = db_credentials.get('host')
        port = db_credentials.get('port')
        db_name = db_credentials.get('db_name')
        return db_utils.get_db(host, port, db_name)
    
    def get_next_post(self):
        collection = self.db['posts']
        return db_utils.get_next_post_insta(collection)
    
    def reject_post(self, post):
        collection = self.db['posts']
        return db_utils.reject_post(collection, post)

    def upload_post(self, post):
        title = utils.standardize_title(post['title'])
        if post['is_video']:
            media_path = utils.download_video(post)
            post = self.instagram_client.clip_upload(path=media_path, caption=title)
        else:
            media_path = utils.download_photo(post)
            post = self.instagram_client.photo_upload(path=media_path, caption=title)

        collection = self.db['posts']
        db_utils.update_post_status_insta(collection, post)
        self.logger.info(f'UPLOAD POST: {post}')

        return post
        # try:

        # except Exception as e:
        #     self.logger.error(f'Error uploading post: {e}')