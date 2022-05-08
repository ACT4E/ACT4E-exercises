from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Dict, Generic, Optional, TypedDict, TypeVar

from .exceptions import InvalidFormat, InvalidValue
from .categories import SemiCategory
from .helper import IOHelper
from .sets import Setoid

__all__ = [
    "FiniteSemiCategory_desc",
    "SemiCategoryRepresentation",
    "RichObject",
    "RichMorphism",
    "StringSetoid",
    "IntegerSetoid",
    "compose_str",
]


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
class RichObject(Generic[OD]):
    label: str
    obdata: OD


@dataclass(frozen=True)
class RichMorphism(Generic[MD]):
    label: str
    mordata: MD


class SemiCategoryRepresentation(ABC):
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


class IntegerSetoid(Setoid[int]):
    """Represents the setoids of integers."""

    def contains(self, x: int) -> bool:
        return isinstance(x, int)

    def save(self, _: IOHelper, x: int) -> int:
        if not isinstance(x, int):
            raise InvalidValue()
        return x

    def load(self, _: IOHelper, o: int) -> int:
        if not isinstance(o, int):
            raise InvalidFormat()
        return o


class StringSetoid(Setoid[str]):
    """Represents the setoids of strings."""

    def contains(self, x: str) -> bool:
        return isinstance(x, str)

    def save(self, _: IOHelper, x: str) -> str:
        if not isinstance(x, str):
            raise InvalidValue()
        return x

    def load(self, _: IOHelper, o: str) -> str:
        if not isinstance(o, str):
            raise InvalidFormat()
        return o


def compose_str(ob1: int, ob2: int, ob3: int, t1: str, t2: str) -> str:
    return t1 + t2


def compose_none(ob1: None, ob2: None, ob3: None, t1: None, t2: None) -> None:
    assert ob1 is None, ob1
    assert ob2 is None, ob2
    assert ob3 is None, ob3
    assert t1 is None, t1
    assert t2 is None, t2
    return None
