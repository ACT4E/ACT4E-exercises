from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .categories import Category, FiniteCategory

__all__ = ["NaturalTransformation", "FiniteNaturalTransformation"]

Ob1 = TypeVar("Ob1")
Mor1 = TypeVar("Mor1")
Ob2 = TypeVar("Ob2")
Mor2 = TypeVar("Mor2")


class NaturalTransformation(Generic[Ob1, Mor1, Ob2, Mor2], ABC):
    @abstractmethod
    def cat1(self) -> Category[Ob1, Mor1]:
        ...

    @abstractmethod
    def cat2(self) -> Category[Ob2, Mor2]:
        ...

    @abstractmethod
    def component(self, ob: Ob1) -> Mor2:
        """Returns the component for a particular object in the first category.
        This is a morphism in the second category.
        """


class FiniteNaturalTransformation(
    Generic[Ob1, Mor1, Ob2, Mor2],
    NaturalTransformation[Ob1, Mor1, Ob2, Mor2],
    ABC,
):
    @abstractmethod
    def cat1(self) -> FiniteCategory[Ob1, Mor1]:
        ...

    @abstractmethod
    def cat2(self) -> FiniteCategory[Ob2, Mor2]:
        ...
