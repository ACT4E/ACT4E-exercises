from abc import ABC, abstractmethod
from typing import Any, Generic, overload, TypeVar

from .posets import FinitePoset, Poset
from .sets import FiniteSet, Setoid
from .sets_power import FiniteSetOfFiniteSubsets, SetOfFiniteSubsets

__all__ = [
    "FinitePosetConstructionOpposite",
    "PosetOfFiniteSubsets",
    "FinitePosetOfFiniteSubsets",
    "PosetConstructionPower",
]

C = TypeVar("C")
E = TypeVar("E")


class FinitePosetConstructionDiscrete(ABC):
    @overload
    def discrete(self, s: FiniteSet[E]) -> FinitePoset[E]:
        ...

    @overload
    def discrete(self, s: Setoid[E]) -> Poset[E]:
        ...

    @abstractmethod
    def discrete(self, s: Setoid[E]) -> Poset[E]:
        """Creates the discrete poset from any set."""


class PosetOfFiniteSubsets(Generic[C, E], Poset[E], ABC):
    """A poset of subsets."""

    @abstractmethod
    def carrier(self) -> SetOfFiniteSubsets[C, E]:
        ...


class FinitePosetOfFiniteSubsets(Generic[C, E], PosetOfFiniteSubsets[C, E], FinitePoset[E], ABC):
    @abstractmethod
    def carrier(self) -> FiniteSetOfFiniteSubsets[C, E]:
        ...


class PosetConstructionPower(ABC):
    @overload
    def powerposet(self, s: FiniteSet[C]) -> FinitePosetOfFiniteSubsets[C, Any]:
        ...

    @overload
    def powerposet(self, s: Setoid[C]) -> PosetOfFiniteSubsets[C, Any]:
        ...

    @abstractmethod
    def powerposet(self, s: Setoid[C]) -> PosetOfFiniteSubsets[C, Any]:
        ...


class FinitePosetConstructionOpposite(ABC):
    @overload
    def opposite(self, p: FinitePoset[E]) -> FinitePoset[E]:
        ...

    @overload
    def opposite(self, p: Poset[E]) -> Poset[E]:
        ...

    @abstractmethod
    def opposite(self, p: Poset[E]) -> Poset[E]:
        ...
