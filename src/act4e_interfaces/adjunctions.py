from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from .categories import Category, FiniteCategory
from .functors import FiniteFunctor, Functor
from .relations import FiniteRelation

__all__ = ["Adjunction", "FiniteAdjunction", "FiniteAdjunctionsOperations"]
Object = TypeVar("Object")
Morphism = TypeVar("Morphism")

Object1 = TypeVar("Object1")
Morphism1 = TypeVar("Morphism1")
Object2 = TypeVar("Object2")
Morphism2 = TypeVar("Morphism2")
Object3 = TypeVar("Object3")
Morphism3 = TypeVar("Morphism3")


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
    def from_relation(
        self, f: FiniteRelation[Any, Any]
    ) -> FiniteAdjunction[Any, Any, Any, Any]:  # TODO: type
        ...
