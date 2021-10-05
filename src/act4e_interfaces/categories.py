from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable, Tuple

from .posets import MonotoneMap, Poset
from .relations import FiniteRelation
from .sets import EnumerableSet, FiniteMap, FiniteSet, Mapping, Setoid
from .types import Morphism, Object

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


class FiniteMapOperations(ABC):
    @abstractmethod
    def compose(self, f: FiniteMap, g: FiniteMap) -> FiniteMap:
        """ compose two functions"""

    @abstractmethod
    def as_relation(self, f: FiniteMap) -> FiniteRelation:
        """ Load the data  """


class SemiBiCategory(ABC):
    @abstractmethod
    def objects(self) -> Setoid:
        ...

    @abstractmethod
    def hom(self, ob1: Object, ob2: Object) -> Setoid:
        ...

    @abstractmethod
    def legs(self, m: Morphism) -> Tuple[Object, Object]:
        """ Return source and target of the morphism """


class SemiCategory(SemiBiCategory, ABC):
    ...


class Category(SemiCategory, ABC):
    @abstractmethod
    def identity(self, ob: Object) -> Morphism:
        """ Identity for the object """


assert [1] + [1, 2] == [1, 1, 2]
assert [1, 1, 2] + [] == [1, 1, 2]


class FiniteSemiCategory(SemiCategory, ABC):
    @abstractmethod
    def objects(self) -> FiniteSet:
        ...

    @abstractmethod
    def hom(self, ob1: Object, ob2: Object) -> FiniteSet:
        ...


class FiniteCategory(FiniteSemiCategory, Category, ABC):
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


class DPI(ABC):
    @abstractmethod
    def functionality(self) -> Poset:
        ...

    @abstractmethod
    def implementations(self) -> Setoid:
        ...

    @abstractmethod
    def costs(self) -> Poset:
        ...

    @abstractmethod
    def requires(self) -> Mapping:
        ...

    @abstractmethod
    def provides(self) -> Mapping:
        ...


class DPCategory(Category, ABC):
    ...


class DP(ABC):
    ...


class FiniteDP(ABC):
    ...


class DPConstructors(ABC):
    @abstractmethod
    def companion(self, f: MonotoneMap) -> DP:
        ...

    @abstractmethod
    def conjoint(self, f: MonotoneMap) -> DP:
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
