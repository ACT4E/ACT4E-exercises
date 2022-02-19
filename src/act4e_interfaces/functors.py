from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from .categories import Category, FiniteCategory


__all__ = ["Functor", "FiniteFunctor"]


Object1 = TypeVar("Object1")
Morphism1 = TypeVar("Morphism1")
Object2 = TypeVar("Object2")
Morphism2 = TypeVar("Morphism2")
Object3 = TypeVar("Object3")
Morphism3 = TypeVar("Morphism3")


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


# TODO: functor composition
