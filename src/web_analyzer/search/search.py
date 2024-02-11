from abc import ABC, abstractmethod
from typing import List


class StringSearchStrategy(ABC):
    @abstractmethod
    def contains(self, string: str, patterns: List[str]) -> bool:
        pass


class AndStrategy(StringSearchStrategy):
    def contains(self, string: str, patterns: List[str]) -> bool:
        return all(pattern in string for pattern in patterns)


class OrStrategy(StringSearchStrategy):
    def contains(self, string: str, patterns: List[str]) -> bool:
        return any(pattern in string for pattern in patterns)


class AtLeastStrategy(StringSearchStrategy):
    def __init__(self, limit):
        self.limit = limit

    def contains(self, string: str, patterns: List[str]) -> bool:
        if len(patterns) < self.limit:
            return False
        found_count = sum(1 for pattern in patterns if pattern in string)
        return found_count >= self.limit
