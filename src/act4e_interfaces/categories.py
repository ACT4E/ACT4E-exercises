from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, List, NoReturn, TypeVar, Union

from .sets import EnumerableSet, FiniteSet, Setoid
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
    def objects(self) -> EnumerableSet[Ob]:
        ...

    @abstractmethod
    def hom(self, ob1: Ob, ob2: Ob) -> EnumerableSet[Mor]:
        ...

    @abstractmethod
    def compose(self, ob1: Ob, ob2: Ob, ob3: Ob, m1: Mor, m2: Mor) -> Mor:
        ...

    @abstractmethod
    def identity(self, ob: Ob) -> Union[Mor, NoReturn]:
        """Identity for the object. Raises ValueError if there is no identity."""

    # @abstractmethod
    # def legs(self, m: Mor) -> Tuple[Ob, Ob]:
    #     """Return source and target of a morphism"""


class Category(Generic[Ob, Mor], SemiCategory[Ob, Mor], ABC):
    @abstractmethod
    def identity(self, ob: Ob) -> Mor:
        """Identity for the object. Guaranteed to exist."""


class FiniteSemiCategory(Generic[Ob, Mor], SemiCategory[Ob, Mor], ABC):
    @abstractmethod
    def objects(self) -> FiniteSet[Ob]:
        ...

    @abstractmethod
    def hom(self, ob1: Ob, ob2: Ob) -> FiniteSet[Mor]:
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
