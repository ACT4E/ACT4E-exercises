from abc import ABC, abstractmethod
from typing import Callable, Iterator

from .types import Element


class Setoid(ABC):
    """ A set is something to which elements may belong. """

    @abstractmethod
    def belongs(self, x: Element) -> bool:
        ...

    @abstractmethod
    def equal(self, x: Element, y: Element) -> bool:
        """ Returns True if the two elements are to be considered equal. """


class Relation(ABC):

    @abstractmethod
    def source(self) -> Setoid:
        """ Returns a setoid """

    @abstractmethod
    def target(self) -> Setoid:
        """ Returns a setoid """

    @abstractmethod
    def holds(self, a: Element, b: Element) -> bool:
        """ Returns true if the two elements are related """


class EnumerableSet(Setoid, ABC):
    """ An enumerable set can construct its elements. """

    @abstractmethod
    def elements(self) -> Iterator[Element]:
        """ This iterator could not terminate. """


class Poset(ABC):

    @abstractmethod
    def carrier(self) -> Setoid:
        ...

    @abstractmethod
    def leq(self, a: Element, b: Element) -> bool:
        ...


class SetoidOperations(ABC):

    @classmethod
    @abstractmethod
    def union_setoids(cls, a: Setoid, b: Setoid) -> Setoid:
        """ Creates the union of two Setoids. """

    @classmethod
    @abstractmethod
    def intersection_setoids(cls, a: Setoid, b: Setoid) -> Setoid:
        """ Creates the intersection of two Setoids. """


class EnumerableSetsOperations(ABC):

    @classmethod
    @abstractmethod
    def make_set_sequence(cls, f: Callable[[int], object]):
        """ Creates an EnumerableSet from a function that gives the
            i-th element. """

    @classmethod
    @abstractmethod
    def union_esets(cls, a: EnumerableSet, b: EnumerableSet) -> EnumerableSet:
        """ Creates the union of two EnumerableSet. """
