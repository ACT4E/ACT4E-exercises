from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .sets import FiniteSet, Setoid

A = TypeVar("A", contravariant=True)
B = TypeVar("B", covariant=True)
E1 = TypeVar("E1", contravariant=True)
E2 = TypeVar("E2")
E3 = TypeVar("E3", covariant=True)

__all__ = ["FiniteMapOperations", "FiniteMap", "Mapping"]


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
    """A finite map is a mapping between two finite sets."""

    @abstractmethod
    def source(self) -> FiniteSet[A]:
        ...

    @abstractmethod
    def target(self) -> FiniteSet[B]:
        ...


class FiniteMapOperations(ABC):
    @abstractmethod
    def identity(self, s: FiniteSet[A]) -> FiniteMap[A, A]:
        """Returns the identity on a set."""

    @abstractmethod
    def compose(self, f: FiniteMap[E1, E2], g: FiniteMap[E2, E3]) -> FiniteMap[E1, E3]:
        """Compose two functions."""
