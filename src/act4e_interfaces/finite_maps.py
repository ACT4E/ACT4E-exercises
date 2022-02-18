from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar

from .relations import FiniteRelation
from .sets import FiniteMap

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")

__all__ = ["FiniteMapOperations"]


class FiniteMapOperations(ABC):
    @abstractmethod
    def compose(self, f: FiniteMap[A, B], g: FiniteMap[B, C]) -> FiniteMap[A, C]:
        """compose two functions"""

    @abstractmethod
    def as_relation(self, f: FiniteMap[A, B]) -> FiniteRelation[A, B]:
        """Load the data"""
