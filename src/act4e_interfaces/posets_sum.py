from abc import ABC, abstractmethod
from typing import Any, Generic, overload, Sequence, TypeVar

from .posets import FinitePoset, Poset
from .sets_sum import (
    FiniteSetDisjointUnion,
    SetDisjointUnion,
)

__all__ = [
    "FinitePosetConstructionSum",
    "FinitePosetDisjointUnion",
    "PosetDisjointUnion",
]

E = TypeVar("E")
C = TypeVar("C")


class PosetDisjointUnion(Generic[C, E], Poset[E], ABC):
    @abstractmethod
    def carrier(self) -> SetDisjointUnion[C, E]:
        ...

    @abstractmethod
    def components(self) -> Sequence[Poset[C]]:
        ...


class FinitePosetDisjointUnion(Generic[C, E], FinitePoset[E], PosetDisjointUnion[C, E], ABC):
    """Specialization of PosetDisjointUnion where we deal with FiniteSets"""

    @abstractmethod
    def carrier(self) -> FiniteSetDisjointUnion[C, E]:
        ...

    @abstractmethod
    def components(self) -> Sequence[FinitePoset[C]]:
        ...


class FinitePosetConstructionSum(ABC):
    @abstractmethod
    def disjoint_union(self, ps: Sequence[FinitePoset[C]]) -> FinitePosetDisjointUnion[C, Any]:
        ...


# @overload
# def disjoint_union(self, ps: Sequence[Poset[C]]) -> PosetDisjointUnion[C, Any]:
#     ...
#
# @abstractmethod
# def disjoint_union(self, ps: Sequence[Poset[C]]) -> PosetDisjointUnion[C, Any]:
#     ...
