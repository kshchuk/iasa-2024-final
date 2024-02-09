from abc import ABC, abstractmethod

import requests


class ResponseParser(ABC):
    """Base class for response parser. All response parser should inherit this class."""

    @staticmethod
    def parse(response: requests.Response) -> dict:
        pass
