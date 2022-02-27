from abc import ABC, abstractmethod
from typing import Any, Collection, List, Optional, TypeVar

from .posets import FinitePoset

__all__ = [
    "FinitePosetClosures",
    "FinitePosetMeasurement",
    "FinitePosetSubsetProperties",
    "FinitePosetSubsetProperties2",
    "FinitePosetInfSup",
    "FinitePosetMinMax",
]

C = TypeVar("C")
E = TypeVar("E")


class FinitePosetSubsetProperties(ABC):
    @abstractmethod
    def is_chain(self, fp: FinitePoset[E], s: Collection[E]) -> bool:
        """True if the given elements form a chain.
        Note: s can be any collection, not necessarily ordered.
        """

    @abstractmethod
    def is_antichain(self, fp: FinitePoset[E], s: Collection[E]) -> bool:
        """True if the given elements form an antichain."""


class FinitePosetMeasurement(ABC):
    @abstractmethod
    def width(self, fp: FinitePoset[Any]) -> int:
        """Return the width of the poset."""

    @abstractmethod
    def height(self, fp: FinitePoset[Any]) -> int:
        """Return the height of the poset."""


class FinitePosetMinMax(ABC):
    @abstractmethod
    def minimal(self, fp: FinitePoset[E], S: List[E]) -> List[E]:
        """Return the minimal elements of S"""

    @abstractmethod
    def maximal(self, fp: FinitePoset[E], S: List[E]) -> List[E]:
        """Return the maximal elements of S"""


class FinitePosetInfSup(ABC):
    @abstractmethod
    def lower_bounds(self, fp: FinitePoset[E], s: List[E]) -> List[E]:
        """Computes the lower bounds for the subset (possibly empty)."""

    @abstractmethod
    def upper_bounds(self, fp: FinitePoset[E], s: List[E]) -> Optional[List[E]]:
        """Computes the upper bounds for the subset (possibly empty)."""

    @abstractmethod
    def infimum(self, fp: FinitePoset[E], s: List[E]) -> Optional[E]:
        """Computes the infimum / meet / greatest lower bound
        for the subset, or returns None if one does not exist."""

    @abstractmethod
    def supremum(self, fp: FinitePoset[E], s: List[E]) -> Optional[E]:
        """Computes the supremum for the subset if it exists,
        or returns None if one does not exist."""


class FinitePosetSubsetProperties2(ABC):
    @abstractmethod
    def is_lower_set(self, fp: FinitePoset[E], s: List[E]) -> bool:
        ...

    @abstractmethod
    def is_upper_set(self, fp: FinitePoset[E], s: List[E]) -> bool:
        ...


class FinitePosetClosures(ABC):
    @abstractmethod
    def upper_closure(self, fp: FinitePoset[E], s: List[E]) -> List[E]:
        ...

    @abstractmethod
    def lower_closure(self, fp: FinitePoset[E], s: List[E]) -> List[E]:
        ...
