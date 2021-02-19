from abc import ABC, abstractmethod
from typing import Optional, Set, Tuple

from .types import Element, Morphism, Object


class FiniteSet(ABC):
    """ A finite set has a finite size. """

    @abstractmethod
    def size(self) -> int:
        """ Return the size of the finite set. """

    @abstractmethod
    def belongs(self, x: Element) -> bool:
        ...

    @abstractmethod
    def equal(self, x: Element, y: Element) -> bool:
        """ Returns True if the two elements are to be considered equal. """


class FiniteSetRepresentation(ABC):

    @classmethod
    @abstractmethod
    def load(cls, yaml_data: str) -> FiniteSet:
        """ Load a finite set from given YAML data"""

    @classmethod
    @abstractmethod
    def save(cls, f: FiniteSet) -> str:
        """ Load a finite set from given YAML data"""


class FiniteSetProperties(ABC):

    @classmethod
    @abstractmethod
    def is_subset(cls, a: FiniteSet, b: FiniteSet) -> bool:
        ...


class FiniteSetOperations(ABC):

    @classmethod
    @abstractmethod
    def union(cls, s1: FiniteSet, s2: FiniteSet) -> FiniteSet:
        ...

    @classmethod
    @abstractmethod
    def intersection(cls, s1: FiniteSet, s2: FiniteSet) -> FiniteSet:
        ...

    @classmethod
    @abstractmethod
    def product(cls, s1: FiniteSet, s2: FiniteSet) -> FiniteSet:
        ...

    @classmethod
    @abstractmethod
    def disjoint_union(cls, s1: FiniteSet, s2: FiniteSet) -> FiniteSet:
        ...


class FiniteRelation(ABC):

    @abstractmethod
    def source(self) -> FiniteSet:
        """ Returns a finite set"""

    @abstractmethod
    def target(self) -> FiniteSet:
        """ Returns a finite set"""

    @abstractmethod
    def holds(self, a: Element, b: Element) -> bool:
        """ Returns true if the two elements are related """


class FiniteRelationRepresentation(ABC):

    @classmethod
    @abstractmethod
    def load(cls, yaml_data: str) -> FiniteRelation:
        """ Load a finite set from given YAML data"""

    @classmethod
    @abstractmethod
    def save(cls, f: FiniteRelation) -> str:
        """ Load a finite set from given YAML data"""


class FiniteRelationProperties(ABC):

    @classmethod
    @abstractmethod
    def is_surjective(cls, fr: FiniteRelation) -> bool:
        """ Return True if the relation is surjective. """

    @classmethod
    @abstractmethod
    def is_injective(cls, fr: FiniteRelation) -> bool:
        """ Return True if the relation is injective. """

    @classmethod
    @abstractmethod
    def is_defined_everywhere(cls, fr: FiniteRelation) -> bool:
        """ Return True if the relation is defined everywhere. """

    @classmethod
    @abstractmethod
    def is_single_valued(cls, fr: FiniteRelation) -> bool:
        """ Return True if the relation is single-valued """


class FiniteRelationOperations(ABC):

    @classmethod
    @abstractmethod
    def transpose(cls, fr: FiniteRelation) -> FiniteRelation:
        """ Create the transposed of a relation """


class FiniteEndorelationProperties(ABC):
    @classmethod
    @abstractmethod
    def is_reflexive(cls, fr: FiniteRelation) -> bool:
        """ Return True if the relation is reflexive. """

    @classmethod
    @abstractmethod
    def is_irreflexive(cls, fr: FiniteRelation) -> bool:
        """ Return True if the relation is irreflexive. """

    @classmethod
    @abstractmethod
    def is_transitive(cls, fr: FiniteRelation) -> bool:
        """ Return True if the relation is transitive. """

    @classmethod
    @abstractmethod
    def is_symmetric(cls, fr: FiniteRelation) -> bool:
        """ Return True if the relation is symmetric  """

    @classmethod
    @abstractmethod
    def is_antisymmetric(cls, fr: FiniteRelation) -> bool:
        """ Return True if the relation is antisymmetric  """

    @classmethod
    @abstractmethod
    def is_asymmetric(cls, fr: FiniteRelation) -> bool:
        """ Return True if the relation is asymmetric  """


class FiniteEndorelationOperations(ABC):
    @classmethod
    @abstractmethod
    def transitive_closure(cls, fr: FiniteRelation) -> FiniteRelation:
        """ Returns transitive closure """


class FiniteMap(ABC):

    @abstractmethod
    def source(self) -> FiniteSet:
        """ Returns a finite set"""

    @abstractmethod
    def target(self) -> FiniteSet:
        """ Returns a finite set"""

    @abstractmethod
    def exec(self, a: Element) -> Element:
        ...


