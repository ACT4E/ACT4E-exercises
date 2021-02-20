from abc import ABC, abstractmethod
from typing import Collection, Optional, Set, Tuple

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

    @abstractmethod
    def elements(self) -> Collection[Element]:
        ...


class InvalidFormat(Exception):
    pass


class FiniteSetRepresentation(ABC):

    @abstractmethod
    def load(self, yaml_data: str) -> FiniteSet:
        """ Load a finite set from given YAML data.
            Throw InvalidFormat if the format is incorrect.
        """

    @abstractmethod
    def save(self, f: FiniteSet) -> str:
        """ Save to a string. """


class FiniteSetProperties(ABC):

    @abstractmethod
    def is_subset(self, a: FiniteSet, b: FiniteSet) -> bool:
        ...


class FiniteSetOperations(ABC):

    @abstractmethod
    def union(self, s1: FiniteSet, s2: FiniteSet) -> FiniteSet:
        ...

    @abstractmethod
    def intersection(self, s1: FiniteSet, s2: FiniteSet) -> FiniteSet:
        ...

    @abstractmethod
    def product(self, s1: FiniteSet, s2: FiniteSet) -> FiniteSet:
        ...

    @abstractmethod
    def disjoint_union(self, s1: FiniteSet, s2: FiniteSet) -> FiniteSet:
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

    @abstractmethod
    def load(self, yaml_data: str) -> FiniteRelation:
        """ Load a finite set from given YAML data"""

    @abstractmethod
    def save(self, f: FiniteRelation) -> str:
        """ Load a finite set from given YAML data"""


class FiniteRelationProperties(ABC):

    @abstractmethod
    def is_surjective(self, fr: FiniteRelation) -> bool:
        """ Return True if the relation is surjective. """

    @abstractmethod
    def is_injective(self, fr: FiniteRelation) -> bool:
        """ Return True if the relation is injective. """

    @abstractmethod
    def is_defined_everywhere(self, fr: FiniteRelation) -> bool:
        """ Return True if the relation is defined everywhere. """

    @abstractmethod
    def is_single_valued(self, fr: FiniteRelation) -> bool:
        """ Return True if the relation is single-valued """


class FiniteRelationOperations(ABC):

    @abstractmethod
    def transpose(self, fr: FiniteRelation) -> FiniteRelation:
        """ Create the transposed of a relation """


class FiniteEndorelationProperties(ABC):

    @abstractmethod
    def is_reflexive(self, fr: FiniteRelation) -> bool:
        """ Return True if the relation is reflexive. """

    @abstractmethod
    def is_irreflexive(self, fr: FiniteRelation) -> bool:
        """ Return True if the relation is irreflexive. """

    @abstractmethod
    def is_transitive(self, fr: FiniteRelation) -> bool:
        """ Return True if the relation is transitive. """

    @abstractmethod
    def is_symmetric(self, fr: FiniteRelation) -> bool:
        """ Return True if the relation is symmetric  """

    @abstractmethod
    def is_antisymmetric(self, fr: FiniteRelation) -> bool:
        """ Return True if the relation is antisymmetric  """

    @abstractmethod
    def is_asymmetric(self, fr: FiniteRelation) -> bool:
        """ Return True if the relation is asymmetric  """


class FiniteEndorelationOperations(ABC):

    @abstractmethod
    def transitive_closure(self, fr: FiniteRelation) -> FiniteRelation:
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

    @abstractmethod
    def load(self, s: str) -> FiniteMap:
        """ Load the data  """

    @abstractmethod
    def save(self, m: FiniteMap) -> str:
        """ Load the data  """


class FiniteMapOperations(ABC):

    @abstractmethod
    def compose(self, f: FiniteMap, g: FiniteMap) -> FiniteMap:
        """ compose two functions"""

    @abstractmethod
    def as_relation(self, f: FiniteMap) -> FiniteRelation:
        """ Load the data  """


class FiniteSemigroup(ABC):

    @abstractmethod
    def carrier(self) -> FiniteSet:
        ...

    @abstractmethod
    def compose(self, a: Element, b: Element) -> Element:
        ...


class FiniteSemigroupRepresentation(ABC):

    @abstractmethod
    def load(self, s: str) -> FiniteSemigroup:
        """ Load the data  """

    @abstractmethod
    def save(self, m: FiniteSemigroup) -> str:
        """ Save the data  """


class FiniteSemigroupConstruct(ABC):

    @abstractmethod
    def free(self, fs: FiniteSet) -> FiniteSemigroup:
        """ Construct the free semigroup on a set. """


class FiniteMonoid(FiniteSemigroup, ABC):

    @abstractmethod
    def identity(self) -> Element:
        ...


class FiniteMonoidRepresentation(ABC):

    @abstractmethod
    def load(self, s: str) -> FiniteMonoid:
        """ Load the data  """

    @abstractmethod
    def save(self, m: FiniteMonoid) -> str:
        """ Save the data  """


# TODO: equational theotires

