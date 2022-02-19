from abc import ABC, abstractmethod
from typing import Any, TypedDict

from .helper import IOHelper
from .natural import FiniteNaturalTransformation

__all__ = ["FiniteNaturalTransformationRepresentation", "FiniteNaturalTransformation_desc"]


class FiniteNaturalTransformation_desc(TypedDict):
    pass


class FiniteNaturalTransformationRepresentation(ABC):
    @abstractmethod
    def load(
        self, h: IOHelper, data: FiniteNaturalTransformation_desc
    ) -> FiniteNaturalTransformation[Any, Any, Any, Any]:
        ...

    @abstractmethod
    def save(
        self, h: IOHelper, f: FiniteNaturalTransformation[Any, Any, Any, Any]
    ) -> FiniteNaturalTransformation_desc:
        ...
