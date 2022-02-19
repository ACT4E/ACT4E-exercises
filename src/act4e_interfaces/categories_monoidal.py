from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .categories import Category, FiniteCategory
from .functors import FiniteFunctor

__all__ = ["MonoidalCategory", "FiniteMonoidalCategory"]

Object = TypeVar("Object")
Morphism = TypeVar("Morphism")


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
