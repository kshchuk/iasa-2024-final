from enum import Enum, auto


class SentimentType(Enum):
    NEGATIVE = auto()
    POSITIVE = auto()
    NEUTRAL = auto()

    def __eq__(self, other):
        return self.value == other.value
