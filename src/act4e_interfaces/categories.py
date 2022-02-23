from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, Tuple, TypeVar

from .sets import FiniteSet, Setoid
from .sets_product import FiniteSetProduct, SetProduct
from .sets_sum import SetDisjointUnion

__all__ = [
    "FiniteCategory",
    "FiniteSemiCategory",
    "FiniteCategoryOperations",
    "SemiCategory",
    "SemiBiCategory",
    "Category",
    "CategoryOperations",
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


class SemiBiCategory(Generic[Ob, Mor], ABC):
    @abstractmethod
    def objects(self) -> Setoid[Ob]:
        ...

    @abstractmethod
    def hom(self, ob1: Ob, ob2: Ob) -> Setoid[Mor]:
        ...

    @abstractmethod
    def compose(self, m1: Mor, m2: Mor) -> Mor:
        ...

    @abstractmethod
    def legs(self, m: Mor) -> Tuple[Ob, Ob]:
        """Return source and target of the Mor"""


class SemiCategory(Generic[Ob, Mor], SemiBiCategory[Ob, Mor], ABC):
    ...


class Category(Generic[Ob, Mor], SemiCategory[Ob, Mor], ABC):
    @abstractmethod
    def identity(self, ob: Ob) -> Mor:
        """Identity for the Ob"""


class FiniteSemiCategory(Generic[Ob, Mor], SemiCategory[Ob, Mor], ABC):
    @abstractmethod
    def objects(self) -> FiniteSet[Ob]:
        ...

    @abstractmethod
    def hom(self, ob1: Ob, ob2: Ob) -> FiniteSet[Mor]:
        ...


class FiniteCategory(Generic[Ob, Mor], FiniteSemiCategory[Ob, Mor], Category[Ob, Mor], ABC):
    ...


class CategoryOperations:
    @abstractmethod
    def product(
        self, c1: Category[Ob, Mor], c2: Category[Ob, Mor]
    ) -> Category[SetProduct[Ob, Any], SetProduct[Mor, Any]]:
        """Product of two categories."""

    @abstractmethod
    def disjoint_union(
        self, c1: Category[Ob, Mor], c2: Category[Ob, Mor]
    ) -> Category[SetDisjointUnion[Ob], Any]:  # TODO: better types
        """Disjoint union for the categories"""

    @abstractmethod
    def arrow(self, c1: Category[Ob, Mor]) -> Category[Mor, Any]:  # TODO: better types
        """Computes the arrow category"""

    @abstractmethod
    def twisted(self, c1: Category[Ob, Mor]) -> Category[Mor, Any]:  # TODO: better types
        """Computes the twisted arrow category"""


class FiniteCategoryOperations:
    @abstractmethod
    def product(
        self, c1: Category[Ob, Mor], c2: Category[Ob, Mor]
    ) -> Category[FiniteSetProduct[Any, Ob], FiniteSetProduct[Any, Mor]]:
        """Product of two categories."""

    @abstractmethod
    def disjoint_union(
        self, c1: FiniteCategory[Ob, Mor], c2: FiniteCategory[Ob, Mor]
    ) -> FiniteCategory[Any, Any]:  # TODO: better types

        """Disjoint union for the categories"""

    @abstractmethod
    def arrow(self, c1: FiniteCategory[Ob, Mor]) -> FiniteCategory[Any, Any]:  # TODO: better types
        """Computes the arrow category"""

    @abstractmethod
    def twisted_arrow(self, c1: FiniteCategory[Ob, Mor]) -> FiniteCategory[Any, Any]:  # TODO: better types
        """Computes the twisted arrow category"""
