from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .relations import Relation
from .sets import (
    FiniteSet,
    Setoid,
)

__all__ = [
    "Poset",
    "FinitePoset",
]

C = TypeVar("C")
E = TypeVar("E")


class Poset(Generic[E], Relation[E, E], ABC):
    def source(self) -> Setoid[E]:
        return self.carrier()

    def target(self) -> Setoid[E]:
        return self.carrier()

    @abstractmethod
    def carrier(self) -> Setoid[E]:
        ...

    @abstractmethod
    def holds(self, a: E, b: E) -> bool:
        ...


class FinitePoset(Generic[E], Poset[E], ABC):
    @abstractmethod
    def carrier(self) -> FiniteSet[E]:
        ...
