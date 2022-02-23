from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, overload, TypeVar

from .sets import FiniteSet, Setoid

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")

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
    @overload
    def identity(self, s: FiniteSet[A]) -> FiniteMap[A, A]:
        ...

    @overload
    def identity(self, s: Setoid[A]) -> Mapping[A, A]:
        ...

    @abstractmethod
    def identity(self, s: Setoid[A]) -> Mapping[A, A]:
        """Returns the identity on a set."""

    @abstractmethod
    def compose(self, f: FiniteMap[A, B], g: FiniteMap[B, C]) -> FiniteMap[A, C]:
        """Compose two functions."""
