from __future__ import annotations

from abc import ABC
from typing import Any, Final, List, Union

from typing_extensions import TypedDict

from .helper import Serializer
from .posets import FinitePoset
from .sets_representation import FiniteSet_desc
from .types import ConcreteRepr

__all__ = [
    "FinitePoset_desc",
    "FinitePoset_sum_desc",
    "FinitePoset_product_desc",
    "FinitePoset_simple_desc",
    "FinitePosetRepresentation",
]


class FinitePoset_simple_desc(TypedDict):
    carrier: FiniteSet_desc
    hasse: List[List[ConcreteRepr]]


class FinitePoset_sum_desc(TypedDict):
    poset_sum: List[Any]


class FinitePoset_product_desc(TypedDict):
    poset_product: List[Any]


FinitePoset_desc = Union[
    FinitePoset_simple_desc,
    FinitePoset_sum_desc,
    FinitePoset_product_desc,
]


class FinitePosetRepresentation(Serializer[FinitePoset[Any], FinitePoset_desc], ABC):
    pass


# @abstractmethod
# def load(self, h: IOHelper, s: FinitePoset_desc) -> FinitePoset[Any]:
#     """Load the data"""
#
# @abstractmethod
# def save(self, h: IOHelper, m: FinitePoset[Any]) -> FinitePoset_desc:
#     """Save the data"""


KWD_POSET_SUM: Final[str] = "poset_sum"
KWD_POSET_PRODUCT: Final[str] = "poset_product"
