from abc import ABC, abstractmethod
from typing import Generic, TypeVar

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


class Poset(Generic[E], ABC):
    @abstractmethod
    def carrier(self) -> Setoid[E]:
        ...

    @abstractmethod
    def holds(self, a: E, b: E) -> bool:
        ...


class FinitePoset(Generic[E], Poset[E], ABC):
    """Implementation of finite posets."""

    @abstractmethod
    def carrier(self) -> FiniteSet[E]:
        ...
