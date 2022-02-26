from abc import ABC, abstractmethod
from typing import Any, Generic, overload, Tuple, TypeVar

from .posets import FinitePoset, Poset

__all__ = [
    "FinitePosetConstructionArrow",
    "FinitePosetConstructionTwisted",
    "PosetOfIntervals",
    "FinitePosetOfIntervals",
    "FinitePosetOfIntervals",
]

C = TypeVar("C")
E = TypeVar("E")


class PosetOfIntervals(Generic[C, E], Poset[E], ABC):
    """A poset of intervals."""

    @abstractmethod
    def construct(self, a: C, b: C) -> E:
        """
        Constructs an interval given the boundaries.

        Must throw ValueError if either a or b is not in the poset,
        or if (a <= b) does not hold.
        """

    @abstractmethod
    def boundaries(self, interval: E) -> Tuple[C, C]:
        """Returns the boundaries of an interval."""


class FinitePosetOfIntervals(Generic[C, E], PosetOfIntervals[C, E], FinitePoset[E], ABC):
    pass


class FinitePosetConstructionTwisted(ABC):
    @abstractmethod
    def twisted(self, s: FinitePoset[C]) -> FinitePosetOfIntervals[C, Any]:
        ...


# @overload
# def twisted(self, s: Poset[C]) -> PosetOfIntervals[C, Any]:
#     ...
#
# @abstractmethod
# def twisted(self, s: Poset[C]) -> PosetOfIntervals[C, Any]:
#     ...


class FinitePosetConstructionArrow(ABC):
    @abstractmethod
    def arrow(self, s: FinitePoset[C]) -> FinitePosetOfIntervals[C, Any]:
        ...


# @overload
# def arrow(self, s: Poset[C]) -> PosetOfIntervals[C, Any]:
#     ...
#
# @abstractmethod
# def arrow(self, s: Poset[C]) -> PosetOfIntervals[C, Any]:
#     ...
