from instagrapi import Client
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access environment variables required for Reddit API authentication
INSTA_USERNAME = str(os.getenv('INSTA_USERNAME'))
INSTA_PASSWORD = str(os.getenv('INSTA_PASSWORD'))

def upload_post():
   
    client = Client()
    client.login(INSTA_USERNAME, INSTA_PASSWORD)

    client.photo_upload(path='/home/simao/Desktop/hustle-bots/media/Nature.png', caption='Teste')

if __name__ == '__main__':
    
    # Post the tweet
    upload_post()