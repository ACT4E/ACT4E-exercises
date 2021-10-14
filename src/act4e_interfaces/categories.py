from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable, Generic, Tuple, TypeVar

from .posets import FinitePoset, MonotoneMap, Poset
from .relations import FiniteRelation
from .sets import EnumerableSet, FiniteMap, FiniteSet, Setoid
from .types import Object

__all__ = [
    "EnumerableSetsOperations",
    "SetoidOperations",
    "MonoidalCategory",
    "MonoidalCategory",
    "FiniteDP",
    "FiniteProfunctor",
    "FiniteFunctor",
    "FiniteAdjunction",
    "FiniteMonoidalCategory",
    "FiniteCategory",
    "FiniteEnrichedCategory",
    "FiniteSemiCategory",
    "FiniteCategoryOperations",
    "FiniteDPOperations",
    "FiniteAdjunctionsOperations",
    "FiniteProfunctorOperations",
    "FiniteMapOperations",
    "FiniteNaturalTransformation",
    "Adjunction",
    "SemiCategory",
    "SemiBiCategory",
    "Category",
    "CategoryOperations",
    "DP",
    "DPCategory",
    "DPI",
    "DPConstructors",
]
E1 = TypeVar("E1")
E2 = TypeVar("E2")


class FiniteMapOperations(ABC):
    @abstractmethod
    def compose(self, f: FiniteMap, g: FiniteMap) -> FiniteMap:
        """ compose two functions"""

    @abstractmethod
    def as_relation(self, f: FiniteMap) -> FiniteRelation:
        """ Load the data  """


O1 = TypeVar("O1")
O2 = TypeVar("O2")
#
#
# class BaseMorphism(Generic[O1, O2], ABC):
#     @abstractmethod
#     def source(self) -> O1:
#         pass
#
#     @abstractmethod
#     def target(self) -> O2:
#         pass


Morphism = TypeVar("Morphism")


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
        """ Return source and target of the morphism """


class SemiCategory(Generic[Object, Morphism], SemiBiCategory[Object, Morphism], ABC):
    ...


class Category(Generic[Object, Morphism], SemiCategory[Object, Morphism], ABC):
    @abstractmethod
    def identity(self, ob: Object) -> Morphism:
        """ Identity for the object """


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
    def product(self, c1: Category, c2: Category) -> Category:
        """ Product of two categories. """

    @abstractmethod
    def disjoint_union(self, c1: Category, c2: Category) -> FiniteCategory:
        """ Disjoint union for the categories """

    @abstractmethod
    def arrow(self, c1: Category) -> Category:
        """ Computes the arrow category """

    @abstractmethod
    def twisted(self, c1: Category) -> Category:
        """ Computes the twisted arrow category """


class FiniteCategoryOperations:
    @abstractmethod
    def product(self, c1: FiniteCategory, c2: FiniteCategory) -> FiniteCategory:
        """ Product of two categories. """

    @abstractmethod
    def disjoint_union(self, c1: FiniteCategory, c2: FiniteCategory) -> FiniteCategory:
        """ Disjoint union for the categories """

    @abstractmethod
    def arrow(self, c1: FiniteCategory) -> FiniteCategory:
        """ Computes the arrow category """

    @abstractmethod
    def twisted_arrow(self, c1: FiniteCategory) -> FiniteCategory:
        """ Computes the twisted arrow category """


class Functor(ABC):
    @abstractmethod
    def source(self) -> Category:
        ...

    @abstractmethod
    def target(self) -> Category:
        ...

    @abstractmethod
    def f_ob(self, ob: Object) -> Object:
        """ Effect on objects """

    @abstractmethod
    def f_mor(self, m: Morphism) -> Morphism:
        """ Effect on morphisms """


class FiniteFunctor(Functor, ABC):
    @abstractmethod
    def source(self) -> FiniteCategory:
        ...

    @abstractmethod
    def target(self) -> FiniteCategory:
        ...


class MonoidalCategory(Category, ABC):
    @abstractmethod
    def monoidal_unit(self) -> Object:
        """ Return the product functor. """

    @abstractmethod
    def monoidal_product(self) -> FiniteFunctor:
        """ Return the product functor. """


class FiniteMonoidalCategory(MonoidalCategory, FiniteCategory, ABC):
    ...


class NaturalTransformation(ABC):
    @abstractmethod
    def cat1(self) -> Category:
        ...

    @abstractmethod
    def cat2(self) -> Category:
        ...

    @abstractmethod
    def component(self, ob: Object) -> Morphism:
        """Returns the component for a particular object in the first category.
        This is a morphism in the second category.
        """


class FiniteNaturalTransformation(NaturalTransformation, ABC):
    @abstractmethod
    def cat1(self) -> FiniteCategory:
        ...

    @abstractmethod
    def cat2(self) -> FiniteCategory:
        ...