class FiniteMapRepresentation(ABC):
    @classmethod
    @abstractmethod
    def load(cls, s: str) -> FiniteMap:
        """ Load the data  """

    @classmethod
    @abstractmethod
    def save(cls, m: FiniteMap) -> str:
        """ Load the data  """


class FiniteMapOperations(ABC):
    @classmethod
    @abstractmethod
    def compose(cls, f: FiniteMap, g: FiniteMap) -> FiniteMap:
        """ compose two functions"""

    @classmethod
    @abstractmethod
    def as_relation(cls, f: FiniteMap) -> FiniteRelation:
        """ Load the data  """


class FiniteSemigroup(ABC):

    @abstractmethod
    def carrier(self) -> FiniteSet:
        ...

    @abstractmethod
    def compose(self, a: Element, b: Element) -> Element:
        ...


class FiniteSemigroupRepresentation(ABC):
    @classmethod
    @abstractmethod
    def load(cls, s: str) -> FiniteSemigroup:
        """ Load the data  """

    @classmethod
    @abstractmethod
    def save(cls, m: FiniteSemigroup) -> str:
        """ Save the data  """


class FiniteMonoid(FiniteSemigroup, ABC):

    @abstractmethod
    def identity(self) -> Element:
        ...


class FiniteMonoidRepresentation(ABC):
    @classmethod
    @abstractmethod
    def load(cls, s: str) -> FiniteMonoid:
        """ Load the data  """

    @classmethod
    @abstractmethod
    def save(cls, m: FiniteMonoid) -> str:
        """ Save the data  """


# TODO: equational theotires

class FinitePoset(ABC):
    """ Implementation of finite posets. """

    @abstractmethod
    def carrier(self) -> FiniteSet:
        ...

    @abstractmethod
    def leq(self, x: Element, y: Element) -> bool:
        """ Implement $\posleq$ """


class FinitePosetRepresentation(ABC):
    @classmethod
    @abstractmethod
    def load(cls, s: str) -> FiniteSemigroup:
        """ Load the data  """

    @classmethod
    @abstractmethod
    def save(cls, m: FiniteSemigroup) -> str:
        """ Save the data  """


class FinitePosetProperties(ABC):
    @classmethod
    @abstractmethod
    def width(cls, fp: FinitePoset) -> int:
        """ Return the width of the poset. """

    @classmethod
    @abstractmethod
    def height(cls, fp: FinitePoset) -> int:
        """ Return the height of the poset. """


class FinitePosetConstructors(ABC):
    @classmethod
    @abstractmethod
    def powerset(cls, s: FiniteSet) -> FinitePoset:
        """ Creates the powerset poset """

    @classmethod
    @abstractmethod
    def uppersets(cls, s: FinitePoset) -> FinitePoset:
        """ Creates the upperset poset """

    @classmethod
    @abstractmethod
    def lowersets(cls, s: FinitePoset) -> FinitePoset:
        """ Creates the lowersets poset """

    @classmethod
    @abstractmethod
    def antichains(cls, s: FinitePoset) -> FiniteSet:
        """ Creates the antichain set """


class FinitePosetSubsetProperties(ABC):
    @classmethod
    @abstractmethod
    def is_chain(cls, fp: FinitePoset, s: FiniteSet) -> bool:
        """ Computes if the subset is a chain. """

    @classmethod
    @abstractmethod
    def is_antichain(cls, fp: FinitePoset, s: FiniteSet) -> bool:
        """ Computes if the subset is an antichain. """


class FinitePosetSubsetOperations(ABC):
    @classmethod
    @abstractmethod
    def upperclosure(cls, fp: FinitePoset, s: Set[Element]) -> Set[Element]:
        """ Computes the upper closure of an element"""

    @classmethod
    @abstractmethod
    def lowerclosure(cls, fp: FinitePoset, s: Set[Element]) -> Set[Element]:
        """ Computes the lower closure of an element"""

    @classmethod
    @abstractmethod
    def maximal(cls, fp: FinitePoset, s: Set[Element]) -> Set[Element]:
        """ Computes the maximal elements in a subset of the poset"""

    @classmethod
    @abstractmethod
    def minimal(cls, fp: FinitePoset, s: Set[Element]) -> Set[Element]:
        """ Computes the minimal elements in a subset of the poset"""

    @classmethod
    @abstractmethod
    def infimum(cls, fp: FinitePoset, s: Set[Element]) -> Optional[Element]:
        """ Computes the infimum for the subset, or None if one does not exist. """

    @classmethod
    @abstractmethod
    def supremum(cls, fp: FinitePoset, s: Set[Element]) -> Optional[Element]:
        """ Computes the supremum for the subset, or None if one does not exist. """

    @classmethod
    @abstractmethod
    def meet(cls, fp: FinitePoset, s: Set[Element]) -> Optional[Element]:
        """ Computes the meet for the subset, or None if one does not exist. """

    @classmethod
    @abstractmethod
    def join(cls, fp: FinitePoset, s: Set[Element]) -> Optional[Element]:
        """ Computes the join for the subset, or None if one does not exist. """


