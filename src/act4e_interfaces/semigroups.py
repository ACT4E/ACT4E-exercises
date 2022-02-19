from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from .sets import FiniteSet, Setoid

__all__ = [
    "Semigroup",
    "FiniteSemigroup",
    "Monoid",
    "Group",
    "FiniteMonoid",
    "FiniteSemigroupConstruct",
    "FiniteFreeGroupConstruct",
    "FiniteGroup",
    "FreeSemigroup",
]

E = TypeVar("E")
C = TypeVar("C")


class Semigroup(Generic[E], ABC):
    @abstractmethod
    def carrier(self) -> Setoid[E]:
        ...

    @abstractmethod
    def compose(self, a: E, b: E) -> E:
        ...


class FiniteSemigroup(Generic[E], Semigroup[E], ABC):
    @abstractmethod
    def carrier(self) -> FiniteSet[E]:
        ...


class FreeSemigroup(Generic[C, E], Semigroup[E], ABC):
    @abstractmethod
    def unit(self, a: C) -> E:
        """From an element of the carrier, returns the element of the free semigroup"""


class FiniteSemigroupConstruct(ABC):
    @abstractmethod
    def free(self, fs: FiniteSet[C]) -> FreeSemigroup[C, Any]:
        """Construct the free semigroup on a set."""


class FreeGroup(Generic[C, E], FreeSemigroup[C, E], ABC):
    ...


class FiniteFreeGroupConstruct(ABC):
    @abstractmethod
    def free(self, fs: FiniteSet[C]) -> FreeGroup[C, E]:
        """Construct the free group on a set."""


class Monoid(Generic[E], Semigroup[E], ABC):
    @abstractmethod
    def identity(self) -> E:
        ...


class Group(Generic[E], Monoid[E], ABC):
    @abstractmethod
    def inverse(self, e: E) -> E:
        """Returns the inverse of an element"""


class FiniteMonoid(Generic[E], Monoid[E], FiniteSemigroup[E], ABC):
    ...


class FiniteGroup(Generic[E], Group[E], FiniteMonoid[E], ABC):
    ...
