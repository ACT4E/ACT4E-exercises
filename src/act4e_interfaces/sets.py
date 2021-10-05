from abc import ABC, abstractmethod
from typing import Iterator, List, overload

from .helper import IOHelper
from .types import ConcreteRepr, Element


class Setoid(ABC):
    """
    A setoid is something to which elements may belong,
    has a way of distinguishing elements,
    and is able to (de)serialize its elements.
    """

    @abstractmethod
    def contains(self, x: Element) -> bool:
        """ Returns true if the element is in the set. """

    def equal(self, x: Element, y: Element) -> bool:
        """ Returns True if the two elements are to be considered equal. """
        return x == y  # default is to use the Python equality

    def apart(self, x: Element, y: Element) -> bool:
        return not self.equal(x, y)

    @abstractmethod
    def save(self, h: IOHelper, x: Element) -> ConcreteRepr:
        ...

    @abstractmethod
    def load(self, h: IOHelper, o: ConcreteRepr) -> Element:
        ...


class Mapping(ABC):
    @abstractmethod
    def source(self) -> Setoid:
        ...

    @abstractmethod
    def target(self) -> Setoid:
        ...

    @abstractmethod
    def __call__(self, a: Element) -> Element:
        ...


class EnumerableSet(Setoid, ABC):
    @abstractmethod
    def elements(self) -> Iterator[Element]:
        """ Note: possibly non-terminating. """


class FiniteSet(EnumerableSet, ABC):
    """ A finite set has a finite size. """

    @abstractmethod
    def size(self) -> int:
        """ Return the size of the finite set. """


class FiniteMap(Mapping, ABC):
    @abstractmethod
    def source(self) -> FiniteSet:
        ...

    @abstractmethod
    def target(self) -> FiniteSet:
        ...


class FiniteSetProperties(ABC):
    @abstractmethod
    def is_subset(self, a: FiniteSet, b: FiniteSet) -> bool:
        """ True if `a` is a subset of `b`. """

    def equal(self, a: FiniteSet, b: FiniteSet) -> bool:
        return self.is_subset(a, b) and self.is_subset(b, a)

    def is_strict_subset(self, a: FiniteSet, b: FiniteSet) -> bool:
        return self.is_subset(a, b) and not self.is_subset(b, a)


class SetProduct(Setoid, ABC):
    """ A set product is a setoid that can be factorized. """

    @abstractmethod
    def components(self) -> List[Setoid]:
        """ Returns the components of the product"""

    @abstractmethod
    def pack(self, *args: Element) -> Element:
        """ Packs an element of each setoid into an element of the mapping"""

    @abstractmethod
    def projections(self) -> List[Mapping]:
        """ Returns the projection mappings. """


class FiniteSetProduct(FiniteSet, SetProduct, ABC):
    """ Specialization of SetProduct where we deal with FiniteSets"""

    @abstractmethod
    def components(self) -> List[FiniteSet]:
        """ Returns the components """

    @abstractmethod
    def projections(self) -> List[FiniteMap]:
        """ Returns the projection mappings. """


class SetUnion(Setoid, ABC):
    """ A set product is a setoid that can be factorized. """

    @abstractmethod
    def components(self) -> List[Setoid]:
        """ Returns the components of the union"""


class FiniteSetPowerSet(ABC):
    @abstractmethod
    def powerset(self, s: FiniteSet) -> FiniteSet:
        """ Creates the powerset  """


class EnumerableSetUnion(EnumerableSet, SetUnion, ABC):
    """ Specialization of SetUnion where we deal with FiniteSets"""

    @abstractmethod
    def components(self) -> List[EnumerableSet]:
        """ Returns the components of the union """


class FiniteSetUnion(FiniteSet, EnumerableSetUnion, ABC):
    """ Specialization of SetUnion where we deal with FiniteSets"""

    @abstractmethod
    def components(self) -> List[FiniteSet]:
        """ Returns the components of the union """


class SetDisjointUnion(Setoid, ABC):
    @abstractmethod
    def components(self) -> List[Setoid]:
        """ Returns the components of the union """

    @abstractmethod
    def injections(self) -> List[Mapping]:
        """ Returns the projection mappings. """


class FiniteSetDisjointUnion(FiniteSet, SetDisjointUnion, ABC):
    """ Specialization of SetProduct where we deal with FiniteSets"""

    @abstractmethod
    def components(self) -> List[FiniteSet]:
        ...

    @abstractmethod
    def injections(self) -> List[FiniteMap]:
        ...


class MakeSetProduct(ABC):
    @overload
    def product(self, components: List[Setoid]) -> SetProduct:
        ...

    @abstractmethod
    def product(self, components: List[FiniteSet]) -> FiniteSetProduct:
        ...


class MakeSetIntersection(ABC):
    @abstractmethod
    def intersection(self, components: List[FiniteSet]) -> FiniteSet:
        ...


class MakeSetUnion(ABC):
    @overload
    def union(self, components: List[FiniteSet]) -> FiniteSetUnion:
        ...

    @overload
    def union(self, components: List[EnumerableSet]) -> EnumerableSetUnion:
        ...

    @abstractmethod
    def union(self, components: List[Setoid]) -> SetUnion:
        ...


class MakeSetDisjointUnion(ABC):
    @overload
    def compute_disjoint_union(self, components: List[Setoid]) -> SetDisjointUnion:
        ...

    @abstractmethod
    def compute_disjoint_union(self, components: List[FiniteSet]) -> FiniteSetDisjointUnion:
        ...
