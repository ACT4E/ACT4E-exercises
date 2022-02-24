from __future__ import annotations

from abc import ABC
from typing import Any, List

from typing_extensions import TypedDict

from .helper import Serializer
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


class FiniteSemigroupRepresentation(Serializer[FiniteSemigroup[Any], FiniteSemigroup_desc], ABC):
    pass


# @abstractmethod
# def load(self, h: IOHelper, s: FiniteSemigroup_desc) -> FiniteSemigroup[Any]:
#     ...
#
# @abstractmethod
# def save(self, h: IOHelper, m: FiniteSemigroup[Any]) -> FiniteSemigroup_desc:
#     ...


class FiniteMonoidRepresentation(Serializer[FiniteMonoid[Any], FiniteMonoid_desc], ABC):
    ...


# @abstractmethod
# def load(self, h: IOHelper, s: FiniteMonoid_desc) -> FiniteMonoid[Any]:
#     ...
#
# @abstractmethod
# def save(self, h: IOHelper, m: FiniteMonoid[Any]) -> FiniteMonoid_desc:
#     ...


class FiniteGroupRepresentation(Serializer[FiniteGroup[Any], FiniteGroup_desc], ABC):
    ...


# @abstractmethod
# def load(self, h: IOHelper, s: FiniteGroup_desc) -> FiniteGroup[Any]:
#     ...
#
# @abstractmethod
# def save(self, h: IOHelper, m: FiniteGroup[Any]) -> FiniteGroup_desc:
#     ...
