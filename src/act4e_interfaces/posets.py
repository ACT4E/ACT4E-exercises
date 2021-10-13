from abc import ABC, abstractmethod
from typing import Generic, List, Optional, overload, Tuple

from .semigroups import FiniteMonoid, Monoid
from .sets import (
    C,
    E,
    E1,
    E2,
    FiniteMap,
    FiniteSet,
    FiniteSetDisjointUnion,
    Mapping,
    SetDisjointUnion,
    SetOfFiniteSubsets,
    Setoid,
    SetProduct,
)


# __all__ = ['Poset', 'FinitePoset']


class Poset(Generic[E], ABC):
    @abstractmethod
    def carrier(self) -> Setoid[E]:
        ...

    @abstractmethod
    def holds(self, a: E, b: E) -> bool:
        ...


class FinitePoset(Poset[E], ABC):
    """ Implementation of finite posets. """

    @abstractmethod
    def carrier(self) -> FiniteSet[E]:
        ...


class FinitePosetSubsetProperties(ABC):
    @abstractmethod
    def is_chain(self, fp: FinitePoset[E], s: List[E]) -> bool:
        """ True if the given elements form a chain. """

    @abstractmethod
    def is_antichain(self, fp: FinitePoset[E], s: List[E]) -> bool:
        """ True if the given elements form an antichain. """


class FinitePosetMeasurement(ABC):
    @abstractmethod
    def width(self, fp: FinitePoset[E]) -> int:
        """ Return the width of the poset. """

    @abstractmethod
    def height(self, fp: FinitePoset[E]) -> int:
        """ Return the height of the poset. """


class FinitePosetMinMax(ABC):
    @abstractmethod
    def miminal(self, fp: FinitePoset[E], S: List[E]) -> List[E]:
        """ Return the minimal elements of S """

    @abstractmethod
    def maximal(self, fp: FinitePoset[E], S: List[E]) -> List[E]:
        """ Return the maximal elements of S """


class FinitePosetInfSup(ABC):
    @abstractmethod
    def lower_bounds(self, fp: FinitePoset[E], s: List[E]) -> List[E]:
        """ Computes the lower bounds for the subset"""

    @abstractmethod
    def infimum(self, fp: FinitePoset[E], s: List[E]) -> Optional[E]:
        """Computes the infimum / meet / greatest lower bound
        for the subset, or returns None if one does not exist."""

    @abstractmethod
    def upper_bounds(self, fp: FinitePoset[E], s: List[E]) -> List[E]:
        """ Computes the upper bounds for the subset. """

    @abstractmethod
    def supremum(self, fp: FinitePoset[E], s: List[E]) -> Optional[E]:
        """Computes the supremum for the subset if it exists,
        or returns None if one does not exist."""


class FinitePosetSubsetProperties2(ABC):
    @abstractmethod
    def is_lower_set(self, fp: FinitePoset[E], s: List[E]) -> bool:
        pass

    @abstractmethod
    def is_upper_set(self, fp: FinitePoset[E], s: List[E]) -> bool:
        pass


class FinitePosetClosures(ABC):
    @abstractmethod
    def upper_closure(self, fp: FinitePoset[E], s: List[E]) -> List[E]:
        pass

    @abstractmethod
    def lower_closure(self, fp: FinitePoset[E], s: List[E]) -> List[E]:
        pass


### Discrete


class FinitePosetConstructionDiscrete(ABC):
    @overload
    def discrete(self, s: Setoid[E]) -> Poset[E]:
        """ Creates the discrete poset from any set. """

    @abstractmethod
    def discrete(self, s: FiniteSet[E]) -> FinitePoset[E]:
        """ Creates the discrete poset from any set. """


### Subset


class PosetOfFiniteSubsets(Generic[C, E], Poset[E], ABC):
    """ A poset of subsets. """

    @abstractmethod
    def carrier(self) -> SetOfFiniteSubsets[C, E]:
        ...


class FinitePosetOfFiniteSubsets(Generic[C, E], PosetOfFiniteSubsets[C, E], FinitePoset[E], ABC):
    pass


class PosetConstructionPower(ABC):
    @overload
    def powerposet(self, s: Poset[C]) -> PosetOfFiniteSubsets[C, E]:
        ...

    @abstractmethod
    def powerposet(self, s: FinitePoset[C]) -> FinitePosetOfFiniteSubsets[C, E]:
        ...


## Product


class PosetProduct(Generic[C, E], Poset[E], ABC):
    """ A poset product is a poset that can be factorized. """

    @abstractmethod
    def carrier(self) -> SetProduct[C, E]:
        """ Returns the components of the product"""

    @abstractmethod
    def components(self) -> List[Poset[C]]:
        """ Returns the components of the product"""

    @abstractmethod
    def pack(self, args: List[C]) -> E:
        """ Packs an element of each setoid into an element of the mapping"""

    @abstractmethod
    def unpack(self, e: E) -> List[C]:
        ...


