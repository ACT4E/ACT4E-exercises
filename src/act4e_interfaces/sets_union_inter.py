from abc import ABC, abstractmethod
from typing import Any, Generic, overload, Sequence, TypeVar

from .sets import EnumerableSet, FiniteSet, Setoid

__all__ = [
    "MakeSetIntersection",
    "MakeSetUnion",
    "SetUnion",
    "FiniteSetUnion",
    "EnumerableSetUnion",
    "SetoidOperations",
]

C = TypeVar("C")
E = TypeVar("E")


class MakeSetIntersection(ABC):
    @abstractmethod
    def intersection(self, components: Sequence[FiniteSet[E]]) -> FiniteSet[E]:
        ...


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


class SetoidOperations(ABC):
    @classmethod
    @abstractmethod
    def union_setoids(cls, a: Setoid[E], b: Setoid[E]) -> Setoid[E]:
        """Creates the union of two Setoids."""

    @classmethod
    @abstractmethod
    def intersection_setoids(cls, a: Setoid[E], b: Setoid[E]) -> Setoid[E]:
        """Creates the intersection of two Setoids."""
