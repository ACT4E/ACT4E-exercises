from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .posets import FinitePoset, Poset
from .posets_maps import MonotoneMap
from .relations import FiniteRelation
from .sets import FiniteSet, Setoid

__all__ = [
    "FiniteDP",
    "FiniteDPOperations",
    "DP",
    "DPI",
    "DPConstructors",
]

E1 = TypeVar("E1")
E2 = TypeVar("E2")

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")

O1 = TypeVar("O1")
O2 = TypeVar("O2")

Morphism = TypeVar("Morphism")

Object1 = TypeVar("Object1")
Morphism1 = TypeVar("Morphism1")
Object2 = TypeVar("Object2")
Morphism2 = TypeVar("Morphism2")

F = TypeVar("F")
I = TypeVar("I")
R = TypeVar("R")


class DPI(Generic[F, I, R], ABC):
    @abstractmethod
    def functionality(self) -> Poset[F]:
        ...

    @abstractmethod
    def implementations(self) -> Setoid[I]:
        ...

    @abstractmethod
    def costs(self) -> Poset[R]:
        ...

    @abstractmethod
    def requires(self, i: I) -> R:
        ...

    @abstractmethod
    def provides(self, i: I) -> F:
        ...


class FiniteDPI(Generic[F, I, R], DPI[F, I, R], ABC):
    @abstractmethod
    def functionality(self) -> FinitePoset[F]:
        ...

    @abstractmethod
    def implementations(self) -> FiniteSet[I]:
        ...

    @abstractmethod
    def costs(self) -> FinitePoset[R]:
        ...


class DP(Generic[F, R], ABC):
    @abstractmethod
    def functionality(self) -> Poset[F]:
        ...

    @abstractmethod
    def costs(self) -> Poset[R]:
        ...

    @abstractmethod
    def feasible(self, f: F, r: R) -> bool:
        ...


class FiniteDP(Generic[F, R], DP[F, R], ABC):
    @abstractmethod
    def functionality(self) -> FinitePoset[F]:
        ...

    @abstractmethod
    def costs(self) -> FinitePoset[R]:
        ...


class DPConstructors(ABC):
    @abstractmethod
    def companion(self, f: MonotoneMap[E1, E2]) -> DP[E1, E2]:
        ...

    @abstractmethod
    def conjoint(self, f: MonotoneMap[E1, E2]) -> DP[E1, E2]:
        ...


class FiniteDPOperations(ABC):
    @abstractmethod
    def series(self, dp1: FiniteDP[A, B], dp2: FiniteDP[B, C]) -> FiniteDP[A, C]:
        ...

    @abstractmethod
    def union(self, dp1: FiniteDP[A, B], dp2: FiniteDP[A, B]) -> FiniteDP[A, B]:
        ...

    @abstractmethod
    def intersection(self, dp1: FiniteDP[A, B], dp2: FiniteDP[A, B]) -> FiniteDP[A, B]:
        ...

    @abstractmethod
    def from_relation(self, f: FiniteRelation[A, B]) -> FiniteDP[A, B]:
        ...
