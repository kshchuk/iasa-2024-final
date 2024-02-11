import os


class Environment:
    @staticmethod
    def reddit_user_id():
        return os.getenv("REDDIT_CLIENT_KEY")

    @staticmethod
    def reddit_user_secret():
        return os.getenv("REDDIT_CLIENT_SECRET")

    @staticmethod
    def youtube_api_key():
        return os.getenv("YOUTUBE_API_KEY")
