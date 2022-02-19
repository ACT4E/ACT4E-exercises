from abc import ABC, abstractmethod
from typing import Any, Generic, Sequence, TypeVar

from .posets import FinitePoset, Poset
from .sets_product import (
    FiniteSetProduct,
    SetProduct,
)

__all__ = [
    "FinitePosetConstructionProduct",
    "FinitePosetProduct",
    "PosetProduct",
]

C = TypeVar("C")
E = TypeVar("E")


class PosetProduct(Generic[C, E], Poset[E], ABC):
    """A poset product is a poset that can be factorized."""

    @abstractmethod
    def carrier(self) -> SetProduct[C, E]:
        """Returns the components of the product"""

    @abstractmethod
    def components(self) -> Sequence[Poset[C]]:
        """Returns the components of the product"""

    @abstractmethod
    def pack(self, args: Sequence[C]) -> E:
        """Packs an element of each setoid into an element of the mapping"""
        raise NotImplementedError()

    @abstractmethod
    def unpack(self, e: E) -> Sequence[C]:
        raise NotImplementedError()


class FinitePosetProduct(Generic[C, E], FinitePoset[E], PosetProduct[C, E], ABC):
    """Specialization of PosetProduct where we deal with FinitePosets"""

    @abstractmethod
    def carrier(self) -> FiniteSetProduct[C, E]:
        """Returns the components of the product"""

    @abstractmethod
    def components(self) -> Sequence[FinitePoset[C]]:
        """Returns the components"""


class FinitePosetConstructionProduct(ABC):
    @abstractmethod
    def product(self, ps: Sequence[FinitePoset[C]]) -> FinitePosetProduct[C, Any]:
        ...
