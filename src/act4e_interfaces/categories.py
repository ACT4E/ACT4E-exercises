from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, Tuple, TypeVar

from .sets import FiniteSet, Setoid
from .sets_product import FiniteSetProduct, SetProduct

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

Object = TypeVar("Object")
Morphism = TypeVar("Morphism")

Object1 = TypeVar("Object1")
Morphism1 = TypeVar("Morphism1")
Object2 = TypeVar("Object2")
Morphism2 = TypeVar("Morphism2")
Object3 = TypeVar("Object3")
Morphism3 = TypeVar("Morphism3")


class SemiBiCategory(Generic[Object, Morphism], ABC):
    @abstractmethod
    def objects(self) -> Setoid[Object]:
        ...

    @abstractmethod
    def hom(self, ob1: Object, ob2: Object) -> Setoid[Morphism]:
        ...

    @abstractmethod
    def compose(self, m1: Morphism, m2: Morphism) -> Morphism:
        ...

    @abstractmethod
    def legs(self, m: Morphism) -> Tuple[Object, Object]:
        """Return source and target of the morphism"""


class SemiCategory(Generic[Object, Morphism], SemiBiCategory[Object, Morphism], ABC):
    ...


class Category(Generic[Object, Morphism], SemiCategory[Object, Morphism], ABC):
    @abstractmethod
    def identity(self, ob: Object) -> Morphism:
        """Identity for the object"""


class FiniteSemiCategory(Generic[Object, Morphism], SemiCategory[Object, Morphism], ABC):
    @abstractmethod
    def objects(self) -> FiniteSet[Object]:
        ...

    @abstractmethod
    def hom(self, ob1: Object, ob2: Object) -> FiniteSet[Morphism]:
        ...


class FiniteCategory(
    Generic[Object, Morphism], FiniteSemiCategory[Object, Morphism], Category[Object, Morphism], ABC
):
    ...


class CategoryOperations:
    @abstractmethod
    def product(
        self, c1: Category[Object, Morphism], c2: Category[Object, Morphism]
    ) -> Category[SetProduct[Any, Object], SetProduct[Any, Morphism]]:
        """Product of two categories."""

    @abstractmethod
    def disjoint_union(
        self, c1: Category[Object, Morphism], c2: Category[Object, Morphism]
    ) -> Category[Any, Any]:  # TODO: better types
        """Disjoint union for the categories"""

    @abstractmethod
    def arrow(self, c1: Category[Object, Morphism]) -> Category[Any, Any]:  # TODO: better types
        """Computes the arrow category"""

    @abstractmethod
    def twisted(self, c1: Category[Object, Morphism]) -> Category[Any, Any]:  # TODO: better types
        """Computes the twisted arrow category"""


class FiniteCategoryOperations:
    @abstractmethod
    def product(
        self, c1: Category[Object, Morphism], c2: Category[Object, Morphism]
    ) -> Category[FiniteSetProduct[Any, Object], FiniteSetProduct[Any, Morphism]]:
        """Product of two categories."""

    @abstractmethod
    def disjoint_union(
        self, c1: FiniteCategory[Object, Morphism], c2: FiniteCategory[Object, Morphism]
    ) -> FiniteCategory[Any, Any]:  # TODO: better types

        """Disjoint union for the categories"""

    @abstractmethod
    def arrow(self, c1: FiniteCategory[Object, Morphism]) -> FiniteCategory[Any, Any]:  # TODO: better types
        """Computes the arrow category"""

    @abstractmethod
    def twisted_arrow(
        self, c1: FiniteCategory[Object, Morphism]
    ) -> FiniteCategory[Any, Any]:  # TODO: better types
        """Computes the twisted arrow category"""
