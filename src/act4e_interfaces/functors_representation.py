from abc import ABC, abstractmethod
from typing import Any, TypedDict

from .categories_representation import FiniteCategory_desc
from .functors import FiniteFunctor
from .helper import IOHelper
from .maps_representation import FiniteMap_desc

__all__ = ["FiniteFunctor_desc", "FiniteFunctorRepresentation"]


class FiniteFunctor_desc(TypedDict):
    source: FiniteCategory_desc
    target: FiniteCategory_desc
    f_ob: FiniteMap_desc
    f_mor: FiniteMap_desc


class FiniteFunctorRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, data: FiniteFunctor_desc) -> FiniteFunctor[Any, Any, Any, Any]:
        ...

    @abstractmethod
    def save(self, h: IOHelper, f: FiniteFunctor[Any, Any, Any, Any]) -> FiniteFunctor_desc:
        ...
