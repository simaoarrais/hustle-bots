from discord_class import DiscordClass
from dotenv import load_dotenv

if __name__ == "__main__":
    # Load environment
    load_dotenv()

    # Initialize Discord bot
    discord_bot = DiscordClass()
    discord_bot.init_discord_client()
