from abc import ABC, abstractmethod
from typing import Any, Generic, Mapping, TypeVar

from .maps import FiniteMap
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
    "FiniteSemigroupMorphism",
    "GroupMorphism",
    "MonoidMorphism",
    "SemigroupMorphism",
    "FiniteGroupMorphism",
    "FiniteMonoidMorphism",
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


E1 = TypeVar("E1", contravariant=True)
E2 = TypeVar("E2", covariant=True)


class SemigroupMorphism(Generic[E1, E2], ABC):
    @abstractmethod
    def source(self) -> Semigroup[E1]:
        ...

    @abstractmethod
    def target(self) -> Semigroup[E2]:
        ...

    @abstractmethod
    def mapping(self) -> Mapping[E1, E2]:
        ...


class MonoidMorphism(Generic[E1, E2], SemigroupMorphism[E1, E2], ABC):
    @abstractmethod
    def source(self) -> Monoid[E1]:
        ...

    @abstractmethod
    def target(self) -> Monoid[E2]:
        ...


class GroupMorphism(Generic[E1, E2], MonoidMorphism[E1, E2], ABC):
    @abstractmethod
    def source(self) -> Group[E1]:
        ...

    @abstractmethod
    def target(self) -> Group[E2]:
        ...


class FiniteSemigroupMorphism(Generic[E1, E2], SemigroupMorphism[E1, E2], ABC):
    @abstractmethod
    def source(self) -> FiniteSemigroup[E1]:
        ...

    @abstractmethod
    def target(self) -> FiniteSemigroup[E2]:
        ...

    @abstractmethod
    def mapping(self) -> FiniteMap[E1, E2]:
        ...


class FiniteMonoidMorphism(Generic[E1, E2], MonoidMorphism[E1, E2], ABC):
    @abstractmethod
    def source(self) -> FiniteMonoid[E1]:
        ...

    @abstractmethod
    def target(self) -> FiniteMonoid[E2]:
        ...

    @abstractmethod
    def mapping(self) -> FiniteMap[E1, E2]:
        ...


class FiniteGroupMorphism(Generic[E1, E2], GroupMorphism[E1, E2], ABC):
    @abstractmethod
    def source(self) -> FiniteGroup[E1]:
        ...

    @abstractmethod
    def target(self) -> FiniteGroup[E2]:
        ...

    @abstractmethod
    def mapping(self) -> FiniteMap[E1, E2]:
        ...
