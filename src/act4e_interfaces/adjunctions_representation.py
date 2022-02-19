from abc import ABC, abstractmethod
from typing import Any, TypedDict

from .adjunctions import FiniteAdjunction
from .helper import IOHelper

__all__ = ["FiniteAdjunction_desc", "FiniteAdjunctionRepresentation"]


class FiniteAdjunction_desc(TypedDict):
    pass


class FiniteAdjunctionRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, data: FiniteAdjunction_desc) -> FiniteAdjunction[Any, Any, Any, Any]:
        ...

    @abstractmethod
    def save(self, h: IOHelper, f: FiniteAdjunction[Any, Any, Any, Any]) -> FiniteAdjunction_desc:
        ...
