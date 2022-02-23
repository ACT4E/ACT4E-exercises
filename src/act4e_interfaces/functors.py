from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from .categories import Category, FiniteCategory


__all__ = ["Functor", "FiniteFunctor"]


Ob1 = TypeVar("Ob1")
Mor1 = TypeVar("Mor1")
Ob2 = TypeVar("Ob2")
Mor2 = TypeVar("Mor2")
Ob3 = TypeVar("Ob3")
Mor3 = TypeVar("Mor3")


class Functor(Generic[Ob1, Mor1, Ob2, Mor2], ABC):
    @abstractmethod
    def source(self) -> Category[Ob1, Mor1]:
        ...

    @abstractmethod
    def target(self) -> Category[Ob2, Mor2]:
        ...

    @abstractmethod
    def f_ob(self, ob: Ob1) -> Ob2:
        """Effect on objects"""

    @abstractmethod
    def f_mor(self, m: Mor1) -> Mor2:
        """Effect on morphisms"""


class FiniteFunctor(Generic[Ob1, Mor1, Ob2, Mor2], Functor[Ob1, Mor1, Ob2, Mor2], ABC):
    @abstractmethod
    def source(self) -> FiniteCategory[Ob1, Mor1]:
        ...

    @abstractmethod
    def target(self) -> FiniteCategory[Ob2, Mor2]:
        ...


# TODO: functor composition
