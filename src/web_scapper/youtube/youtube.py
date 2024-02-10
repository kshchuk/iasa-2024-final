from datetime import datetime, timedelta
from googleapiclient.discovery import build
from web_scapper.search.post import Article
from web_scapper.search.post import Comment
from typing import List
from environment.env_variables import Environment
from web_scapper.search.common_search import SearchEngine
from googleapiclient.errors import HttpError


class YouTubeReader(SearchEngine):

    def __init__(self):
        self.youtube = None

    def build(self):
        api_key = Environment.youtube_api_key()
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        return self

    def collect_recommended(self, keywords: List[str], period: str):
        return self.collect_data(keywords, period)

    def collect_data(self, keywords: List[str], period: str, post_limit=10, comment_limit=15) -> List[Article]:
        posts = []
        if post_limit < 1:
            return posts

        past = SearchEngine.period_to_days(period)
        period_ago = datetime.now() - timedelta(days=past)
        period_ago_iso = period_ago.isoformat("T") + "Z"
        search_response = self.youtube.search().list(
            q=keywords,
            part='id,snippet',
            maxResults=post_limit,
            publishedAfter=period_ago_iso,
            type='video'
        ).execute()

        video_ids = [item['id']['videoId'] for item in search_response['items']]
        video_response = self.youtube.videos().list(
            part='id,snippet,statistics',
            id=','.join(video_ids)
        ).execute()

        for item in video_response['items']:
            video_id = item['id']
            video_title = item['snippet']['title']
            description = item['snippet']['description']
            likes = item['statistics'].get('likeCount', 0)
            post = Article(title=video_title, content=description, votes=likes)

            posts.append(post)
            if comment_limit < 1:
                continue
            if self._comments_disabled(item):
                continue
            try:
                comments_response = self.youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    maxResults=comment_limit,
                    textFormat='plainText'
                ).execute()
                comments = []
                for comment in comments_response['items']:
                    topLevelComment = comment['snippet']['topLevelComment']
                    comment_text = topLevelComment['snippet']['textDisplay']
                    comment_likes = topLevelComment['snippet'].get('likeCount', 0)

                    comment = Comment()
                    comment.content = comment_text
                    comment.votes = comment_likes
                    comments.append(comment)
                post.comments = comments
            except HttpError as e:
                error_message = e._get_reason()
                if e.resp.status == 403:
                    if "commentsDisabled" in error_message:
                        continue
                    else:
                        print("Error: ", error_message)
                else:
                    print("Error: ", error_message)

        return posts

    def _comments_disabled(self, item):
        return 'commentCount' not in item['statistics']
