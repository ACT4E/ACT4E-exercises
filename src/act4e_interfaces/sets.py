from abc import ABC, abstractmethod
from typing import Generic, Iterator, List, overload, Tuple, TypeVar

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
        """ Returns true if the element is in the set. """

    def equal(self, x: E, y: E) -> bool:
        """ Returns True if the two elements are to be considered equal. """
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
        """ Note: possibly non-terminating. """


class FiniteSet(EnumerableSet[E], ABC):
    """ A finite set has a finite size. """

    @abstractmethod
    def size(self) -> int:
        """ Return the size of the finite set. """


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
        """ True if `a` is a subset of `b`. """

    def equal(self, a: FiniteSet[E], b: FiniteSet[E]) -> bool:
        return self.is_subset(a, b) and self.is_subset(b, a)

    def is_strict_subset(self, a: FiniteSet[E], b: FiniteSet[E]) -> bool:
        return self.is_subset(a, b) and not self.is_subset(b, a)


### Set product

C = TypeVar("C")


class SetProduct(Generic[C, E], Setoid[E], ABC):
    """ A set product is a setoid that can be factorized. """

    @abstractmethod
    def components(self) -> List[Setoid[E]]:
        """ Returns the components of the product"""

    @abstractmethod
    def pack(self, args: List[C]) -> E:
        """ Packs an element of each setoid into an element of the mapping"""

    @abstractmethod
    def unpack(self, args: E) -> List[C]:
        """ Packs an element of each setoid into an element of the mapping"""


class FiniteSetProduct(FiniteSet[E], SetProduct[C, E], ABC):
    """ Specialization of SetProduct where we deal with FiniteSets"""

    @abstractmethod
    def components(self) -> List[FiniteSet[E]]:
        """ Returns the components """


class MakeSetProduct(ABC):
    @overload
    def product(self, components: List[Setoid[E]]) -> SetProduct[C, E]:
        ...

    @abstractmethod
    def product(self, components: List[FiniteSet[E]]) -> FiniteSetProduct[C, E]:
        ...


## Set union


class SetUnion(Generic[C, E], Setoid[E], ABC):
    """ A set product is a setoid that can be factorized. """

    @abstractmethod
    def components(self) -> List[Setoid[C]]:
        """ Returns the components of the union"""


class EnumerableSetUnion(Generic[C, E], EnumerableSet[E], SetUnion[C, E], ABC):
    """ Specialization of SetUnion where we deal with FiniteSets"""

    @abstractmethod
    def components(self) -> List[EnumerableSet[C]]:
        """ Returns the components of the union """


class FiniteSetUnion(Generic[C, E], FiniteSet[E], EnumerableSetUnion[C, E], ABC):
    """ Specialization of SetUnion where we deal with FiniteSets"""

    @abstractmethod
    def components(self) -> List[FiniteSet[C]]:
        """ Returns the components of the union """


class MakeSetUnion(ABC):
    @overload
    def union(self, components: List[FiniteSet[C]]) -> FiniteSetUnion[C, E]:
        ...

    @overload
    def union(self, components: List[EnumerableSet[C]]) -> EnumerableSetUnion[C, E]:
        ...

    @abstractmethod
    def union(self, components: List[Setoid[C]]) -> SetUnion[C, E]:
        ...


### Power set


class SetOfFiniteSubsets(Generic[C, E], Setoid[E], ABC):
    """ A set of subsets. """

    @abstractmethod
    def contents(self, e: E) -> Iterator[C]:
        """ Returns the contents of an element represeting a subset."""

    @abstractmethod
    def construct(self, elements: List[C]) -> E:
        """ Get the element representing the given subset."""


class FiniteSetOfFiniteSubsets(Generic[C, E], SetOfFiniteSubsets[C, E], FiniteSet[E], ABC):
    pass


class MakePowerSet(ABC):
    @overload
    def powerset(self, s: Setoid[C]) -> SetOfFiniteSubsets[C, E]:
        ...

    @abstractmethod
    def powerset(self, s: FiniteSet[C]) -> FiniteSetOfFiniteSubsets[C, E]:
        """ Creates the powerset of a finite set. """


### disjoint union


class SetDisjointUnion(Generic[C, E], Setoid[E], ABC):
    @abstractmethod
    def components(self) -> List[Setoid[C]]:
        """ Returns the components of the union """

    def pack(self, i: int, e: C) -> E:
        """ Injection mapping. """

    def unpack(self, e: E) -> Tuple[int, C]:
        ...


class FiniteSetDisjointUnion(Generic[C, E], FiniteSet[E], SetDisjointUnion[C, E], ABC):
    """ Specialization of SetDisjointUnion where we deal with FiniteSets. """

    @abstractmethod
    def components(self) -> List[FiniteSet[C]]:
        ...


class MakeSetDisjointUnion(ABC):
    @overload
    def disjoint_union(self, components: List[Setoid[C]]) -> SetDisjointUnion[C, E]:
        ...

    @abstractmethod
    def disjoint_union(self, components: List[FiniteSet[C]]) -> FiniteSetDisjointUnion[C, E]:
        ...


### Set intersection


class MakeSetIntersection(ABC):
    @abstractmethod
    def intersection(self, components: List[FiniteSet[C]]) -> FiniteSet[C]:
        ...
