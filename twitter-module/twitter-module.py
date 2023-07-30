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
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # Create the API object
    api = tweepy.API(auth)

    try:
        # Post the tweet
        api.update_status(tweet_text)
        print("Tweet posted successfully!")
    except tweepy.TweepError as e:
        print("Error posting tweet:", e)

if __name__ == "__main__":
    # Your tweet text here
    tweet_text = "Hello, this is a test tweet using Tweepy in Python! #Python #Tweepy #TwitterAPI"
    
    # Post the tweet
    post_tweet(tweet_text)
