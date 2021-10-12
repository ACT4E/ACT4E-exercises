from abc import ABC, abstractmethod
from typing import Iterator, List, Optional, Tuple

from .semigroups import FiniteMonoid, Monoid
from .sets import FiniteMap, FiniteSet, Mapping, Setoid
from .types import Element

# __all__ = ['Poset', 'FinitePoset']


class Poset(ABC):
    @abstractmethod
    def carrier(self) -> Setoid:
        ...

    @abstractmethod
    def holds(self) -> Mapping:
        ...


class FinitePoset(Poset, ABC):
    """ Implementation of finite posets. """

    @abstractmethod
    def carrier(self) -> FiniteSet:
        ...

    @abstractmethod
    def holds(self) -> FiniteMap:
        ...


class FinitePosetSubsetProperties(ABC):
    @abstractmethod
    def is_chain(self, fp: FinitePoset, s: List[Element]) -> bool:
        """ True if the given elements form a chain. """

    @abstractmethod
    def is_antichain(self, fp: FinitePoset, s: List[Element]) -> bool:
        """ True if the given elements form an antichain. """


class FinitePosetMeasurement(ABC):
    @abstractmethod
    def width(self, fp: FinitePoset) -> int:
        """ Return the width of the poset. """

    @abstractmethod
    def height(self, fp: FinitePoset) -> int:
        """ Return the height of the poset. """


class FinitePosetMinMax(ABC):
    @abstractmethod
    def miminal(self, fp: FinitePoset, S: List[Element]) -> List[Element]:
        """ Return the minimal elements of S """

    @abstractmethod
    def maximal(self, fp: FinitePoset, S: List[Element]) -> List[Element]:
        """ Return the maximal elements of S """


class FinitePosetInfSup(ABC):
    @abstractmethod
    def lower_bounds(self, fp: FinitePoset, s: List[Element]) -> List[Element]:
        """ Computes the lower bounds for the subset"""

    @abstractmethod
    def infimum(self, fp: FinitePoset, s: List[Element]) -> Optional[Element]:
        """Computes the infimum / meet / greatest lower bound
        for the subset, or returns None if one does not exist."""

    @abstractmethod
    def upper_bounds(self, fp: FinitePoset, s: List[Element]) -> List[Element]:
        """ Computes the upper bounds for the subset. """

    @abstractmethod
    def supremum(self, fp: FinitePoset, s: List[Element]) -> Optional[Element]:
        """Computes the supremum for the subset if it exists,
        or returns None if one does not exist."""


class FinitePosetSubsetProperties2(ABC):
    @abstractmethod
    def is_lower_set(self, fp: FinitePoset, s: List[Element]) -> bool:
        pass

    @abstractmethod
    def is_upper_set(self, fp: FinitePoset, s: List[Element]) -> bool:
        pass


class FinitePosetClosures(ABC):
    @abstractmethod
    def upper_closure(self, fp: FinitePoset, s: List[Element]) -> List[Element]:
        pass

    @abstractmethod
    def lower_closure(self, fp: FinitePoset, s: List[Element]) -> List[Element]:
        pass


class FinitePosetConstructionDiscrete(ABC):
    @abstractmethod
    def discrete(self, s: FiniteSet) -> FinitePoset:
        """ Creates the discrete poset from any set. """


class SubsetPoset(Poset, ABC):
    """ A poset of subsets. """

    def contents(self, e: Element) -> Iterator[Element]:
        """ Returns the contents of a subset"""


class FiniteSubsetPoset(SubsetPoset, FinitePoset, ABC):
    def construct(self, elements: List[Element]) -> Element:
        """ Given a list of elements, builds the element that represents the poset."""
        pass


class FinitePosetConstructionPower(ABC):
    @abstractmethod
    def powerposet(self, s: FinitePoset) -> FiniteSubsetPoset:
        ...


class PosetProduct(Poset, ABC):
    """ A poset product is a poset that can be factorized. """

    @abstractmethod
    def components(self) -> List[Poset]:
        """ Returns the components of the product"""

    @abstractmethod
    def projections(self) -> List[Mapping]:
        """ Returns the projection mappings. """

    @abstractmethod
    def pack(self, args: List[Element]) -> Element:
        """ Packs an element of each setoid into an element of the mapping"""

    @abstractmethod
    def unpack(self, e: Element) -> List[Element]:
        ...


