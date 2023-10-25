from __future__ import annotations

from abc import ABC
from typing import Any, List

from typing_extensions import TypedDict

from .helper import Serializer
from .semigroups import FiniteGroup, FiniteMonoid, FiniteSemigroup
from .sets_representation import FiniteSet_desc
from .types import ConcreteRepr

__all__ = [
    "FiniteGroupRepresentation",
    "FiniteGroup_desc",
    "FiniteMonoidRepresentation",
    "FiniteMonoid_desc",
    "FiniteSemigroupRepresentation",
    "FiniteSemigroup_desc",
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


class FiniteMonoidRepresentation(Serializer[FiniteMonoid[Any], FiniteMonoid_desc], ABC):
    ...


class FiniteGroupRepresentation(Serializer[FiniteGroup[Any], FiniteGroup_desc], ABC):
    ...
