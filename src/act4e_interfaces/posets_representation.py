from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, List

from typing_extensions import TypedDict

from .helper import IOHelper
from .posets import FinitePoset
from .sets_representation import FiniteSet_desc
from .types import ConcreteRepr

__all__ = [
    "FinitePoset_desc",
    "FinitePosetRepresentation",
]


class FinitePoset_desc(TypedDict):
    carrier: FiniteSet_desc
    hasse: List[List[ConcreteRepr]]


class FinitePosetRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, s: FinitePoset_desc) -> FinitePoset[Any]:
        """Load the data"""

    @abstractmethod
    def save(self, h: IOHelper, m: FinitePoset[Any]) -> FinitePoset_desc:
        """Save the data"""