class FinitePosetProduct(FiniteSet, PosetProduct, ABC):
    """ Specialization of PosetProduct where we deal with FinitePosets"""

    @abstractmethod
    def components(self) -> List[FinitePoset]:
        """ Returns the components """

    @abstractmethod
    def projections(self) -> List[FiniteMap]:
        """ Returns the projection mappings. """


class FinitePosetConstructionProduct(ABC):
    @abstractmethod
    def product(self, ps: List[FinitePoset]) -> FinitePoset:
        ...


class PosetSum(Poset, ABC):
    """ A set product is a setoid that can be factorized in a sum. """

    @abstractmethod
    def components(self) -> List[Poset]:
        """ Returns the components of the union"""


class FinitePosetSum(PosetSum, ABC):
    """ Specialization of SetUnion where we deal with FiniteSets"""

    @abstractmethod
    def components(self) -> List[FinitePoset]:
        """ Returns the components of the union """


class FinitePosetConstructionSum(ABC):
    @abstractmethod
    def disjoint_union(self, ps: List[FinitePoset]) -> FinitePosetSum:
        ...


class FinitePosetConstructionOpposite(ABC):
    @abstractmethod
    def opposite(self, p: FinitePoset) -> FinitePoset:
        ...


class IntervalPoset(Poset, ABC):
    """ A poset of intervals. """

    def construct(self, a: Element, b: Element) -> Element:
        """ Constructs an interval given the boundaries. """

    def boundaries(self, interval: Element) -> Tuple[Element, Element]:
        """ Returns the boundaries of an interval."""


class FiniteIntervalPoset(IntervalPoset, FinitePoset, ABC):
    pass


class FinitePosetConstructionTwisted(ABC):
    @abstractmethod
    def twisted(self, s: FinitePoset) -> FiniteIntervalPoset:
        ...


class FinitePosetConstructionArrow(ABC):
    @abstractmethod
    def arrow(self, s: FinitePoset) -> FiniteIntervalPoset:
        ...


class MonotoneMap(Mapping, ABC):
    def source_poset(self) -> Poset:
        ...

    def target_poset(self) -> Poset:
        ...


class FiniteMonotoneMap(Mapping, ABC):
    def source_poset(self) -> FinitePoset:
        ...

    def target_poset(self) -> FinitePoset:
        ...


class FiniteMonotoneMapProperties(ABC):
    @abstractmethod
    def is_monotone(self, p1: FinitePoset, p2: FinitePoset, m: FiniteMap) -> bool:
        """ Check if a map is monotone. """

    @abstractmethod
    def is_antitone(self, p1: FinitePoset, p2: FinitePoset, m: FiniteMap) -> bool:
        """ Check if a map is antitone. """


class MonoidalPoset(ABC):
    """ Implementation of finite posets. """

    @abstractmethod
    def poset(self) -> Poset:
        ...

    @abstractmethod
    def monoid(self) -> Monoid:
        ...


class FiniteMonoidalPoset(MonoidalPoset, ABC):
    """ Implementation of finite posets. """

    @abstractmethod
    def poset(self) -> FinitePoset:
        ...

    @abstractmethod
    def monoid(self) -> FiniteMonoid:
        ...


class MonoidalPosetOperations(ABC):
    """ Implementation of finite posets. """

    @abstractmethod
    def is_monoidal_poset(self, fp: FinitePoset, fm: FiniteMonoid) -> bool:
        """ Check that the pair of poset and monoid make together a monoidal poset."""


class MeetSemilattice(Poset, ABC):
    @abstractmethod
    def meet(self, x: Element, y: Element) -> Element:
        ...

    @abstractmethod
    def top(self) -> Element:
        ...


class JoinSemilattice(Poset, ABC):
    @abstractmethod
    def join(self, x: Element, y: Element) -> Element:
        ...

    @abstractmethod
    def bottom(self) -> Element:
        ...


class Lattice(JoinSemilattice, MeetSemilattice, ABC):
    ...


class FiniteLattice(Lattice, ABC):
    @abstractmethod
    def carrier(self) -> FiniteSet:
        ...
