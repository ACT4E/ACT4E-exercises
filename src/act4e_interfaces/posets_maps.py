from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .maps import FiniteMap, Mapping
from .posets import FinitePoset, Poset

__all__ = [
    "MonotoneMap",
    "FiniteMonotoneMap",
    "FiniteMonotoneMapProperties",
]

C = TypeVar("C")
E = TypeVar("E")
E1 = TypeVar("E1")
E2 = TypeVar("E2")


class MonotoneMap(Generic[E1, E2], Mapping[E1, E2], ABC):
    def source_poset(self) -> Poset[E1]:
        ...

    def target_poset(self) -> Poset[E2]:
        ...


class FiniteMonotoneMap(Generic[E1, E2], MonotoneMap[E1, E2], ABC):
    def source_poset(self) -> FinitePoset[E1]:
        ...

    def target_poset(self) -> FinitePoset[E2]:
        ...


class FiniteMonotoneMapProperties(ABC):
    @abstractmethod
    def is_monotone(self, p1: FinitePoset[E1], p2: FinitePoset[E2], m: FiniteMap[E1, E2]) -> bool:
        """Check if a map is monotone."""

    @abstractmethod
    def is_antitone(self, p1: FinitePoset[E1], p2: FinitePoset[E2], m: FiniteMap[E1, E2]) -> bool:
        """Check if a map is antitone."""
