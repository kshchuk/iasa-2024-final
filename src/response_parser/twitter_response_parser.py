from src.response_parser.base_response_parser import ResponseParser


class TwitterResponseParser(ResponseParser):
    def __init__(self):
        super().__init__()

    @staticmethod
    def parse(response) -> dict:
        response_json = response.json()
        data = [tweet["text"] for tweet in response_json["data"]]
        return {"data": data}
