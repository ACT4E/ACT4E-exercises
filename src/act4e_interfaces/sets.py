from abc import ABC, abstractmethod
from typing import Callable, Generic, Iterator, TypeVar

from .helper import IOHelper
from .types import ConcreteRepr

E = TypeVar("E")
E1 = TypeVar("E1")
E2 = TypeVar("E2")
E3 = TypeVar("E3")

__all__ = [
    "Setoid",
    "EnumerableSet",
    "FiniteSet",
    "EnumerableSetsOperations",
    "FiniteSetProperties",
    "EnumerableSetsOperations",
]


class Setoid(Generic[E], ABC):
    """
    A setoid is something to which elements may belong,
    has a way of distinguishing elements,
    and is able to (de)serialize its elements.
    """

    @abstractmethod
    def contains(self, x: E) -> bool:
        """Returns true if the element is in the set."""

    def equal(self, x: E, y: E) -> bool:
        """Returns True if the two elements are to be considered equal."""
        return x == y  # default is to use the Python equality

    def apart(self, x: E, y: E) -> bool:
        return not self.equal(x, y)

    @abstractmethod
    def save(self, h: IOHelper, x: E) -> ConcreteRepr:
        ...

    @abstractmethod
    def load(self, h: IOHelper, o: ConcreteRepr) -> E:
        ...


class EnumerableSet(Generic[E], Setoid[E], ABC):
    @abstractmethod
    def elements(self) -> Iterator[E]:
        """Note: possibly non-terminating."""


class FiniteSet(Generic[E], EnumerableSet[E], ABC):
    """A finite set has a finite size."""

    @abstractmethod
    def size(self) -> int:
        """Return the size of the finite set."""


class FiniteSetProperties(ABC):
    @abstractmethod
    def is_subset(self, a: FiniteSet[E], b: FiniteSet[E]) -> bool:
        """True if `a` is a subset of `b`."""

    def equal(self, a: FiniteSet[E], b: FiniteSet[E]) -> bool:
        return self.is_subset(a, b) and self.is_subset(b, a)

    def is_strict_subset(self, a: FiniteSet[E], b: FiniteSet[E]) -> bool:
        return self.is_subset(a, b) and not self.is_subset(b, a)


class EnumerableSetsOperations(ABC):
    @abstractmethod
    def make_set_sequence(self, f: Callable[[int], E]) -> EnumerableSet[E]:
        """Creates an EnumerableSet from a function that gives the
        i-th element."""

    @abstractmethod
    def union_esets(self, a: EnumerableSet[E], b: EnumerableSet[E]) -> EnumerableSet[E]:
        """Creates the union of two EnumerableSet."""
