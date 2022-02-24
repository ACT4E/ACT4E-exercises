from __future__ import annotations

from abc import ABC
from typing import Any, List

from typing_extensions import TypedDict

from .helper import Serializer
from .maps import FiniteMap
from .sets_representation import FiniteSet_desc
from .types import ConcreteRepr

__all__ = [
    "FiniteMap_desc",
    "FiniteMapRepresentation",
]


class FiniteMap_desc(TypedDict):
    source: FiniteSet_desc
    target: FiniteSet_desc
    values: List[List[ConcreteRepr]]


class FiniteMapRepresentation(Serializer[FiniteMap[Any, Any], FiniteMap_desc], ABC):
    pass


# @abstractmethod
# def load(self, h: IOHelper, s: FiniteMap_desc) -> FiniteMap[Any, Any]:
#     ...
#
# @abstractmethod
# def save(self, h: IOHelper, m: FiniteMap[Any, Any]) -> FiniteMap_desc:
#     ...
