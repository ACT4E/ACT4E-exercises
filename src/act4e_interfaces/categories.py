from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, Tuple, TypeVar

from .dps import DP
from .posets import Poset
from .relations import FiniteRelation
from .sets import FiniteSet, Setoid
from .sets_product import FiniteSetProduct, SetProduct
from .types import Object

__all__ = [
    "MonoidalCategory",
    "MonoidalCategory",
    "FiniteProfunctor",
    "FiniteFunctor",
    "FiniteAdjunction",
    "FiniteMonoidalCategory",
    "FiniteCategory",
    "FiniteEnrichedCategory",
    "FiniteSemiCategory",
    "FiniteCategoryOperations",
    "FiniteAdjunctionsOperations",
    "FiniteProfunctorOperations",
    "FiniteNaturalTransformation",
    "Adjunction",
    "SemiCategory",
    "SemiBiCategory",
    "Category",
    "CategoryOperations",
    "DPCategory",
]
E1 = TypeVar("E1")
E2 = TypeVar("E2")

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")

O1 = TypeVar("O1")
O2 = TypeVar("O2")

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


class Functor(Generic[Object1, Morphism1, Object2, Morphism2], ABC):
    @abstractmethod
    def source(self) -> Category[Object1, Morphism1]:
        ...

    @abstractmethod
    def target(self) -> Category[Object2, Morphism2]:
        ...

    @abstractmethod
    def f_ob(self, ob: Object1) -> Object2:
        """Effect on objects"""

    @abstractmethod
    def f_mor(self, m: Morphism1) -> Morphism2:
        """Effect on morphisms"""


class FiniteFunctor(
    Generic[Object1, Morphism1, Object2, Morphism2], Functor[Object1, Morphism1, Object2, Morphism2], ABC
):
    @abstractmethod
    def source(self) -> FiniteCategory[Object1, Morphism1]:
        ...

    @abstractmethod
    def target(self) -> FiniteCategory[Object2, Morphism2]:
        ...


class MonoidalCategory(Generic[Object, Morphism], Category[Object, Morphism], ABC):
    @abstractmethod
    def monoidal_unit(self) -> Object:
        """Return the product functor."""

    @abstractmethod
    def monoidal_product(self) -> FiniteFunctor[Object, Morphism, Object, Morphism]:  # XXX: to check
        """Return the product functor."""


class FiniteMonoidalCategory(
    Generic[Object, Morphism], MonoidalCategory[Object, Morphism], FiniteCategory[Object, Morphism], ABC
):
    ...


class NaturalTransformation(Generic[Object1, Morphism1, Object2, Morphism2], ABC):
    @abstractmethod
    def cat1(self) -> Category[Object1, Morphism1]:
        ...

    @abstractmethod
    def cat2(self) -> Category[Object2, Morphism2]:
        ...

    @abstractmethod
    def component(self, ob: Object1) -> Morphism2:
        """Returns the component for a particular object in the first category.
        This is a morphism in the second category.
        """


class FiniteNaturalTransformation(
    Generic[Object1, Morphism1, Object2, Morphism2],
    NaturalTransformation[Object1, Morphism1, Object2, Morphism2],
    ABC,
):
    @abstractmethod
    def cat1(self) -> FiniteCategory[Object1, Morphism1]:
        ...

    @abstractmethod
    def cat2(self) -> FiniteCategory[Object2, Morphism2]:
        ...


class Adjunction(Generic[Object1, Morphism1, Object2, Morphism2], ABC):
    @abstractmethod
    def source(self) -> Category[Object1, Morphism1]:
        ...

    @abstractmethod
    def target(self) -> Category[Object2, Morphism2]:
        ...

    @abstractmethod
    def left(self) -> Functor[Object1, Morphism1, Object2, Morphism2]:
        ...

    @abstractmethod
    def right(self) -> Functor[Object2, Morphism2, Object1, Morphism1]:
        ...


class FiniteAdjunction(
    Generic[Object1, Morphism1, Object2, Morphism2], Adjunction[Object1, Morphism1, Object2, Morphism2], ABC
):
    @abstractmethod
    def source(self) -> FiniteCategory[Object1, Morphism1]:
        ...

    @abstractmethod
    def target(self) -> FiniteCategory[Object2, Morphism2]:
        ...

    @abstractmethod
    def left(self) -> FiniteFunctor[Object1, Morphism1, Object2, Morphism2]:
        ...

    @abstractmethod
    def right(self) -> FiniteFunctor[Object2, Morphism2, Object1, Morphism1]:
        ...


class FiniteAdjunctionsOperations(ABC):
    @abstractmethod
    def is_adjunction(
        self,
        left: FiniteFunctor[Object1, Morphism1, Object2, Morphism2],
        right: FiniteFunctor[Object2, Morphism2, Object1, Morphism1],
    ) -> bool:
        """check the pair is an adjunction"""

    @abstractmethod
    def compose(
        self,
        adj1: FiniteAdjunction[Object1, Morphism1, Object2, Morphism2],
        adj2: FiniteAdjunction[Object2, Morphism2, Object3, Morphism3],
    ) -> FiniteAdjunction[Object1, Morphism1, Object3, Morphism3]:
        """compose two compatible adjunctions"""

    @abstractmethod
    def from_relation(self, f: FiniteRelation[A, B]) -> FiniteAdjunction[Any, Any, Any, Any]:  # TODO: type
        ...


class Profunctor(ABC):
    pass  # # def source(self) -> Category:  #     ...  #  # def target(self) -> Category:  #     ...  #
    # def functor(self) -> Functor:  #     ...


class FiniteProfunctor(ABC):
    pass  # # def cat1(self) -> FiniteCategory:  #     ...  #  # def cat2(self) -> FiniteCategory:  #
    # ...  #  # def functor(self) -> FiniteFunctor:  #     ...


class FiniteProfunctorOperations(ABC):
    pass  # # @abstractmethod  # def series(self, p1: FiniteProfunctor, p2: FiniteProfunctor) ->
    # FiniteProfunctor:  #     ...


class FiniteEnrichedCategory(Generic[Object, Morphism], FiniteCategory[Object, Morphism], ABC):
    pass  # def enrichment(self) -> FiniteMonoidalCategory:  #     ...


class DPCategory(Category[Poset[Any], DP[Any, Any]], ABC):
    ...
