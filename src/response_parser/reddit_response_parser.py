from src.response_parser.base_response_parser import ResponseParser


class RedditResponseParser(ResponseParser):
    def __init__(self):
        super().__init__()

    @staticmethod
    def parse(response: dict) -> dict:
        data = [response['post']['content']]
        for comment in response["comments"]:
            data.append(comment["content"])

        return {"data": data}
