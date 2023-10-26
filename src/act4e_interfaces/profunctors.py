from abc import ABC
from typing import Generic, TypeVar, Any

from .categories import FiniteCategory, Category
from .posets import Poset
from .dps import DP

Object = TypeVar("Object")
Morphism = TypeVar("Morphism")

__all__ = [
    "DPCategory",
    "FiniteEnrichedCategory",
    "FiniteProfunctor",
    "FiniteProfunctorOperations",
    "Profunctor",
]


class Profunctor(ABC):
    pass
    # def source(self) -> Category:  #     ...  #  # def target(self) -> Category:  #     ...  #
    # def functor(self) -> Functor:  #     ...


class FiniteProfunctor(ABC):
    pass
    # def cat1(self) -> FiniteCategory:  #     ...  #  # def cat2(self) -> FiniteCategory:  #
    # ...  #  # def functor(self) -> FiniteFunctor:  #     ...


class FiniteProfunctorOperations(ABC):
    pass
    # @abstractmethod  # def series(self, p1: FiniteProfunctor, p2: FiniteProfunctor) ->
    # FiniteProfunctor:  #     ...


class FiniteEnrichedCategory(Generic[Object, Morphism], FiniteCategory[Object, Morphism], ABC):
    pass
    # def enrichment(self) -> FiniteMonoidalCategory:  #     ...


class DPCategory(Category[Poset[Any], DP[Any, Any]], ABC):
    ...
