from dotenv import load_dotenv

import praw
import os

def access_reddit():
    # Load environment variables from .env file
    load_dotenv()

    # Access environment variables
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    print(f"username: {username}\
          \npassword: {password}\
          \nclient_id: {client_id}\
          \nclient_secret: {client_secret}")
    return 0

if __name__ == "__main__":
    access_reddit()