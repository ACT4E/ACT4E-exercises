from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .relations import FiniteRelation
from .sets import FiniteSet, Setoid

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")

__all__ = ["FiniteMapOperations", "FiniteMap", "Mapping"]


class FiniteMapOperations(ABC):
    @abstractmethod
    def compose(self, f: FiniteMap[A, B], g: FiniteMap[B, C]) -> FiniteMap[A, C]:
        """compose two functions"""

    @abstractmethod
    def as_relation(self, f: FiniteMap[A, B]) -> FiniteRelation[A, B]:
        """Load the data"""


class Mapping(Generic[A, B], ABC):
    @abstractmethod
    def source(self) -> Setoid[A]:
        ...

    @abstractmethod
    def target(self) -> Setoid[B]:
        ...

    @abstractmethod
    def __call__(self, a: A) -> B:
        ...


class FiniteMap(Generic[A, B], Mapping[A, B], ABC):
    @abstractmethod
    def source(self) -> FiniteSet[A]:
        ...

    @abstractmethod
    def target(self) -> FiniteSet[B]:
        ...
