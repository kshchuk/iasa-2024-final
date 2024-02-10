import json
from abc import ABC


class ResponseParser(ABC):
    """Base class for response parser. All response parser should inherit this class."""

    @staticmethod
    def parse(response: dict) -> dict:
        pass
