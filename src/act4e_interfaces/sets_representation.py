from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, List, TypeVar, Union

from typing_extensions import TypedDict

from .helper import IOHelper, Serializer
from .sets import FiniteSet
from .types import ConcreteRepr

__all__ = [
    "FiniteSet_desc",
    "FiniteSetUnion_desc",
    "FiniteSetProduct_desc",
    "FiniteSetDisjointUnion_desc",
    "DirectElements_desc",
    "IOHelper",
    "FiniteSetRepresentation",
]

E = TypeVar("E")
E1 = TypeVar("E1")
E2 = TypeVar("E2")


class DirectElements_desc(TypedDict):
    elements: List[ConcreteRepr]


class FiniteSetProduct_desc(TypedDict):
    # product: List[FiniteSet_desc] # cannot be recursive
    product: List[Any]


class FiniteSetDisjointUnion_desc(TypedDict):
    # disunion: List[FiniteSet_desc]  # cannot be recursive
    disunion: List[Any]


class FiniteSetUnion_desc(TypedDict):
    # union: List[FiniteSet_desc]  # cannot be recursive
    union: List[Any]


FiniteSet_desc = Union[
    DirectElements_desc,
    FiniteSetProduct_desc,
    FiniteSetUnion_desc,
    FiniteSetDisjointUnion_desc,
]


class FiniteSetRepresentation(Serializer[FiniteSet[Any], FiniteSet_desc], ABC):
    @abstractmethod
    def load(self, h: IOHelper, data: FiniteSet_desc) -> FiniteSet[Any]:
        """Load a finite set from data structure.
        Throw InvalidFormat if the format is incorrect.
        """

    @abstractmethod
    def save(self, h: IOHelper, f: FiniteSet[Any]) -> FiniteSet_desc:
        """Serializes into a data structure"""
