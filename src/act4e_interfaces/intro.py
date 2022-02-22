__all__ = ["SimpleIntro"]

from abc import ABC, abstractmethod


class SimpleIntro(ABC):
    @abstractmethod
    def sum(self, a: int, b: int) -> int:
        """Returns the sum of two integers."""