class FinitePosetOperations(ABC):
    @classmethod
    @abstractmethod
    def opposite(cls, s: str) -> FinitePoset:
        ...

    @classmethod
    @abstractmethod
    def product(cls, p1: FinitePoset, p2: FinitePoset) -> FinitePoset:
        ...

    @classmethod
    @abstractmethod
    def disjoint_union(cls, p1: FinitePoset, p2: FinitePoset) -> FinitePoset:
        ...


class FinitePosetMapProperties(ABC):
    @classmethod
    @abstractmethod
    def is_monotone(cls, fp: FinitePoset, m: FiniteMap) -> bool:
        """ Check if a map is monotone. """

    @classmethod
    @abstractmethod
    def is_antitone(cls, fp: FinitePoset, m: FiniteMap) -> bool:
        """ Check if a map is antitone. """


class FiniteMeetSemilattice:
    @abstractmethod
    def meet(self, x: Element, y: Element) -> Element:
        ...

    @abstractmethod
    def top(self) -> Element:
        ...


class FiniteJoinSemilattice:
    @abstractmethod
    def join(self, x: Element, y: Element) -> Element:
        ...

    @abstractmethod
    def bottom(self) -> Element:
        ...


class FiniteLattice(FiniteMeetSemilattice, FiniteJoinSemilattice, ABC):
    ...


class FiniteCategory(ABC):

    @abstractmethod
    def objects(self) -> FiniteSet:
        ...

    @abstractmethod
    def homs(self, ob1: Object, ob2: Object) -> FiniteSet:
        ...

    @abstractmethod
    def legs(self, m: Morphism) -> Tuple[Object, Object]:
        """ Return source and target of the morphism """


class FiniteFunctor(ABC):

    @abstractmethod
    def source(self) -> FiniteCategory:
        ...

    @abstractmethod
    def target(self) -> FiniteCategory:
        ...

    @abstractmethod
    def f_ob(self, ob: Object) -> Object:
        """ Effect on objects """

    @abstractmethod
    def f_mor(self, m: Morphism) -> Morphism:
        """ Effect on morphisms """


class FiniteFunctorRepresentation(ABC):

    @classmethod
    @abstractmethod
    def load(cls, yaml_data: str) -> FiniteFunctor:
        """ Load a functor from given YAML data"""

    @classmethod
    @abstractmethod
    def save(cls, f: FiniteFunctor) -> str:
        ...

class FiniteNaturalTransformation(ABC):

    @abstractmethod
    def cat1(self) -> FiniteCategory:
        ...

    @abstractmethod
    def cat2(self) -> FiniteCategory:
        ...

    @abstractmethod
    def component(self, ob: Object) -> Morphism:
        """ Returns the component for a particular object in the first category.
            This is a morphism in the second category.
        """


class FiniteNaturalTransformationRepresentation(ABC):

    @classmethod
    @abstractmethod
    def load(cls, yaml_data: str) -> FiniteNaturalTransformation:
        """ Load a natural transformation from given YAML data"""

    @classmethod
    @abstractmethod
    def save(cls, f: FiniteNaturalTransformation) -> str:
        ...


class FiniteAdjunction(ABC):

    def cat1(self) -> FiniteCategory:
        ...
    def cat2(self) -> FiniteCategory:
        ...
    def left(self) -> FiniteFunctor:
        pass

    def right(self) -> FiniteFunctor:
        pass


class FiniteAdjunctionRepresentation(ABC):

    @classmethod
    @abstractmethod
    def load(cls, yaml_data: str) -> FiniteAdjunction:
        """ Load a natural transformation from given YAML data"""

    @classmethod
    @abstractmethod
    def save(cls, f: FiniteAdjunction) -> str:
        ...





class FiniteAdjunctionsOperations(ABC):

    @classmethod
    @abstractmethod
    def is_adjunction(cls, left: FiniteFunctor,
                      right: FiniteFunctor) -> bool:
        """ check the pair is an adjunction """

    @classmethod
    @abstractmethod
    def compose(cls, adj1: FiniteAdjunction,
                adj2: FiniteAdjunction) -> FiniteAdjunction:

        """ compose two compatible adjunctions"""

    @classmethod
    @abstractmethod
    def from_relation(cls, f: FiniteRelation) -> FiniteAdjunction:
        ...
