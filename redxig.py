# import discord_module.discord_module as discord
# import instagram_module.instagram_module as instagram
from reddit_module import reddit_module as reddit
# import twitter_module.twitter_module as twitter

import utils
import logging
import os
    
if __name__ == "__main__":
    
    reddit_client = reddit.access_reddit()
    subreddit = reddit.access_subreddit(reddit_client, subreddit='NatureIsFuckingLit')
    top_posts_above_threshold = reddit.get_top_posts(subreddit, threshold=1000, n_posts=3, search_limit=3)
    utils.save_json_file('test.json', top_posts_above_threshold)
