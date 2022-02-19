from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .categories import Category, FiniteCategory

__all__ = ["NaturalTransformation", "FiniteNaturalTransformation"]

Object1 = TypeVar("Object1")
Morphism1 = TypeVar("Morphism1")
Object2 = TypeVar("Object2")
Morphism2 = TypeVar("Morphism2")


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