class FinitePoset(ABC):
    """ Implementation of finite posets. """

    @abstractmethod
    def carrier(self) -> FiniteSet:
        ...

    @abstractmethod
    def leq(self, x: Element, y: Element) -> bool:
        """ Implements $\posleq$ """


class FinitePosetRepresentation(ABC):

    @abstractmethod
    def load(self, s: str) -> FinitePoset:
        """ Load the data  """

    @abstractmethod
    def save(self, m: FinitePoset) -> str:
        """ Save the data  """


class FinitePosetProperties(ABC):

    @abstractmethod
    def width(self, fp: FinitePoset) -> int:
        """ Return the width of the poset. """

    @abstractmethod
    def height(self, fp: FinitePoset) -> int:
        """ Return the height of the poset. """


class FinitePosetConstructors(ABC):

    @abstractmethod
    def discrete(self, s: FiniteSet) -> FinitePoset:
        """ Creates the discrete poset from any set. """

    @abstractmethod
    def powerset(self, s: FiniteSet) -> FinitePoset:
        """ Creates the powerset poset """

    @abstractmethod
    def uppersets(self, s: FinitePoset) -> FinitePoset:
        """ Creates the upperset poset """

    @abstractmethod
    def lowersets(self, s: FinitePoset) -> FinitePoset:
        """ Creates the lowersets poset """

    @abstractmethod
    def antichains(self, s: FinitePoset) -> FiniteSet:
        """ Creates the antichain set """

    @abstractmethod
    def intervals(self, s: FinitePoset) -> FinitePoset:
        """ Computes the poset of intervals. """

    @abstractmethod
    def intervals2(self, s: FinitePoset) -> FinitePoset:
        """ Computes the other of intervals. """


class FinitePosetSubsetProperties(ABC):

    @abstractmethod
    def is_chain(self, fp: FinitePoset, s: FiniteSet) -> bool:
        """ Computes if the subset is a chain. """

    @abstractmethod
    def is_antichain(self, fp: FinitePoset, s: FiniteSet) -> bool:
        """ Computes if the subset is an antichain. """


class FinitePosetSubsetOperations(ABC):

    @abstractmethod
    def upperclosure(self, fp: FinitePoset, s: Set[Element]) -> Set[Element]:
        """ Computes the upper closure of an element"""

    @abstractmethod
    def lowerclosure(self, fp: FinitePoset, s: Set[Element]) -> Set[Element]:
        """ Computes the lower closure of an element"""

    @abstractmethod
    def maximal(self, fp: FinitePoset, s: Set[Element]) -> Set[Element]:
        """ Computes the maximal elements in a subset of the poset"""

    @abstractmethod
    def minimal(self, fp: FinitePoset, s: Set[Element]) -> Set[Element]:
        """ Computes the minimal elements in a subset of the poset"""

    @abstractmethod
    def infimum(self, fp: FinitePoset, s: Set[Element]) -> Optional[Element]:
        """ Computes the infimum for the subset, or None if one does not exist. """

    @abstractmethod
    def supremum(self, fp: FinitePoset, s: Set[Element]) -> Optional[Element]:
        """ Computes the supremum for the subset, or None if one does not exist. """

    @abstractmethod
    def meet(self, fp: FinitePoset, s: Set[Element]) -> Optional[Element]:
        """ Computes the meet for the subset, or None if one does not exist. """

    @abstractmethod
    def join(self, fp: FinitePoset, s: Set[Element]) -> Optional[Element]:
        """ Computes the join for the subset, or None if one does not exist. """


class FinitePosetOperations(ABC):

    @abstractmethod
    def opposite(self, s: str) -> FinitePoset:
        ...

    @abstractmethod
    def product(self, p1: FinitePoset, p2: FinitePoset) -> FinitePoset:
        ...

    @abstractmethod
    def disjoint_union(self, p1: FinitePoset, p2: FinitePoset) -> FinitePoset:
        ...


class FiniteMonotoneMap(ABC):
    def source(self) -> FinitePoset:
        ...

    def target(self) -> FinitePoset:
        ...


class FiniteMonotoneMapProperties(ABC):

    @abstractmethod
    def is_monotone(self, p1: FinitePoset, p2: FinitePoset, m: FiniteMap) -> bool:
        """ Check if a map is monotone. """

    @abstractmethod
    def is_antitone(self, p1: FinitePoset, p2: FinitePoset, m: FiniteMap) -> bool:
        """ Check if a map is antitone. """


class FiniteMonoidalPoset(ABC):
    """ Implementation of finite posets. """

    @abstractmethod
    def poset(self) -> FinitePoset:
        ...

    @abstractmethod
    def monoid(self) -> FiniteMonoid:
        ...


class MonoidalPosetOperations(ABC):
    """ Implementation of finite posets. """

    @abstractmethod
    def is_monoidal_poset(self, fp: FinitePoset, fm: FiniteMonoid) -> bool:
        """ Check that the pair of poset and monoid make together a monoidal poset."""


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