class FinitePosetProduct(Generic[C, E], FiniteSet[E], PosetProduct[C, E], ABC):
    """ Specialization of PosetProduct where we deal with FinitePosets"""

    @abstractmethod
    def components(self) -> List[FinitePoset[C]]:
        """ Returns the components """


class FinitePosetConstructionProduct(ABC):
    @abstractmethod
    def product(self, ps: List[FinitePoset[C]]) -> FinitePoset[E]:
        ...


## Disjoint union


class PosetDisjointUnion(Generic[C, E], Poset[E], ABC):
    """ A set product is a setoid that can be factorized in a sum. """

    @abstractmethod
    def carrier(self) -> SetDisjointUnion[C, E]:
        """ Returns the components of the product"""

    @abstractmethod
    def components(self) -> List[Poset[C]]:
        """ Returns the components of the union"""


class FinitePosetDisjointUnion(Generic[C, E], PosetDisjointUnion[C, E], ABC):
    """ Specialization of SetUnion where we deal with FiniteSets"""

    @abstractmethod
    def carrier(self) -> FiniteSetDisjointUnion[C, E]:
        """ Returns the components of the product"""

    @abstractmethod
    def components(self) -> List[FinitePoset[C]]:
        """ Returns the components of the union """


class FinitePosetConstructionSum(ABC):
    @overload
    def disjoint_union(self, ps: List[Poset[C]]) -> PosetDisjointUnion[C, E]:
        ...

    @abstractmethod
    def disjoint_union(self, ps: List[FinitePoset[C]]) -> FinitePosetDisjointUnion[C, E]:
        ...


### Opposite


class FinitePosetConstructionOpposite(ABC):
    @overload
    def opposite(self, p: Poset[E]) -> Poset[E]:
        ...

    @abstractmethod
    def opposite(self, p: FinitePoset[E]) -> FinitePoset[E]:
        ...


### Interval


class PosetOfIntervals(Generic[C, E], Poset[E], ABC):
    """ A poset of intervals. """

    def construct(self, a: C, b: C) -> E:
        """ Constructs an interval given the boundaries. """

    def boundaries(self, interval: E) -> Tuple[C, C]:
        """ Returns the boundaries of an interval."""


class FinitePosetOfIntervals(Generic[C, E], PosetOfIntervals[C, E], FinitePoset[E], ABC):
    pass


class FinitePosetConstructionTwisted(ABC):
    @overload
    def twisted(self, s: Poset[C]) -> PosetOfIntervals[C, E]:
        ...

    @abstractmethod
    def twisted(self, s: FinitePoset[C]) -> FinitePosetOfIntervals[C, E]:
        ...


class FinitePosetConstructionArrow(ABC):
    @overload
    def arrow(self, s: Poset[C]) -> PosetOfIntervals[C, E]:
        ...

    @abstractmethod
    def arrow(self, s: FinitePoset[C]) -> FinitePosetOfIntervals[C, E]:
        ...


class MonotoneMap(Generic[E1, E2], Mapping[E1, E2], ABC):
    def source_poset(self) -> Poset[E1]:
        ...

    def target_poset(self) -> Poset[E2]:
        ...


class FiniteMonotoneMap(Generic[E1, E2], MonotoneMap[E1, E2], ABC):
    def source_poset(self) -> FinitePoset[E1]:
        ...

    def target_poset(self) -> FinitePoset[E2]:
        ...


class FiniteMonotoneMapProperties(ABC):
    @abstractmethod
    def is_monotone(self, p1: FinitePoset[E1], p2: FinitePoset[E2], m: FiniteMap[E1, E2]) -> bool:
        """ Check if a map is monotone. """

    @abstractmethod
    def is_antitone(self, p1: FinitePoset[E1], p2: FinitePoset[E2], m: FiniteMap[E1, E2]) -> bool:
        """ Check if a map is antitone. """


class MonoidalPoset(Generic[E], ABC):
    """ Implementation of finite posets. """

    @abstractmethod
    def poset(self) -> Poset[E]:
        ...

    @abstractmethod
    def monoid(self) -> Monoid[E]:
        ...


class FiniteMonoidalPoset(Generic[E], MonoidalPoset[E], ABC):
    """ Implementation of finite posets. """

    @abstractmethod
    def poset(self) -> FinitePoset[E]:
        ...

    @abstractmethod
    def monoid(self) -> FiniteMonoid[E]:
        ...


class MonoidalPosetOperations(ABC):
    """ Implementation of finite posets. """

    @abstractmethod
    def is_monoidal_poset(self, fp: FinitePoset[E], fm: FiniteMonoid[E]) -> bool:
        """ Check that the pair of poset and monoid make together a monoidal poset."""


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
