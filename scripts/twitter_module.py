import tweepy
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables required for Reddit API authentication
BEARER_TOKEN = str(os.getenv('X_BEARER_TOKEN'))
API_KEY = str(os.getenv('X_API_KEY'))
API_SECRET = str(os.getenv('X_API_SECRET'))
ACCESS_TOKEN = str(os.getenv('X_ACCESS_TOKEN'))
ACCESS_TOKEN_SECRET = str(os.getenv('X_ACCESS_TOKEN_SECRET'))
CLIENT_ID = str(os.getenv('X_CLIENT_ID'))
CLIENT_SECRET = str(os.getenv('X_CLIENT_SECRET'))

def post_tweet(tweet_text):
   
    client = tweepy.Client(bearer_token=BEARER_TOKEN, 
                           consumer_key=API_KEY, 
                           consumer_secret=API_SECRET, 
                           access_token=ACCESS_TOKEN, 
                           access_token_secret=ACCESS_TOKEN_SECRET)

    client.create_tweet(text=tweet_text)

if __name__ == '__main__':
    # Your tweet text here
    tweet_text = 'Hello, this is a test tweet using Tweepy in Python! #Python #Tweepy #TwitterAPI'
    
    # Post the tweet
    post_tweet(tweet_text)
