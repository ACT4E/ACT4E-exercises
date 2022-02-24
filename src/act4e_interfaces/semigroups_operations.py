from abc import ABC, abstractmethod
from typing import Any, TypedDict, TypeVar

from .helper import Serializer
from .maps import FiniteMap
from .maps_representation import FiniteMap_desc
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
from .semigroups_representation import FiniteGroup_desc, FiniteMonoid_desc, FiniteSemigroup_desc

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


#
# @abstractmethod
# def is_isomorphism(self, a: FiniteSemigroupMorphism[A, B]) -> bool:
#     """Check that the morphism is an isomorphism."""

#
# class SemigroupMorphismsOperations(ABC):
#     @abstractmethod
#     def compose_semi(self, f: SemigroupMorphism[A, B], g: SemigroupMorphism[B, C]) -> SemigroupMorphism[A, C]:
#         ...
#
#     @abstractmethod
#     def compose_monoid(self, f: MonoidMorphism[A, B], g: MonoidMorphism[B, C]) -> MonoidMorphism[A, C]:
#         ...
#
#     @abstractmethod
#     def compose_group(self, f: GroupMorphism[A, B], g: GroupMorphism[B, C]) -> GroupMorphism[A, C]:
#         ...


class FiniteSemigroupMorphismsOperations(ABC):
    @abstractmethod
    def compose_semi(
        self, f: FiniteSemigroupMorphism[A, B], g: FiniteSemigroupMorphism[B, C]
    ) -> FiniteSemigroupMorphism[A, C]:
        ...

    @abstractmethod
    def compose_monoid(
        self, f: FiniteMonoidMorphism[A, B], g: FiniteMonoidMorphism[B, C]
    ) -> FiniteMonoidMorphism[A, C]:
        ...

    @abstractmethod
    def compose_group(
        self, f: FiniteGroupMorphism[A, B], g: FiniteGroupMorphism[B, C]
    ) -> FiniteGroupMorphism[A, C]:
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


class FiniteSemigroupMorphismRepresentation(
    Serializer[FiniteSemigroupMorphism[Any, Any], FiniteSemigroupMorphism_desc], ABC
):
    ...


# @abstractmethod
# def load(self, h: IOHelper, s: FiniteSemigroupMorphism_desc) -> FiniteSemigroupMorphism[Any, Any]:
#     """Load the data"""
#
# @abstractmethod
# def save(self, h: IOHelper, m: FiniteSemigroupMorphism[Any, Any]) -> FiniteSemigroupMorphism_desc:
#     """Save the data"""


class FiniteMonoidMorphismRepresentation(
    Serializer[FiniteMonoidMorphism[Any, Any], FiniteMonoidMorphism_desc], ABC
):
    pass


# @abstractmethod
# def load(self, h: IOHelper, s: FiniteMonoidMorphism_desc) -> FiniteMonoidMorphism[Any, Any]:
#     """Load the data"""
#
# @abstractmethod
# def save(self, h: IOHelper, m: FiniteMonoidMorphism[Any, Any]) -> FiniteMonoidMorphism_desc:
#     """Save the data"""


class FiniteGroupMorphismRepresentation(
    Serializer[FiniteGroupMorphism[Any, Any], FiniteGroupMorphism_desc], ABC
):
    ...


#
# @abstractmethod
# def load(self, h: IOHelper, s: FiniteGroupMorphism_desc) -> FiniteGroupMorphism[Any, Any]:
#     """Load the data"""
#
# @abstractmethod
# def save(self, h: IOHelper, m: FiniteGroupMorphism[Any, Any]) -> FiniteGroupMorphism_desc:
#     """Save the data"""
