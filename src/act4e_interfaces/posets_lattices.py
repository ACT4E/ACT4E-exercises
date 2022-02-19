from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .posets import Poset
from .sets import FiniteSet

__all__ = [
    "MeetSemilattice",
    "Lattice",
    "JoinSemilattice",
    "FiniteLattice",
]

C = TypeVar("C")
E = TypeVar("E")


class MeetSemilattice(Generic[E], Poset[E], ABC):
    @abstractmethod
    def meet(self, x: E, y: E) -> E:
        ...

    @abstractmethod
    def top(self) -> E:
        ...


class JoinSemilattice(Generic[E], Poset[E], ABC):
    @abstractmethod
    def join(self, x: E, y: E) -> E:
        ...

    @abstractmethod
    def bottom(self) -> E:
        ...


class Lattice(Generic[E], JoinSemilattice[E], MeetSemilattice[E], ABC):
    ...


class FiniteLattice(Generic[E], Lattice[E], ABC):
    @abstractmethod
    def carrier(self) -> FiniteSet[E]:
        ...
