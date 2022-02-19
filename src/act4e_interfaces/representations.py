from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, List, TypeVar, Union

from typing_extensions import TypedDict

from .categories import (
    FiniteAdjunction,
    FiniteFunctor,
    FiniteNaturalTransformation,
    FiniteProfunctor,
)
from .dps import FiniteDP
from .finite_maps import FiniteMap
from .helper import IOHelper
from .posets import FinitePoset
from .relations import FiniteRelation
from .semigroups import FiniteGroup, FiniteMonoid, FiniteSemigroup
from .sets import FiniteSet
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
    "FiniteDP_desc",
]

E = TypeVar("E")
E1 = TypeVar("E1")
E2 = TypeVar("E2")


class DirectElements_desc(TypedDict):
    elements: List[ConcreteRepr]


class FiniteSetProduct_desc(TypedDict):
    # product: List[FiniteSet_desc] # cannot be recursive
    product: List[Any]


class FiniteSetDisjointUnion_desc(TypedDict):
    # disunion: List[FiniteSet_desc]  # cannot be recursive
    disunion: List[Any]


class FiniteSetUnion_desc(TypedDict):
    # union: List[FiniteSet_desc]  # cannot be recursive
    union: List[Any]


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
    def load(self, h: IOHelper, s: FiniteMap_desc) -> FiniteMap[Any, Any]:
        ...

    @abstractmethod
    def save(self, h: IOHelper, m: FiniteMap[Any, Any]) -> FiniteMap_desc:
        ...


class FiniteSetRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, data: FiniteSet_desc) -> FiniteSet[Any]:
        """Load a finite set from data structure.
        Throw InvalidFormat if the format is incorrect.
        """

    @abstractmethod
    def save(self, h: IOHelper, f: FiniteSet[Any]) -> FiniteSet_desc:
        """Serializes into a data structure"""


class FiniteSemigroupRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, s: FiniteSemigroup_desc) -> FiniteSemigroup[Any]:
        """Load the data"""

    @abstractmethod
    def save(self, h: IOHelper, m: FiniteSemigroup[Any]) -> FiniteSemigroup_desc:
        """Save the data"""


class FiniteNaturalTransformation_desc(TypedDict):
    pass


class FiniteMonoidRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, s: FiniteMonoid_desc) -> FiniteMonoid[Any]:
        """Load the data"""

    @abstractmethod
    def save(self, h: IOHelper, m: FiniteMonoid[Any]) -> FiniteMonoid_desc:
        """Save the data"""


class FiniteGroupRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, s: FiniteGroup_desc) -> FiniteGroup[Any]:
        """Load the data"""

    @abstractmethod
    def save(self, h: IOHelper, m: FiniteGroup[Any]) -> FiniteGroup_desc:
        """Save the data"""


class FinitePosetRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, s: FinitePoset_desc) -> FinitePoset[Any]:
        """Load the data"""

    @abstractmethod
    def save(self, h: IOHelper, m: FinitePoset[Any]) -> FinitePoset_desc:
        """Save the data"""


class FiniteRelationRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, data: FiniteRelation_desc) -> FiniteRelation[Any, Any]:
        """Load a finite set from given YAML data"""

    @abstractmethod
    def save(self, h: IOHelper, f: FiniteRelation[Any, Any]) -> FiniteRelation_desc:
        """Load a finite set from given YAML data"""


class FiniteCategory_desc(TypedDict):
    pass


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


class FiniteAdjunction_desc(TypedDict):
    pass


class FiniteAdjunctionRepresentation(ABC):
    @abstractmethod
    def load(self, h: IOHelper, data: FiniteAdjunction_desc) -> FiniteAdjunction[Any, Any, Any, Any]:
        ...

    @abstractmethod
    def save(self, h: IOHelper, f: FiniteAdjunction[Any, Any, Any, Any]) -> FiniteAdjunction_desc:
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
    def load(self, yaml_data: FiniteDP_desc) -> FiniteDP[Any, Any]:
        ...

    @abstractmethod
    def save(self, f: FiniteDP[Any, Any]) -> FiniteDP_desc:
        ...
