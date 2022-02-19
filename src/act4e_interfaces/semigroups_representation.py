from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, List

from typing_extensions import TypedDict

from .helper import IOHelper
from .semigroups import FiniteGroup, FiniteMonoid, FiniteSemigroup
from .sets_representation import FiniteSet_desc
from .types import ConcreteRepr

__all__ = [
    "FiniteSemigroup_desc",
    "FiniteGroup_desc",
    "FiniteMonoid_desc",
    "FiniteGroupRepresentation",
    "FiniteMonoidRepresentation",
    "FiniteSemigroupRepresentation",
]


class FiniteSemigroup_desc(TypedDict):
    carrier: FiniteSet_desc
    composition: List[List[ConcreteRepr]]


class FiniteMonoid_desc(FiniteSemigroup_desc):
    neutral: ConcreteRepr


class FiniteGroup_desc(FiniteMonoid_desc):
    inverse: List[List[ConcreteRepr]]


class FiniteSemigroupRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, s: FiniteSemigroup_desc) -> FiniteSemigroup[Any]:
        """Load the data"""

    @abstractmethod
    def save(self, h: IOHelper, m: FiniteSemigroup[Any]) -> FiniteSemigroup_desc:
        """Save the data"""


class FiniteMonoidRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, s: FiniteMonoid_desc) -> FiniteMonoid[Any]:
        """Load the data"""

    @abstractmethod
    def save(self, h: IOHelper, m: FiniteMonoid[Any]) -> FiniteMonoid_desc:
        """Save the data"""


class FiniteGroupRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, s: FiniteGroup_desc) -> FiniteGroup[Any]:
        """Load the data"""

    @abstractmethod
    def save(self, h: IOHelper, m: FiniteGroup[Any]) -> FiniteGroup_desc:
        """Save the data"""
