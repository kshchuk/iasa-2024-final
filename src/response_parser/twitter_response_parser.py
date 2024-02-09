from src.response_parser.base_response_parser import ResponseParser


class TwitterResponseParser(ResponseParser):
    def __init__(self):
        super().__init__()

    @staticmethod
    def parse(response) -> dict:
        data = [tweet["text"] for tweet in response["data"]]
        return {"data": data}
