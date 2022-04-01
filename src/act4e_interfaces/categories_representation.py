from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Dict, Generic, Optional, Tuple, TypedDict, TypeVar

from .helper import IOHelper
from .categories import SemiCategory
from .sets import Setoid

__all__ = ["FiniteSemiCategory_desc", "SemiCategoryRepresentation", "RichObject", "RichMorphism"]


class Morphisms_desc(TypedDict):
    source: str
    target: str
    mordata: Any


class ID_desc(TypedDict):
    mordata: Any


class Objects_desc(TypedDict):
    identity: Optional[ID_desc]
    obdata: Any


class FiniteSemiCategory_desc(TypedDict):
    objects: Dict[str, Objects_desc]
    morphisms: Dict[str, Morphisms_desc]


OD = TypeVar("OD")
MD = TypeVar("MD")

X = TypeVar("X")


@dataclass(frozen=True)
class RichObject(Generic[X]):
    label: str
    obdata: X


@dataclass(frozen=True)
class RichMorphism(Generic[X]):
    label: str
    mordata: X


class SemiCategoryRepresentation:
    @abstractmethod
    def load(
        self,
        h: IOHelper,
        data: FiniteSemiCategory_desc,
        ObData: Setoid[OD],
        MorData: Setoid[MD],
        compose: Callable[[OD, OD, OD, MD, MD], MD],
    ) -> SemiCategory[RichObject[OD], RichMorphism[MD]]:
        pass
