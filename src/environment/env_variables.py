from dotenv import load_dotenv
from dotenv import find_dotenv
import os


class Environment:
    @staticmethod
    def reddit_user_id():
        _ = load_dotenv(find_dotenv())
        return os.getenv("REDDIT_CLIENT_KEY")

    @staticmethod
    def reddit_user_secret():
        return os.getenv("REDDIT_CLIENT_SECRET")
