from abc import ABC, abstractmethod

from .types import Element
from .sets import FiniteMap, FiniteSet, Mapping, Setoid


class Semigroup(ABC):
    @abstractmethod
    def carrier(self) -> Setoid:
        ...

    @abstractmethod
    def composition(self) -> Mapping:
        ...


class FiniteSemigroup(Semigroup, ABC):
    @abstractmethod
    def carrier(self) -> FiniteSet:
        ...

    @abstractmethod
    def composition(self) -> FiniteMap:
        ...


class FreeSemigroup(Semigroup, ABC):
    @abstractmethod
    def unit(self, a: Element) -> Element:
        """ From an element of the carrier, returns the element of the free semigroup """


class FiniteSemigroupConstruct(ABC):
    @abstractmethod
    def free(self, fs: FiniteSet) -> FreeSemigroup:
        """ Construct the free semigroup on a set. """


class FreeGroup(Semigroup, ABC):
    @abstractmethod
    def unit(self, a: Element) -> Element:
        """ From an element of the carrier, returns the element of the free group. """


class FiniteFreeGroupConstruct(ABC):
    @abstractmethod
    def free(self, fs: FiniteSet) -> FreeGroup:
        """ Construct the free group on a set. """


class Monoid(Semigroup, ABC):
    @abstractmethod
    def identity(self) -> Element:
        ...


class Group(Monoid, ABC):
    @abstractmethod
    def inverse(self) -> Mapping:
        """ Returns the inverse of an element"""


class FiniteMonoid(Monoid, FiniteSemigroup, ABC):
    """"""


class FiniteGroup(Group, FiniteMonoid, ABC):
    @abstractmethod
    def inverse(self) -> FiniteMap:
        ...
