from instagrapi import Client
from dotenv import load_dotenv
import os

def authenticate(insta_username, insta_password):
    client = Client()
    client.login(insta_username, insta_password)
    return client


def upload_post():
   
    client = authenticate(INSTA_USERNAME, INSTA_PASSWORD)

    client.photo_upload(path='/home/simao/Desktop/hustle-bots/media/Nature.png', caption='Teste')

if __name__ == '__main__':
    # Load environment variables from .env file
    load_dotenv(dotenv_path='../.env')

    # Access environment variables required for Reddit API authentication
    INSTA_USERNAME = str(os.getenv('INSTA_USERNAME'))
    INSTA_PASSWORD = str(os.getenv('INSTA_PASSWORD'))
    
    # Post the tweet
    upload_post()