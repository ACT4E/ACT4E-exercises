from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, overload, TypedDict, Union

from .finite import (
    FiniteAdjunction,
    FiniteMap,
    FiniteMonoid,
    FiniteNaturalTransformation,
    FinitePoset,
    FiniteProfunctor,
    FiniteRelation,
    FiniteSemigroup,
    FiniteSet,
    FiniteSetDisjointUnion,
    FiniteSetProduct,
)

__all__ = [
    "FiniteSet_desc",
    "FiniteMap_desc",
    "FiniteSetUnion_desc",
    "FiniteSetProduct_desc",
    "FiniteSetDisjointUnion_desc",
    "DirectElements_desc",
    "FiniteSetRepresentation",
    "FiniteMapRepresentation",
    "IOHelper",
    "FiniteSemigroup_desc",
    "FiniteGroup_desc",
    "FiniteMonoid_desc",
    "FiniteAdjunctionRepresentation",
    "FinitePosetRepresentation",
    "FiniteNaturalTransformationRepresentation",
    "FiniteFunctorRepresentation",
    "FiniteRelationRepresentation",
    "FiniteProfunctorRepresentation",
    "FiniteMonoidRepresentation",
    "FiniteSemigroupRepresentation",
]


class IOHelper(ABC):
    @abstractmethod
    def loadfile(self, name: str) -> dict:
        """ Load from the filesystem. """


class DirectElements_desc(TypedDict):
    elements: List[object]


class FiniteSetProduct_desc(TypedDict):
    product_components: List[FiniteSet_desc]


class FiniteSetDisjointUnion_desc(TypedDict):
    disunion_components: List[FiniteSet_desc]


class FiniteSetUnion_desc(TypedDict):
    union_components: List[FiniteSet_desc]


FiniteSet_desc = Union[
    DirectElements_desc,
    FiniteSetProduct_desc,
    FiniteSetUnion_desc,
    FiniteSetDisjointUnion_desc,
]


class FiniteMap_desc(TypedDict):
    source: FiniteSet_desc
    target: FiniteSet_desc
    values: List[List[object]]


class FiniteSemigroup_desc(TypedDict):
    carrier: FiniteSet_desc
    compose: FiniteMap_desc


class FiniteMonoid_desc(TypedDict):
    carrier: FiniteSet_desc
    compose: FiniteMap_desc
    neutral: object


class FiniteGroup_desc(TypedDict):
    carrier: FiniteSet_desc
    compose: FiniteMap_desc
    neutral: object
    inv: FiniteMap_desc


class FiniteMapRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, s: FiniteMap_desc) -> FiniteMap:
        ...

    @abstractmethod
    def save(self, h: IOHelper, m: FiniteMap) -> FiniteMap_desc:
        ...


class FiniteSetRepresentation(ABC):
    @overload
    def load(
        self, h: IOHelper, data: FiniteSetDisjointUnion_desc
    ) -> FiniteSetDisjointUnion:
        ...

    @overload
    def load(self, h: IOHelper, data: FiniteSetUnion_desc) -> FiniteSet:
        ...

    @overload
    def load(self, h: IOHelper, data: FiniteSetProduct_desc) -> FiniteSetProduct:
        ...

    @abstractmethod
    def load(self, h: IOHelper, data: FiniteSet_desc) -> FiniteSet:
        """
        Load a finite set from data structure.
        Throw InvalidFormat if the format is incorrect.
        """

    @abstractmethod
    def save(self, h: IOHelper, f: FiniteSet) -> FiniteSet_desc:
        """ Serializes into a data structure """


class FiniteRelationRepresentation(ABC):
    @abstractmethod
    def load(self, yaml_data: str) -> FiniteRelation:
        """ Load a finite set from given YAML data"""

    @abstractmethod
    def save(self, f: FiniteRelation) -> str:
        """ Load a finite set from given YAML data"""


class FiniteSemigroupRepresentation(ABC):
    @abstractmethod
    def load(self, s: str) -> FiniteSemigroup:
        """ Load the data  """

    @abstractmethod
    def save(self, m: FiniteSemigroup) -> str:
        """ Save the data  """


class FiniteMonoidRepresentation(ABC):
    @abstractmethod
    def load(self, s: str) -> FiniteMonoid:
        """ Load the data  """

    @abstractmethod
    def save(self, m: FiniteMonoid) -> str:
        """ Save the data  """


class FinitePosetRepresentation(ABC):
    @abstractmethod
    def load(self, s: str) -> FinitePoset:
        """ Load the data  """

    @abstractmethod
    def save(self, m: FinitePoset) -> str:
        """ Save the data  """


class FiniteFunctorRepresentation(ABC):
    @abstractmethod
    def load(self, yaml_data: str) -> FiniteFunctor:
        """ Load a functor from given YAML data"""

    @abstractmethod
    def save(self, f: FiniteFunctor) -> str:
        ...


class FiniteNaturalTransformationRepresentation(ABC):
    @abstractmethod
    def load(self, yaml_data: str) -> FiniteNaturalTransformation:
        """ Load a natural transformation from given YAML data"""

    @abstractmethod
    def save(self, f: FiniteNaturalTransformation) -> str:
        ...


class FiniteAdjunctionRepresentation(ABC):
    @abstractmethod
    def load(self, yaml_data: str) -> FiniteAdjunction:
        ...

    @abstractmethod
    def save(self, f: FiniteAdjunction) -> str:
        ...


class FiniteProfunctorRepresentation(ABC):
    @abstractmethod
    def load(self, yaml_data: str) -> FiniteProfunctor:
        """ Load a natural transformation from given YAML data"""

    @abstractmethod
    def save(self, f: FiniteProfunctor) -> str:
        ...