class FiniteSemiCategory(ABC):

    @abstractmethod
    def objects(self) -> FiniteSet:
        ...

    @abstractmethod
    def homs(self, ob1: Object, ob2: Object) -> FiniteSet:
        ...

    @abstractmethod
    def legs(self, m: Morphism) -> Tuple[Object, Object]:
        """ Return source and target of the morphism """


class FiniteCategory(FiniteSemiCategory, ABC):

    @abstractmethod
    def identity(self, ob: Object) -> Morphism:
        """ Identity for the object """


class FiniteCategoryOperations:

    @abstractmethod
    def product(self, c1: FiniteCategory, c2: FiniteCategory) -> FiniteCategory:
        """ Product of two categories. """

    @abstractmethod
    def disjoint_union(self, c1: FiniteCategory, c2: FiniteCategory) -> FiniteCategory:
        """ Disjoint union for the categories """

    @abstractmethod
    def arrow(self, c1: FiniteCategory) -> FiniteCategory:
        """ Computes the arrow category """

    @abstractmethod
    def twisted_arrow(self, c1: FiniteCategory) -> FiniteCategory:
        """ Computes the twisted arrow category """


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

    @abstractmethod
    def load(self, yaml_data: str) -> FiniteFunctor:
        """ Load a functor from given YAML data"""

    @abstractmethod
    def save(self, f: FiniteFunctor) -> str:
        ...


class FiniteMonoidalCategory(FiniteCategory, ABC):

    @abstractmethod
    def monoidal_unit(self) -> Object:
        """ Return the product functor. """

    @abstractmethod
    def monoidal_product(self) -> FiniteFunctor:
        """ Return the product functor. """


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

    @abstractmethod
    def load(self, yaml_data: str) -> FiniteNaturalTransformation:
        """ Load a natural transformation from given YAML data"""

    @abstractmethod
    def save(self, f: FiniteNaturalTransformation) -> str:
        ...


class FiniteAdjunction(ABC):

    @abstractmethod
    def source(self) -> FiniteCategory:
        ...

    @abstractmethod
    def target(self) -> FiniteCategory:
        ...

    @abstractmethod
    def left(self) -> FiniteFunctor:
        pass

    @abstractmethod
    def right(self) -> FiniteFunctor:
        pass


class FiniteAdjunctionRepresentation(ABC):

    @abstractmethod
    def load(self, yaml_data: str) -> FiniteAdjunction:
        ...

    @abstractmethod
    def save(self, f: FiniteAdjunction) -> str:
        ...


class FiniteAdjunctionsOperations(ABC):

    @abstractmethod
    def is_adjunction(self, left: FiniteFunctor,
                      right: FiniteFunctor) -> bool:
        """ check the pair is an adjunction """

    @abstractmethod
    def compose(self, adj1: FiniteAdjunction,
                adj2: FiniteAdjunction) -> FiniteAdjunction:
        """ compose two compatible adjunctions"""

    @abstractmethod
    def from_relation(self, f: FiniteRelation) -> FiniteAdjunction:
        ...


class FiniteDP(ABC):
    pass


class FiniteDPRepresentation(ABC):

    @abstractmethod
    def load(self, yaml_data: str) -> FiniteDP:
        ...

    @abstractmethod
    def save(self, f: FiniteDP) -> str:
        ...


class FiniteDPConstructors(ABC):

    @abstractmethod
    def companion(self, f: FiniteMonotoneMap) -> FiniteDP:
        pass

    @abstractmethod
    def conjoint(self, f: FiniteMonotoneMap) -> FiniteDP:
        pass


class FiniteDPOperations(ABC):

    @abstractmethod
    def series(self, dp1: FiniteDP, dp2: FiniteDP) -> FiniteDP:
        pass

    @abstractmethod
    def union(self, dp1: FiniteDP, dp2: FiniteDP) -> FiniteDP:
        pass

    @abstractmethod
    def intersection(self, dp1: FiniteDP, dp2: FiniteDP) -> FiniteDP:
        pass

    @abstractmethod
    def from_relation(self, f: FiniteRelation) -> FiniteDP:
        ...


class FiniteProfunctor(ABC):
    def cat1(self) -> FiniteCategory:
        ...

    def cat2(self) -> FiniteCategory:
        ...

    def functor(self) -> FiniteFunctor:
        ...


class FiniteProfunctorRepresentation(ABC):

    @abstractmethod
    def load(self, yaml_data: str) -> FiniteProfunctor:
        """ Load a natural transformation from given YAML data"""

    @abstractmethod
    def save(self, f: FiniteProfunctor) -> str:
        ...


class FiniteProfunctorOperations(ABC):

    @abstractmethod
    def series(self, p1: FiniteProfunctor, p2: FiniteProfunctor) -> FiniteProfunctor:
        ...


class FiniteEnrichedCategory(FiniteCategory, ABC):
    def enrichment(self) -> FiniteMonoidalCategory:
        ...
