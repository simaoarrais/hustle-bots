import discord_module.discord_module as discord
import instagram_module.instagram_module as instagram
import reddit_module.reddit_module as reddit
import twitter_module.twitter_module as twitter

import utils
import logging
import os

def main():
    reddit_client = reddit.access_reddit()
    print(reddit_client)
    pass

if __name__ == "__main__":
    main()
