from abc import ABC, abstractmethod
from typing import Any, Dict, TypedDict

from .categories_representation import FiniteSemiCategory_desc
from .functors import FiniteFunctor
from .helper import IOHelper

__all__ = ["FiniteFunctor_desc", "FiniteFunctorRepresentation"]


class FiniteFunctor_desc(TypedDict):
    source: FiniteSemiCategory_desc
    target: FiniteSemiCategory_desc
    f_ob: Dict[str, str]
    f_mor: Dict[str, str]


class FiniteFunctorRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, data: FiniteFunctor_desc) -> FiniteFunctor[Any, Any, Any, Any]:
        ...

    @abstractmethod
    def save(self, h: IOHelper, f: FiniteFunctor[Any, Any, Any, Any]) -> FiniteFunctor_desc:
        ...
