from abc import ABC, abstractmethod
from typing import Any, Generic, overload, Sequence, Tuple, TypeVar

from .sets import FiniteSet, Setoid

__all__ = ["SetDisjointUnion", "FiniteSetDisjointUnion", "MakeSetDisjointUnion"]

C = TypeVar("C")
E = TypeVar("E")


class SetDisjointUnion(Generic[C, E], Setoid[E], ABC):
    @abstractmethod
    def components(self) -> Sequence[Setoid[C]]:
        """Returns the components of the union"""

    @abstractmethod
    def pack(self, i: int, e: C) -> E:
        """Injection mapping: construct element of the i-th component."""

    @abstractmethod
    def unpack(self, e: E) -> Tuple[int, C]:
        """Returns the index of the component and the element."""


class FiniteSetDisjointUnion(Generic[C, E], FiniteSet[E], SetDisjointUnion[C, E], ABC):
    """Specialization of SetDisjointUnion where we deal with FiniteSets."""

    @abstractmethod
    def components(self) -> Sequence[FiniteSet[C]]:
        ...


class MakeSetDisjointUnion(ABC):
    @overload
    def disjoint_union(self, components: Sequence[FiniteSet[C]]) -> FiniteSetDisjointUnion[C, Any]:
        ...

    @overload
    def disjoint_union(self, components: Sequence[Setoid[C]]) -> SetDisjointUnion[C, Any]:
        ...

    @abstractmethod
    def disjoint_union(self, components: Sequence[Setoid[C]]) -> SetDisjointUnion[C, Any]:
        """Returns a disjoint union of the given components.
        Returns a finite set if all components are finite."""
