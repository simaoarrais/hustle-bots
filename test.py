import os
import tweepy
from dotenv import load_dotenv

load_dotenv()
X_BEARER_TOKEN = os.getenv('X_BEARER_TOKEN')
X_API_KEY = os.getenv('X_API_KEY')
X_API_SECRET = os.getenv('X_API_SECRET')
X_ACCESS_TOKEN = os.getenv('X_ACCESS_TOKEN')
X_ACCESS_TOKEN_SECRET = os.getenv('X_ACCESS_TOKEN_SECRET')
X_CLIENT_ID = os.getenv('X_CLIENT_ID')
X_CLIENT_SECRET = os.getenv('X_CLIENT_SECRET')

x_client = tweepy.Client(
                bearer_token=X_BEARER_TOKEN,
                consumer_key=X_API_KEY,
                consumer_secret=X_API_SECRET,
                access_token=X_ACCESS_TOKEN,
                access_token_secret=X_ACCESS_TOKEN_SECRET
            )

auth = tweepy.OAuthHandler(X_API_KEY, X_API_SECRET)
auth.set_access_token(X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET)
x_api = tweepy.API(auth)

media_video = x_api.media_upload('output/1dty38f.mp4', chunked=True, media_category="tweet_video")
media_photo = x_api.media_upload('output/terry.png')
print(f'Video - {media_video}\n')
print(f'Photo - {media_photo}\n')
tweet = x_api.update_status(status='Hello', media_ids=[media_video.media_id_string])