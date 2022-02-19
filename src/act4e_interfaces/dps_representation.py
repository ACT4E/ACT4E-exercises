from abc import ABC, abstractmethod
from typing import Any, List, TypedDict

from . import FiniteDP
from .posets_representation import FinitePoset_desc
from .sets_representation import FiniteSet_desc
from .types import ConcreteRepr

__all__ = [
    "FiniteDPRepresentation",
    "FiniteDP_desc",
]


class FiniteDP_desc(TypedDict):
    F: FinitePoset_desc
    R: FinitePoset_desc
    I: FiniteSet_desc
    feas: List[List[ConcreteRepr]]


class FiniteDPRepresentation(ABC):
    @abstractmethod
    def load(self, yaml_data: FiniteDP_desc) -> FiniteDP[Any, Any]:
        ...

    @abstractmethod
    def save(self, f: FiniteDP[Any, Any]) -> FiniteDP_desc:
        ...