class Adjunction(ABC):
    @abstractmethod
    def source(self) -> Category:
        ...

    @abstractmethod
    def target(self) -> Category:
        ...

    @abstractmethod
    def left(self) -> Functor:
        ...

    @abstractmethod
    def right(self) -> Functor:
        ...


class FiniteAdjunction(Adjunction, ABC):
    @abstractmethod
    def source(self) -> FiniteCategory:
        ...

    @abstractmethod
    def target(self) -> FiniteCategory:
        ...

    @abstractmethod
    def left(self) -> FiniteFunctor:
        ...

    @abstractmethod
    def right(self) -> FiniteFunctor:
        ...


class FiniteAdjunctionsOperations(ABC):
    @abstractmethod
    def is_adjunction(self, left: FiniteFunctor, right: FiniteFunctor) -> bool:
        """ check the pair is an adjunction """

    @abstractmethod
    def compose(self, adj1: FiniteAdjunction, adj2: FiniteAdjunction) -> FiniteAdjunction:
        """ compose two compatible adjunctions"""

    @abstractmethod
    def from_relation(self, f: FiniteRelation) -> FiniteAdjunction:
        ...


F = TypeVar("F")
I = TypeVar("I")
R = TypeVar("R")


class DPI(Generic[F, I, R], ABC):
    @abstractmethod
    def functionality(self) -> Poset[F]:
        ...

    @abstractmethod
    def implementations(self) -> Setoid[I]:
        ...

    @abstractmethod
    def costs(self) -> Poset[R]:
        ...

    @abstractmethod
    def requires(self, i: I) -> R:
        ...

    @abstractmethod
    def provides(self, i: I) -> F:
        ...


class FiniteDPI(Generic[F, I, R], DPI[F, I, R], ABC):
    @abstractmethod
    def functionality(self) -> FinitePoset[F]:
        ...

    @abstractmethod
    def implementations(self) -> FiniteSet[I]:
        ...

    @abstractmethod
    def costs(self) -> FinitePoset[R]:
        ...


class DP(Generic[F, R], ABC):
    @abstractmethod
    def functionality(self) -> Poset[F]:
        ...

    @abstractmethod
    def costs(self) -> Poset[R]:
        ...

    @abstractmethod
    def feasible(self, f: F, r: R) -> bool:
        ...


class FiniteDP(Generic[F, R], DP[F, R], ABC):
    @abstractmethod
    def functionality(self) -> FinitePoset[F]:
        ...

    @abstractmethod
    def costs(self) -> FinitePoset[R]:
        ...


class DPConstructors(ABC):
    @abstractmethod
    def companion(self, f: MonotoneMap[E1, E2]) -> DP[E1, E2]:
        ...

    @abstractmethod
    def conjoint(self, f: MonotoneMap[E1, E2]) -> DP[E1, E2]:
        ...


class FiniteDPOperations(ABC):
    @abstractmethod
    def series(self, dp1: FiniteDP, dp2: FiniteDP) -> FiniteDP:
        ...

    @abstractmethod
    def union(self, dp1: FiniteDP, dp2: FiniteDP) -> FiniteDP:
        ...

    @abstractmethod
    def intersection(self, dp1: FiniteDP, dp2: FiniteDP) -> FiniteDP:
        ...

    @abstractmethod
    def from_relation(self, f: FiniteRelation) -> FiniteDP:
        ...


class DPCategory(Category, ABC):
    ...


class Profunctor(ABC):
    def source(self) -> Category:
        ...

    def target(self) -> Category:
        ...

    def functor(self) -> Functor:
        ...


class FiniteProfunctor(ABC):
    def cat1(self) -> FiniteCategory:
        ...

    def cat2(self) -> FiniteCategory:
        ...

    def functor(self) -> FiniteFunctor:
        ...


class FiniteProfunctorOperations(ABC):
    @abstractmethod
    def series(self, p1: FiniteProfunctor, p2: FiniteProfunctor) -> FiniteProfunctor:
        ...


class FiniteEnrichedCategory(FiniteCategory, ABC):
    def enrichment(self) -> FiniteMonoidalCategory:
        ...


class SetoidOperations(ABC):
    @classmethod
    @abstractmethod
    def union_setoids(cls, a: Setoid, b: Setoid) -> Setoid:
        """ Creates the union of two Setoids. """

    @classmethod
    @abstractmethod
    def intersection_setoids(cls, a: Setoid, b: Setoid) -> Setoid:
        """ Creates the intersection of two Setoids. """


class EnumerableSetsOperations(ABC):
    @classmethod
    @abstractmethod
    def make_set_sequence(cls, f: Callable[[int], object]):
        """Creates an EnumerableSet from a function that gives the
        i-th element."""

    @classmethod
    @abstractmethod
    def union_esets(cls, a: EnumerableSet, b: EnumerableSet) -> EnumerableSet:
        """ Creates the union of two EnumerableSet. """
