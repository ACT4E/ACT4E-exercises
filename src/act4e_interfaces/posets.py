from abc import ABC, abstractmethod
from typing import List, Optional

from .semigroups import FiniteMonoid
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


class FinitePosetConstructors(ABC):
    @abstractmethod
    def discrete(self, s: FiniteSet) -> FinitePoset:
        """ Creates the discrete poset from any set. """

    @abstractmethod
    def powerset(self, s: FiniteSet) -> FinitePoset:
        """ Creates the powerset poset """

    @abstractmethod
    def uppersets(self, s: FinitePoset) -> FinitePoset:
        """ Creates the upperset poset """

    @abstractmethod
    def lowersets(self, s: FinitePoset) -> FinitePoset:
        """ Creates the lowersets poset """

    @abstractmethod
    def antichains(self, s: FinitePoset) -> FiniteSet:
        """ Creates the antichain set """


class FinitePosetConstruction(ABC):
    @abstractmethod
    def product(self, p1: FinitePoset, p2: FinitePoset) -> FinitePoset:
        ...

    @abstractmethod
    def disjoint_union(self, p1: FinitePoset, p2: FinitePoset) -> FinitePoset:
        ...

    @abstractmethod
    def opposite(self, p: FinitePoset) -> FinitePoset:
        ...

    @abstractmethod
    def twisted(self, s: FinitePoset) -> FinitePoset:
        ...

    @abstractmethod
    def arrow(self, s: FinitePoset) -> FinitePoset:
        ...

    @abstractmethod
    def powerposet(self, s: FinitePoset) -> FinitePoset:
        ...


class MonotoneMap(Mapping, ABC):
    def source_poset(self) -> Poset:
        ...

    def target_poset(self) -> Poset:
        ...


class FiniteMonotoneMapProperties(ABC):
    @abstractmethod
    def is_monotone(self, p1: FinitePoset, p2: FinitePoset, m: FiniteMap) -> bool:
        """ Check if a map is monotone. """

    @abstractmethod
    def is_antitone(self, p1: FinitePoset, p2: FinitePoset, m: FiniteMap) -> bool:
        """ Check if a map is antitone. """


class FiniteMonoidalPoset(ABC):
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


class FiniteLattice(ABC):
    @abstractmethod
    def carrier(self) -> FiniteSet:
        ...
