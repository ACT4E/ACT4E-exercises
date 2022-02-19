from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .posets import FinitePoset, Poset
from .semigroups import FiniteMonoid, Monoid

__all__ = [
    "FiniteMonoidalPoset",
    "MonoidalPosetOperations",
    "MonoidalPosetOperations",
]

C = TypeVar("C")
E = TypeVar("E")


class MonoidalPoset(Generic[E], ABC):
    """Implementation of finite posets."""

    @abstractmethod
    def poset(self) -> Poset[E]:
        ...

    @abstractmethod
    def monoid(self) -> Monoid[E]:
        ...


class FiniteMonoidalPoset(Generic[E], MonoidalPoset[E], ABC):
    """Implementation of finite posets."""

    @abstractmethod
    def poset(self) -> FinitePoset[E]:
        ...

    @abstractmethod
    def monoid(self) -> FiniteMonoid[E]:
        ...


class MonoidalPosetOperations(ABC):
    """Implementation of finite posets."""

    @abstractmethod
    def is_monoidal_poset(self, fp: FinitePoset[E], fm: FiniteMonoid[E]) -> bool:
        """Check that the pair of poset and monoid make together a monoidal poset."""
