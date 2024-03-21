import utils

from reddit_class import RedditClass

async def handle_discord_commands(message, client, logger):
    if message.channel.name == 'redxig':

        # ----------------------------------- Hello ---------------------------------- #
        if message.content.startswith('hello'):
            await message.channel.send('Hello!')

        # ---------------------------------- Reddit ---------------------------------- #
        elif message.content.startswith('init reddit'):
            reddit_client = RedditClass(logger=logger)
            reddit_subreddit = reddit_client.access_subreddit()
            top_posts = reddit_client.get_top_posts(reddit_subreddit, n_posts=3, search_limit=3)
            utils.save_json_file(data=top_posts, logger=logger)
            await message.channel.send('Reddit!')

        elif message.content.startswith('give'):
            # Read the JSON data from the file
            json_data = utils.read_json_file('test.json')

            # Process the post information and send a formatted message to the Discord channel
            for post in json_data:
                title = post['title']
                score = post['score']
                url = post['url']
                author = post['author']
                permalink = post['permalink']

                # Format the message
                post_info_message = f"**Title:** {title}\n" \
                                    f"**Score:** {score}\n" \
                                    f"**URL:** {url}\n" \
                                    f"**Author:** {author}\n" \
                                    f"**Permalink:** https://www.reddit.com{permalink}"

                # Send the message to the Discord channel
                await message.channel.send(post_info_message)
