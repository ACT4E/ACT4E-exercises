from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from .categories import Category, FiniteCategory
from .functors import FiniteFunctor, Functor
from .relations import FiniteRelation

__all__ = ["Adjunction", "FiniteAdjunction", "FiniteAdjunctionsOperations"]
Object = TypeVar("Object")
Morphism = TypeVar("Morphism")

Ob1 = TypeVar("Ob1")
Mor1 = TypeVar("Mor1")
Ob2 = TypeVar("Ob2")
Mor2 = TypeVar("Mor2")
Ob3 = TypeVar("Ob3")
Mor3 = TypeVar("Mor3")


class Adjunction(Generic[Ob1, Mor1, Ob2, Mor2], ABC):
    @abstractmethod
    def source(self) -> Category[Ob1, Mor1]:
        ...

    @abstractmethod
    def target(self) -> Category[Ob2, Mor2]:
        ...

    @abstractmethod
    def left(self) -> Functor[Ob1, Mor1, Ob2, Mor2]:
        ...

    @abstractmethod
    def right(self) -> Functor[Ob2, Mor2, Ob1, Mor1]:
        ...


class FiniteAdjunction(Generic[Ob1, Mor1, Ob2, Mor2], Adjunction[Ob1, Mor1, Ob2, Mor2], ABC):
    @abstractmethod
    def source(self) -> FiniteCategory[Ob1, Mor1]:
        ...

    @abstractmethod
    def target(self) -> FiniteCategory[Ob2, Mor2]:
        ...

    @abstractmethod
    def left(self) -> FiniteFunctor[Ob1, Mor1, Ob2, Mor2]:
        ...

    @abstractmethod
    def right(self) -> FiniteFunctor[Ob2, Mor2, Ob1, Mor1]:
        ...


class FiniteAdjunctionsOperations(ABC):
    @abstractmethod
    def is_adjunction(
        self,
        left: FiniteFunctor[Ob1, Mor1, Ob2, Mor2],
        right: FiniteFunctor[Ob2, Mor2, Ob1, Mor1],
    ) -> bool:
        """check the pair is an adjunction"""

    @abstractmethod
    def compose(
        self,
        adj1: FiniteAdjunction[Ob1, Mor1, Ob2, Mor2],
        adj2: FiniteAdjunction[Ob2, Mor2, Ob3, Mor3],
    ) -> FiniteAdjunction[Ob1, Mor1, Ob3, Mor3]:
        """compose two compatible adjunctions"""

    @abstractmethod
    def from_relation(
        self, f: FiniteRelation[Any, Any]
    ) -> FiniteAdjunction[Any, Any, Any, Any]:  # TODO: type
        ...
