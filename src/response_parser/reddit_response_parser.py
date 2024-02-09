from src.response_parser.base_response_parser import ResponseParser


class RedditResponseParser(ResponseParser):
    def __init__(self):
        super().__init__()

    @staticmethod
    def parse(response) -> dict:
        response_json = response.json()
        data = [response_json['post']['content']]
        for comment in response_json["comments"]:
            data.append(comment["content"])

        return {"data": data}
