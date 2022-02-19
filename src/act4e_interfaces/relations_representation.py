from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, List

from typing_extensions import TypedDict

from .helper import IOHelper
from .relations import FiniteRelation
from .sets_representation import FiniteSet_desc
from .types import ConcreteRepr

__all__ = [
    "FiniteRelation_desc",
    "FiniteRelationRepresentation",
]


class FiniteRelation_desc(TypedDict):
    source: FiniteSet_desc
    target: FiniteSet_desc
    values: List[List[ConcreteRepr]]


class FiniteRelationRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, data: FiniteRelation_desc) -> FiniteRelation[Any, Any]:
        """Load a finite set from given YAML data"""

    @abstractmethod
    def save(self, h: IOHelper, f: FiniteRelation[Any, Any]) -> FiniteRelation_desc:
        """Load a finite set from given YAML data"""
