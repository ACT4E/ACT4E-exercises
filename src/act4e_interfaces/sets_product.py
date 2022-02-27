from abc import ABC, abstractmethod
from typing import Any, Generic, Sequence, TypeVar

from .sets import FiniteSet, Setoid

C = TypeVar("C")  # composite
E = TypeVar("E")  # composite

__all__ = ["SetProduct", "FiniteSetProduct", "FiniteMakeSetProduct"]


class SetProduct(Generic[C, E], Setoid[E], ABC):
    """A set product is a setoid that can be factorized."""

    @abstractmethod
    def components(self) -> Sequence[Setoid[C]]:
        """Returns the components of the product."""

    @abstractmethod
    def pack(self, args: Sequence[C]) -> E:
        """Packs an element of each setoid into an element of the product."""

    @abstractmethod
    def unpack(self, args: E) -> Sequence[C]:
        """Unpacks an element of the product to the constituents."""


class FiniteSetProduct(Generic[C, E], FiniteSet[E], SetProduct[C, E], ABC):
    """Specialization of SetProduct where we deal with FiniteSets"""

    @abstractmethod
    def components(self) -> Sequence[FiniteSet[C]]:
        """Returns the components"""


class FiniteMakeSetProduct(ABC):
    @abstractmethod
    def product(self, components: Sequence[FiniteSet[C]]) -> FiniteSetProduct[C, Any]:
        ...


# @overload
# def product(self, components: Sequence[Setoid[C]]) -> SetProduct[C, Any]:
#     ...
#
# @abstractmethod
# def product(self, components: Sequence[Setoid[C]]) -> SetProduct[C, Any]:
#     ...
