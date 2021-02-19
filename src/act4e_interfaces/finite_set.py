from abc import ABC, abstractmethod


class Set(ABC):

    @abstractmethod
    def belongs(self, x) -> bool:
        ...
