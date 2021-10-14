from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, TypeVar, Union

from typing_extensions import TypedDict

from .categories import (
    FiniteAdjunction,
    FiniteDP,
    FiniteFunctor,
    FiniteNaturalTransformation,
    FiniteProfunctor,
)
from .helper import IOHelper
from .posets import FinitePoset
from .relations import FiniteRelation
from .semigroups import FiniteGroup, FiniteMonoid, FiniteSemigroup
from .sets import FiniteMap, FiniteSet
from .types import ConcreteRepr

__all__ = [
    "FiniteSet_desc",
    "FiniteMap_desc",
    "FiniteSetUnion_desc",
    "FiniteSetProduct_desc",
    "FiniteSetDisjointUnion_desc",
    "DirectElements_desc",
    "FiniteProfunctor_desc",
    "FiniteNaturalTransformation_desc",
    "IOHelper",
    "FiniteRelation_desc",
    "FiniteFunctor_desc",
    "FiniteSemigroup_desc",
    "FiniteGroup_desc",
    "FiniteMonoid_desc",
    "FiniteSetRepresentation",
    "FiniteMapRepresentation",
    "FiniteAdjunction_desc",
    "FiniteGroupRepresentation",
    "FiniteAdjunctionRepresentation",
    "FinitePosetRepresentation",
    "FiniteNaturalTransformationRepresentation",
    "FiniteFunctorRepresentation",
    "FiniteRelationRepresentation",
    "FiniteProfunctorRepresentation",
    "FiniteMonoidRepresentation",
    "FiniteSemigroupRepresentation",
    "FiniteDPRepresentation",
    "FiniteMap_desc",
    "FinitePoset_desc",
]

E = TypeVar("E")
E1 = TypeVar("E1")
E2 = TypeVar("E2")


class DirectElements_desc(TypedDict):
    elements: List[ConcreteRepr]


class FiniteSetProduct_desc(TypedDict):
    product: List[FiniteSet_desc]


class FiniteSetDisjointUnion_desc(TypedDict):
    disunion: List[FiniteSet_desc]


class FiniteSetUnion_desc(TypedDict):
    union: List[FiniteSet_desc]


FiniteSet_desc = Union[
    DirectElements_desc,
    FiniteSetProduct_desc,
    FiniteSetUnion_desc,
    FiniteSetDisjointUnion_desc,
]


class FiniteMap_desc(TypedDict):
    source: FiniteSet_desc
    target: FiniteSet_desc
    values: List[List[ConcreteRepr]]


class FiniteRelation_desc(TypedDict):
    source: FiniteSet_desc
    target: FiniteSet_desc
    values: List[List[ConcreteRepr]]


class FinitePoset_desc(TypedDict):
    carrier: FiniteSet_desc
    hasse: List[List[ConcreteRepr]]


class FiniteSemigroup_desc(TypedDict):
    carrier: FiniteSet_desc
    composition: List[List[ConcreteRepr]]


class FiniteMonoid_desc(FiniteSemigroup_desc):
    neutral: ConcreteRepr


class FiniteGroup_desc(FiniteMonoid_desc):
    inverse: List[List[ConcreteRepr]]


class FiniteMapRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, s: FiniteMap_desc) -> FiniteMap[E1, E2]:
        ...

    @abstractmethod
    def save(self, h: IOHelper, m: FiniteMap[E1, E2]) -> FiniteMap_desc:
        ...


class FiniteSetRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, data: FiniteSet_desc) -> FiniteSet[E]:
        """Load a finite set from data structure.
        Throw InvalidFormat if the format is incorrect.
        """

    @abstractmethod
    def save(self, h: IOHelper, f: FiniteSet[E]) -> FiniteSet_desc:
        """ Serializes into a data structure """


class FiniteSemigroupRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, s: FiniteSemigroup_desc) -> FiniteSemigroup[E]:
        """ Load the data  """

    @abstractmethod
    def save(self, h: IOHelper, m: FiniteSemigroup[E]) -> FiniteSemigroup_desc:
        """ Save the data  """


class FiniteNaturalTransformation_desc(TypedDict):
    pass


class FiniteMonoidRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, s: FiniteMonoid_desc) -> FiniteMonoid[E]:
        """ Load the data  """

    @abstractmethod
    def save(self, h: IOHelper, m: FiniteMonoid[E]) -> FiniteMonoid_desc:
        """ Save the data  """


class FiniteGroupRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, s: FiniteGroup_desc) -> FiniteGroup[E]:
        """ Load the data  """

    @abstractmethod
    def save(self, h: IOHelper, m: FiniteGroup[E]) -> FiniteGroup_desc:
        """ Save the data  """


class FinitePosetRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, s: FinitePoset_desc) -> FinitePoset[E]:
        """ Load the data  """

    @abstractmethod
    def save(self, h: IOHelper, m: FinitePoset[E]) -> FinitePoset_desc:
        """ Save the data  """


class FiniteRelationRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, data: FiniteRelation_desc) -> FiniteRelation[E1, E2]:
        """ Load a finite set from given YAML data"""

    @abstractmethod
    def save(self, h: IOHelper, f: FiniteRelation[E1, E2]) -> FiniteRelation_desc:
        """ Load a finite set from given YAML data"""


class FiniteCategory_desc(TypedDict):
    pass


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
    def load(self, h: IOHelper, data: FiniteNaturalTransformation_desc) -> FiniteNaturalTransformation:
        ...

    @abstractmethod
    def save(self, h: IOHelper, f: FiniteNaturalTransformation) -> FiniteNaturalTransformation_desc:
        ...


class FiniteAdjunction_desc(TypedDict):
    pass


class FiniteAdjunctionRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, data: FiniteAdjunction_desc) -> FiniteAdjunction:
        ...

    @abstractmethod
    def save(self, h: IOHelper, f: FiniteAdjunction) -> FiniteAdjunction_desc:
        ...


class FiniteProfunctor_desc(TypedDict):
    pass


class FiniteProfunctorRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, data: FiniteProfunctor_desc) -> FiniteProfunctor:
        ...

    @abstractmethod
    def save(self, h: IOHelper, f: FiniteProfunctor) -> FiniteProfunctor_desc:
        ...


class FiniteDP_desc(TypedDict):
    F: FinitePoset_desc
    R: FinitePoset_desc
    I: FiniteSet_desc
    feas: List[List[ConcreteRepr]]


class FiniteDPRepresentation(ABC):
    @abstractmethod
    def load(self, yaml_data: FiniteDP_desc) -> FiniteDP:
        ...

    @abstractmethod
    def save(self, f: FiniteDP) -> FiniteDP_desc:
        ...
