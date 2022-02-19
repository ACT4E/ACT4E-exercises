from typing import TypedDict
from abc import ABC, abstractmethod
from .helper import IOHelper
from .profunctors import FiniteProfunctor


class FiniteProfunctor_desc(TypedDict):
    pass


class FiniteProfunctorRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, data: FiniteProfunctor_desc) -> FiniteProfunctor:
        ...

    @abstractmethod
    def save(self, h: IOHelper, f: FiniteProfunctor) -> FiniteProfunctor_desc:
        ...
