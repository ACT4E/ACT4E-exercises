from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, overload, TypedDict, Union

from .finite import (FiniteAdjunction, FiniteFunctor, FiniteGroup, FiniteMap, FiniteMonoid,
                     FiniteNaturalTransformation, FinitePoset, FiniteProfunctor, FiniteRelation,
                     FiniteSemigroup, FiniteSet, FiniteSetDisjointUnion, FiniteSetProduct)

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


class FiniteMapRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, s: FiniteMap_desc) -> FiniteMap:
        ...

    @abstractmethod
    def save(self, h: IOHelper, m: FiniteMap) -> FiniteMap_desc:
        ...


class FiniteSetRepresentation(ABC):
    # @overload
    # def load(self, h: IOHelper, data: FiniteSetDisjointUnion_desc) \
    #     -> FiniteSetDisjointUnion:
    #     ...
    #
    # @overload
    # def load(self, h: IOHelper, data: FiniteSetUnion_desc) -> FiniteSet:
    #     ...
    #
    # @overload
    # def load(self, h: IOHelper, data: FiniteSetProduct_desc) -> FiniteSetProduct:
    #     ...

    @abstractmethod
    def load(self, h: IOHelper, data: FiniteSet_desc) -> FiniteSet:
        """ Load a finite set from data structure.
            Throw InvalidFormat if the format is incorrect.
        """

    @abstractmethod
    def save(self, h: IOHelper, f: FiniteSet) -> FiniteSet_desc:
        """ Serializes into a data structure """


class FiniteSemigroup_desc(TypedDict):
    carrier: FiniteSet_desc
    compose: FiniteMap_desc


class FiniteSemigroupRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, s: FiniteSemigroup_desc) -> FiniteSemigroup:
        """ Load the data  """

    @abstractmethod
    def save(self, h: IOHelper, m: FiniteSemigroup) -> FiniteSemigroup_desc:
        """ Save the data  """


class FiniteMonoid_desc(FiniteSemigroup_desc):
    # carrier: FiniteSet_desc
    # compose: FiniteMap_desc
    neutral: object


class FiniteMonoidRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, s: FiniteMonoid_desc) -> FiniteMonoid:
        """ Load the data  """

    @abstractmethod
    def save(self, h: IOHelper, m: FiniteMonoid) -> FiniteMonoid_desc:
        """ Save the data  """


class FiniteGroup_desc(FiniteMonoid_desc):
    # carrier: FiniteSet_desc
    # compose: FiniteMap_desc
    # neutral: object
    inv: FiniteMap_desc


class FiniteGroupRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, s: FiniteGroup_desc) -> FiniteGroup:
        """ Load the data  """

    @abstractmethod
    def save(self, h: IOHelper, m: FiniteGroup) -> FiniteGroup_desc:
        """ Save the data  """


class FinitePosetRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, s: str) -> FinitePoset:
        """ Load the data  """

    @abstractmethod
    def save(self, h: IOHelper, m: FinitePoset) -> str:
        """ Save the data  """


class FiniteRelation_desc(TypedDict):
    source: FiniteSet_desc
    target: FiniteSet_desc
    values: List[List[object]]


class FiniteRelationRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, data: FiniteRelation_desc) -> FiniteRelation:
        """ Load a finite set from given YAML data"""

    @abstractmethod
    def save(self, h: IOHelper, f: FiniteRelation) -> FiniteRelation_desc:
        """ Load a finite set from given YAML data"""


class FiniteCategory_desc(TypedDict):
    ...


class FiniteFunctor_desc(TypedDict):
    source: FiniteCategory_desc
    target: FiniteCategory_desc
    f_ob: FiniteMap
    f_mor: FiniteMap


class FiniteFunctorRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, data: FiniteFunctor_desc) -> FiniteFunctor:
        ...

    @abstractmethod
    def save(self, h: IOHelper, f: FiniteFunctor) -> FiniteFunctor_desc:
        ...


class FiniteNaturalTransformationRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, data: str) -> FiniteNaturalTransformation:
        ...

    @abstractmethod
    def save(self, h: IOHelper, f: FiniteNaturalTransformation) -> str:
        ...


class FiniteAdjunction_desc(TypedDict):
    ...


class FiniteAdjunctionRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, data: FiniteAdjunction_desc) -> FiniteAdjunction:
        ...

    @abstractmethod
    def save(self, h: IOHelper, f: FiniteAdjunction) -> FiniteAdjunction_desc:
        ...


class FiniteProfunctor_desc(TypedDict):
    ...


class FiniteProfunctorRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, data: FiniteProfunctor_desc) -> FiniteProfunctor:
        ...

    @abstractmethod
    def save(self, h: IOHelper, f: FiniteProfunctor) -> FiniteProfunctor_desc:
        ...
