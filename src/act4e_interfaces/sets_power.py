from abc import ABC, abstractmethod
from typing import Any, Generic, Iterator, overload, Sequence, TypeVar

from .sets import FiniteSet, Setoid

__all__ = ["MakePowerSet", "SetOfFiniteSubsets", "FiniteSetOfFiniteSubsets", "SetOfFiniteSubsets"]

C = TypeVar("C")
E = TypeVar("E")


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
        """Creates the powerset of a setoid. Returns a finite set if s is finite."""
