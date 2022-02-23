from abc import ABC, abstractmethod
from typing import Any, TypedDict, TypeVar

from . import FiniteGroup_desc, FiniteMap_desc, FiniteMonoid_desc, FiniteSemigroup_desc, IOHelper
from .maps import FiniteMap
from .semigroups import (
    FiniteGroup,
    FiniteGroupMorphism,
    FiniteMonoid,
    FiniteMonoidMorphism,
    FiniteSemigroup,
    FiniteSemigroupMorphism,
    GroupMorphism,
    MonoidMorphism,
    SemigroupMorphism,
)

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


class FiniteSemigroupMorphismsChecks(ABC):
    @abstractmethod
    def is_semigroup_morphism(self, a: FiniteSemigroup[A], b: FiniteSemigroup[B], f: FiniteMap[A, B]) -> bool:
        """Check that the triple forms a semigroup morphism."""

    @abstractmethod
    def is_monoid_morphism(self, a: FiniteMonoid[A], b: FiniteMonoid[B], f: FiniteMap[A, B]) -> bool:
        """Check that the triple forms a monoid morphism."""

    @abstractmethod
    def is_group_morphism(self, a: FiniteGroup[A], b: FiniteGroup[B], f: FiniteMap[A, B]) -> bool:
        """Check that the triple forms a monoid morphism."""

    @abstractmethod
    def is_isomorphism(self, a: FiniteSemigroupMorphism[A, B]) -> bool:
        """Check that the morphism is an isomorphism."""


class FiniteSemigroupMorphismsOperations(ABC):
    @abstractmethod
    def compose_semigroup_morphism(
        self, f: SemigroupMorphism[A, B], g: SemigroupMorphism[B, C]
    ) -> SemigroupMorphism[A, C]:
        ...

    @abstractmethod
    def compose_monoid_morphism(
        self, f: MonoidMorphism[A, B], g: MonoidMorphism[B, C]
    ) -> MonoidMorphism[A, C]:
        ...

    @abstractmethod
    def compose_group_morphism(self, f: GroupMorphism[A, B], g: GroupMorphism[B, C]) -> GroupMorphism[A, C]:
        ...


class FiniteSemigroupMorphism_desc(TypedDict):
    source: FiniteSemigroup_desc
    target: FiniteSemigroup_desc
    mapping: FiniteMap_desc


class FiniteMonoidMorphism_desc(TypedDict):
    source: FiniteMonoid_desc
    target: FiniteMonoid_desc
    mapping: FiniteMap_desc


class FiniteGroupMorphism_desc(TypedDict):
    source: FiniteGroup_desc
    target: FiniteGroup_desc
    mapping: FiniteMap_desc


class FiniteSemigroupMorphismRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, s: FiniteSemigroupMorphism_desc) -> FiniteSemigroupMorphism[Any, Any]:
        """Load the data"""

    @abstractmethod
    def save(self, h: IOHelper, m: FiniteSemigroupMorphism[Any, Any]) -> FiniteSemigroupMorphism_desc:
        """Save the data"""


class FiniteMonoidMorphismRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, s: FiniteMonoidMorphism_desc) -> FiniteMonoidMorphism[Any, Any]:
        """Load the data"""

    @abstractmethod
    def save(self, h: IOHelper, m: FiniteMonoidMorphism[Any, Any]) -> FiniteMonoidMorphism_desc:
        """Save the data"""


class FiniteGroupMorphismRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, s: FiniteGroupMorphism_desc) -> FiniteGroupMorphism[Any, Any]:
        """Load the data"""

    @abstractmethod
    def save(self, h: IOHelper, m: FiniteGroupMorphism[Any, Any]) -> FiniteGroupMorphism_desc:
        """Save the data"""
