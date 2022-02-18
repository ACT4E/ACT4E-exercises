from abc import ABC, abstractmethod
from typing import Any, Callable, Generic, Iterator, overload, Sequence, Tuple, TypeVar

from .helper import IOHelper
from .types import ConcreteRepr

E = TypeVar("E")
E1 = TypeVar("E1")
E2 = TypeVar("E2")
E3 = TypeVar("E3")


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


class Mapping(Generic[E1, E2], ABC):
    @abstractmethod
    def source(self) -> Setoid[E1]:
        ...

    @abstractmethod
    def target(self) -> Setoid[E2]:
        ...

    @abstractmethod
    def __call__(self, a: E1) -> E2:
        ...


class EnumerableSet(Setoid[E], ABC):
    @abstractmethod
    def elements(self) -> Iterator[E]:
        """Note: possibly non-terminating."""


class FiniteSet(EnumerableSet[E], ABC):
    """A finite set has a finite size."""

    @abstractmethod
    def size(self) -> int:
        """Return the size of the finite set."""


class FiniteMap(Mapping[E1, E2], ABC):
    @abstractmethod
    def source(self) -> FiniteSet[E1]:
        ...

    @abstractmethod
    def target(self) -> FiniteSet[E2]:
        ...


class FiniteSetProperties(ABC):
    @abstractmethod
    def is_subset(self, a: FiniteSet[E], b: FiniteSet[E]) -> bool:
        """True if `a` is a subset of `b`."""

    def equal(self, a: FiniteSet[E], b: FiniteSet[E]) -> bool:
        return self.is_subset(a, b) and self.is_subset(b, a)

    def is_strict_subset(self, a: FiniteSet[E], b: FiniteSet[E]) -> bool:
        return self.is_subset(a, b) and not self.is_subset(b, a)


### Set product

C = TypeVar("C")  # composite


class SetProduct(Generic[C, E], Setoid[E], ABC):
    """A set product is a setoid that can be factorized."""

    @abstractmethod
    def components(self) -> Sequence[Setoid[C]]:
        """Returns the components of the product"""

    @abstractmethod
    def pack(self, args: Sequence[C]) -> E:
        """Packs an element of each setoid into an element of the mapping"""
        raise NotImplementedError()

    @abstractmethod
    def unpack(self, args: E) -> Sequence[C]:
        """Packs an element of each setoid into an element of the mapping"""
        raise NotImplementedError()


class FiniteSetProduct(Generic[C, E], FiniteSet[E], SetProduct[C, E], ABC):
    """Specialization of SetProduct where we deal with FiniteSets"""

    @abstractmethod
    def components(self) -> Sequence[FiniteSet[C]]:
        """Returns the components"""


class MakeSetProduct(ABC):
    @overload
    def product(self, components: Sequence[FiniteSet[C]]) -> FiniteSetProduct[C, Any]:
        ...

    @overload
    def product(self, components: Sequence[Setoid[C]]) -> SetProduct[C, Any]:
        ...

    @abstractmethod
    def product(self, components: Sequence[Setoid[C]]) -> SetProduct[C, Any]:
        ...


## Set union


class SetUnion(Generic[C, E], Setoid[E], ABC):
    """A set product is a setoid that can be factorized."""

    @abstractmethod
    def components(self) -> Sequence[Setoid[C]]:
        """Returns the components of the union"""


class EnumerableSetUnion(Generic[C, E], EnumerableSet[E], SetUnion[C, E], ABC):
    """Specialization of SetUnion where we deal with FiniteSets"""

    @abstractmethod
    def components(self) -> Sequence[EnumerableSet[C]]:
        """Returns the components of the union"""


class FiniteSetUnion(Generic[C, E], FiniteSet[E], EnumerableSetUnion[C, E], ABC):
    """Specialization of SetUnion where we deal with FiniteSets"""

    @abstractmethod
    def components(self) -> Sequence[FiniteSet[C]]:
        """Returns the components of the union"""


class MakeSetUnion(ABC):
    @overload
    def union(self, components: Sequence[FiniteSet[C]]) -> FiniteSetUnion[C, Any]:
        ...

    @overload
    def union(self, components: Sequence[EnumerableSet[C]]) -> EnumerableSetUnion[C, Any]:
        ...

    @abstractmethod
    def union(self, components: Sequence[Setoid[C]]) -> SetUnion[C, Any]:
        ...


### Power set


class SetOfFiniteSubsets(Generic[C, E], Setoid[E], ABC):
    """A set of subsets."""

    @abstractmethod
    def contents(self, e: E) -> Iterator[C]:
        """Returns the contents of an element representing a subset."""

    @abstractmethod
    def construct(self, elements: Sequence[C]) -> E:
        """Get the element representing the given subset."""


class FiniteSetOfFiniteSubsets(Generic[C, E], SetOfFiniteSubsets[C, E], FiniteSet[E], ABC):
    pass


class MakePowerSet(ABC):
    @overload
    def powerset(self, s: FiniteSet[C]) -> FiniteSetOfFiniteSubsets[C, Any]:
        ...

    @overload
    def powerset(self, s: Setoid[C]) -> SetOfFiniteSubsets[C, Any]:
        ...

    @abstractmethod
    def powerset(self, s: Setoid[C]) -> SetOfFiniteSubsets[C, Any]:
        """Creates the powerset of a finite set."""


### disjoint union


class SetDisjointUnion(Generic[C, E], Setoid[E], ABC):
    @abstractmethod
    def components(self) -> Sequence[Setoid[C]]:
        """Returns the components of the union"""

    @abstractmethod
    def pack(self, i: int, e: C) -> E:
        """Injection mapping."""
        raise NotImplementedError()

    @abstractmethod
    def unpack(self, e: E) -> Tuple[int, C]:
        raise NotImplementedError()


class FiniteSetDisjointUnion(Generic[C, E], FiniteSet[E], SetDisjointUnion[C, E], ABC):
    """Specialization of SetDisjointUnion where we deal with FiniteSets."""

    @abstractmethod
    def components(self) -> Sequence[FiniteSet[C]]:
        ...


class MakeSetDisjointUnion(ABC):
    @overload
    def disjoint_union(self, components: Sequence[FiniteSet[C]]) -> FiniteSetDisjointUnion[C, Any]:
        ...

    @overload
    def disjoint_union(self, components: Sequence[Setoid[C]]) -> SetDisjointUnion[C, Any]:
        ...

    @abstractmethod
    def disjoint_union(self, components: Sequence[Setoid[C]]) -> SetDisjointUnion[C, Any]:
        ...


### Set intersection


class MakeSetIntersection(ABC):
    @abstractmethod
    def intersection(self, components: Sequence[FiniteSet[E]]) -> FiniteSet[E]:
        ...


X = TypeVar("X")


class SetoidOperations(ABC):
    @classmethod
    @abstractmethod
    def union_setoids(cls, a: Setoid[X], b: Setoid[X]) -> Setoid[X]:
        """Creates the union of two Setoids."""

    @classmethod
    @abstractmethod
    def intersection_setoids(cls, a: Setoid[X], b: Setoid[X]) -> Setoid[X]:
        """Creates the intersection of two Setoids."""


class EnumerableSetsOperations(ABC):
    @classmethod
    @abstractmethod
    def make_set_sequence(cls, f: Callable[[int], X]) -> EnumerableSet[X]:
        """Creates an EnumerableSet from a function that gives the
        i-th element."""

    @classmethod
    @abstractmethod
    def union_esets(cls, a: EnumerableSet[X], b: EnumerableSet[X]) -> EnumerableSet[X]:
        """Creates the union of two EnumerableSet."""
