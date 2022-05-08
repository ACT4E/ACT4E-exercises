from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, List, Optional, TypeVar

from .sets import EnumerableSet, FiniteSet
from .sets_product import FiniteSetProduct
from .sets_sum import FiniteSetDisjointUnion

__all__ = [
    "FiniteCategory",
    "FiniteSemiCategory",
    "FiniteCategoryOperations",
    "SemiCategory",
    "Category",
]

E1 = TypeVar("E1")
E2 = TypeVar("E2")

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")

O1 = TypeVar("O1")
O2 = TypeVar("O2")

Ob = TypeVar("Ob")
Mor = TypeVar("Mor")

Ob1 = TypeVar("Ob1")
Mor1 = TypeVar("Mor1")
Ob2 = TypeVar("Ob2")
Mor2 = TypeVar("Mor2")
Ob3 = TypeVar("Ob3")
Mor3 = TypeVar("Mor3")


class SemiCategory(Generic[Ob, Mor], ABC):
    @abstractmethod
    def objects(self, uptolevel: Optional[int] = None) -> EnumerableSet[Ob]:
        """Returns the set of objects up to given level (if given)."""

    @abstractmethod
    def hom(self, ob1: Ob, ob2: Ob, uptolevel: Optional[int] = None) -> EnumerableSet[Mor]:
        """Returns the homset of up to given level (if given)."""

    @abstractmethod
    def compose(self, ob1: Ob, ob2: Ob, ob3: Ob, m1: Mor, m2: Mor) -> Mor:
        """Equivalent to the ; operator."""
        ...

    @abstractmethod
    def identity(self, ob: Ob) -> Mor:
        """Identity for the object. Raises I.InvalidValue if there is no identity for ob."""


class Category(Generic[Ob, Mor], SemiCategory[Ob, Mor], ABC):
    @abstractmethod
    def identity(self, ob: Ob) -> Mor:
        """Identity for the object. Guaranteed to exist."""


class FiniteSemiCategory(Generic[Ob, Mor], SemiCategory[Ob, Mor], ABC):
    @abstractmethod
    def objects(self, uptolevel: Optional[int] = None) -> FiniteSet[Ob]:
        ...

    @abstractmethod
    def hom(self, ob1: Ob, ob2: Ob, uptolevel: Optional[int] = None) -> FiniteSet[Mor]:
        ...


class FiniteCategory(Generic[Ob, Mor], FiniteSemiCategory[Ob, Mor], Category[Ob, Mor], ABC):
    ...


#
# class CategoryOperations:
#     @abstractmethod
#     def product(
#         self, c1: Category[Ob, Mor], c2: Category[Ob, Mor]
#     ) -> Category[SetProduct[Ob, Any], SetProduct[Mor, Any]]:
#         """Product of two categories."""
#
#     @abstractmethod
#     def disjoint_union(
#         self, c1: Category[Ob, Mor], c2: Category[Ob, Mor]
#     ) -> Category[SetDisjointUnion[Ob, Any], Any]:  # TODO: better types
#         """Disjoint union for the categories"""
#
#     @abstractmethod
#     def arrow(self, c1: Category[Ob, Mor]) -> Category[Mor, Any]:  # TODO: better types
#         """Computes the arrow category"""
#
#     @abstractmethod
#     def twisted(self, c1: Category[Ob, Mor]) -> Category[Mor, Any]:  # TODO: better types
#         """Computes the twisted arrow category"""


class FiniteCategoryOperations:
    @abstractmethod
    def product(
        self, components: List[FiniteSemiCategory[Ob, Mor]]
    ) -> FiniteSemiCategory[FiniteSetProduct[Any, Ob], FiniteSetProduct[Any, Mor]]:
        """Product of categories."""

    @abstractmethod
    def disjoint_union(
        self, c1: FiniteSemiCategory[Ob, Mor], c2: FiniteSemiCategory[Ob, Mor]
    ) -> FiniteSemiCategory[
        FiniteSetDisjointUnion[Ob, Any], FiniteSetDisjointUnion[Ob, Any]
    ]:  # TODO: better types

        """Disjoint union of the categories"""

    @abstractmethod
    def arrow(
        self, c1: FiniteSemiCategory[Ob, Mor]
    ) -> FiniteSemiCategory[Mor, FiniteSetProduct[Mor]]:  # TODO: better types
        """Computes the arrow category"""

    @abstractmethod
    def twisted_arrow(
        self, c1: FiniteSemiCategory[Ob, Mor]
    ) -> FiniteSemiCategory[Mor, FiniteSetProduct[Mor]]:  # TODO: better types
        """Computes the twisted arrow category"""
