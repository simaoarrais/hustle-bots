from dotenv import load_dotenv

import tweepy
import os

# Load environment variables from .env file
load_dotenv()

# Replace with your own Twitter API credentials
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

def post_tweet(tweet_text):
    # Authenticate with Twitter API
    client = tweepy.Client(consumer_key=API_KEY,
                         consumer_secret=API_SECRET,
                         access_token=ACCESS_TOKEN,
                         access_token_secret=ACCESS_TOKEN_SECRET)

    # Post the tweet
    client.create_tweet(text=tweet_text)
    print("Tweet posted successfully!")

if __name__ == "__main__":
    # Your tweet text here
    tweet_text = "Hello, this is a test tweet using Tweepy in Python!\n #Python #Tweepy #TwitterAPI"
    
    # Post the tweet
    post_tweet(tweet_text)
