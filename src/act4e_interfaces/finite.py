from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable, Iterator, List, Optional, overload, Tuple

from .helper import IOHelper
from .types import ConcreteRepr, Element, Morphism, Object

__all__ = [
    "InvalidFormat",
    "FreeSemigroup",
    "InvalidValue",
    "EnumerableSetsOperations",
    "EnumerableSet",
    "FiniteSetUnion",
    "Setoid",
    "SetoidOperations",
    "SetProduct",
    "SetDisjointUnion",
    "MakeSetUnion",
    "MakeSetDisjointUnion",
    "MakeSetIntersection",
    "MakeSetProduct",
    "MonotoneMap",
    "Mapping",
    "SetUnion",
    "Group",
    "Monoid",
    "MonoidalCategory",
    "MonoidalCategory",
    "FiniteMap",
    "FiniteDP",
    "FiniteSet",
    "FiniteSetProperties",
    "FiniteSetProduct",
    "FiniteProfunctor",
    "FiniteSetDisjointUnion",
    "FiniteFunctor",
    "FiniteSemigroupConstruct",
    "FiniteSemigroup",
    "FinitePoset",
    "FiniteAdjunction",
    "FiniteMonoidalPoset",
    "FiniteMonoidalCategory",
    "FiniteCategory",
    "FiniteEnrichedCategory",
    "FiniteRelation",
    "Relation",
    "FiniteSemiCategory",
    "FiniteMonoid",
    "FiniteCategoryOperations",
    "FiniteDPOperations",
    "FiniteAdjunctionsOperations",
    "FiniteProfunctorOperations",
    "FiniteGroup",
    "FiniteLattice",
    "FiniteRelationProperties",
    "FiniteRelationOperations",
    "FiniteEndorelationOperations",
    "FiniteMonotoneMapProperties",
    "FiniteEndorelationProperties",
    "FinitePosetConstruction",
    "FinitePosetConstructors",
    "FinitePosetSubsetProperties",
    "FinitePosetClosures",
    "FinitePosetMeasurement",
    "FinitePosetSubsetProperties2",
    "FiniteMapOperations",
    # "FinitePosetSubsetOperations",
    "FiniteNaturalTransformation",
    "Semigroup",
    "Lattice",
    "JoinSemilattice",
    "Adjunction",
    "MeetSemilattice",
    "MonoidalPosetOperations",
    "SemiCategory",
    "SemiBiCategory",
    "Poset",
    "Category",
    "CategoryOperations",
    "DP",
    "DPCategory",
    "DPI",
    "DPConstructors",
    "InvalidFormat",
]


class Setoid(ABC):
    """
    A setoid is something to which elements may belong,
    has a way of distinguishing elements,
    and is able to (de)serialize its elements.
    """

    @abstractmethod
    def contains(self, x: Element) -> bool:
        """ Returns true if the element is in the set. """

    def equal(self, x: Element, y: Element) -> bool:
        """ Returns True if the two elements are to be considered equal. """
        return x == y  # default is to use the Python equality

    def apart(self, x: Element, y: Element) -> bool:
        return not self.equal(x, y)

    @abstractmethod
    def save(self, h: IOHelper, x: Element) -> ConcreteRepr:
        ...

    @abstractmethod
    def load(self, h: IOHelper, o: ConcreteRepr) -> Element:
        ...


class Mapping(ABC):
    @abstractmethod
    def source(self) -> Setoid:
        ...

    @abstractmethod
    def target(self) -> Setoid:
        ...

    @abstractmethod
    def __call__(self, a: Element) -> Element:
        ...


class EnumerableSet(Setoid, ABC):
    @abstractmethod
    def elements(self) -> Iterator[Element]:
        """ Note: possibly non-terminating. """


class FiniteSet(EnumerableSet, ABC):
    """ A finite set has a finite size. """

    @abstractmethod
    def size(self) -> int:
        """ Return the size of the finite set. """


class FiniteMap(Mapping, ABC):
    @abstractmethod
    def source(self) -> FiniteSet:
        ...

    @abstractmethod
    def target(self) -> FiniteSet:
        ...


class InvalidFormat(Exception):
    """ Raise this if the input data to parse is invalid. """


class InvalidValue(ValueError):
    """ Raise this if the input does not make sense. """


class FiniteSetProperties(ABC):
    @abstractmethod
    def is_subset(self, a: FiniteSet, b: FiniteSet) -> bool:
        """ True if `a` is a subset of `b`. """

    def equal(self, a: FiniteSet, b: FiniteSet) -> bool:
        return self.is_subset(a, b) and self.is_subset(b, a)

    def is_strict_subset(self, a: FiniteSet, b: FiniteSet) -> bool:
        return self.is_subset(a, b) and not self.is_subset(b, a)


class SetProduct(Setoid, ABC):
    """ A set product is a setoid that can be factorized. """

    @abstractmethod
    def components(self) -> List[Setoid]:
        """ Returns the components of the product"""

    @abstractmethod
    def pack(self, *args: Element) -> Element:
        """ Packs an element of each setoid into an element of the mapping"""

    @abstractmethod
    def projections(self) -> List[Mapping]:
        """ Returns the projection mappings. """


class FiniteSetProduct(FiniteSet, SetProduct, ABC):
    """ Specialization of SetProduct where we deal with FiniteSets"""

    @abstractmethod
    def components(self) -> List[FiniteSet]:
        """ Returns the components """

    @abstractmethod
    def projections(self) -> List[FiniteMap]:
        """ Returns the projection mappings. """


class SetUnion(Setoid, ABC):
    """ A set product is a setoid that can be factorized. """

    @abstractmethod
    def components(self) -> List[Setoid]:
        """ Returns the components of the union"""


class EnumerableSetUnion(EnumerableSet, SetUnion, ABC):
    """ Specialization of SetUnion where we deal with FiniteSets"""

    @abstractmethod
    def components(self) -> List[EnumerableSet]:
        """ Returns the components of the union """


class FiniteSetUnion(FiniteSet, EnumerableSetUnion, ABC):
    """ Specialization of SetUnion where we deal with FiniteSets"""

    @abstractmethod
    def components(self) -> List[FiniteSet]:
        """ Returns the components of the union """


class SetDisjointUnion(Setoid, ABC):
    @abstractmethod
    def components(self) -> List[Setoid]:
        """ Returns the components of the union """

    @abstractmethod
    def injections(self) -> List[Mapping]:
        """ Returns the projection mappings. """


class FiniteSetDisjointUnion(FiniteSet, SetDisjointUnion, ABC):
    """ Specialization of SetProduct where we deal with FiniteSets"""

    @abstractmethod
    def components(self) -> List[FiniteSet]:
        ...

    @abstractmethod
    def injections(self) -> List[FiniteMap]:
        ...


class MakeSetProduct(ABC):
    @overload
    def product(self, components: List[Setoid]) -> SetProduct:
        ...

    @abstractmethod
    def product(self, components: List[FiniteSet]) -> FiniteSetProduct:
        ...


class MakeSetIntersection(ABC):
    @abstractmethod
    def intersection(self, components: List[FiniteSet]) -> FiniteSet:
        ...


class MakeSetUnion(ABC):
    @overload
    def union(self, components: List[FiniteSet]) -> FiniteSetUnion:
        ...

    @overload
    def union(self, components: List[EnumerableSet]) -> EnumerableSetUnion:
        ...

    @abstractmethod
    def union(self, components: List[Setoid]) -> SetUnion:
        ...


# added
class MakeSetDisjointUnion(ABC):
    @overload
    def compute_disjoint_union(self, components: List[Setoid]) -> SetDisjointUnion:
        ...

    @abstractmethod
    def compute_disjoint_union(self, components: List[FiniteSet]) -> FiniteSetDisjointUnion:
        ...


class Relation(ABC):
    @abstractmethod
    def source(self) -> Setoid:
        """ Returns a setoid """

    @abstractmethod
    def target(self) -> Setoid:
        """ Returns a setoid """

    @abstractmethod
    def holds(self) -> Mapping:
        """ Returns true if the two elements are related """


class FiniteRelation(Relation, ABC):
    @abstractmethod
    def source(self) -> FiniteSet:
        """ Returns a finite set"""

    @abstractmethod
    def target(self) -> FiniteSet:
        """ Returns a finite set"""

    @abstractmethod
    def holds(self) -> FiniteMap:
        """ Returns true if the two elements are related """


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
        """ Returns the transitive closure of a relation """


class FiniteMapOperations(ABC):
    @abstractmethod
    def compose(self, f: FiniteMap, g: FiniteMap) -> FiniteMap:
        """ compose two functions"""

    @abstractmethod
    def as_relation(self, f: FiniteMap) -> FiniteRelation:
        """ Load the data  """


class Semigroup(ABC):
    @abstractmethod
    def carrier(self) -> Setoid:
        ...

    @abstractmethod
    def composition(self) -> Mapping:
        ...


class FiniteSemigroup(Semigroup, ABC):
    @abstractmethod
    def carrier(self) -> FiniteSet:
        ...

    @abstractmethod
    def composition(self) -> FiniteMap:
        ...


class FreeSemigroup(Semigroup, ABC):

    @abstractmethod
    def unit(self, a: Element) -> Element:
        """ From an element of the carrier, returns the element of the free semigroup """


class FiniteSemigroupConstruct(ABC):
    @abstractmethod
    def free(self, fs: FiniteSet) -> FreeSemigroup:
        """ Construct the free semigroup on a set. """


class FreeGroup(Semigroup, ABC):

    @abstractmethod
    def unit(self, a: Element) -> Element:
        """ From an element of the carrier, returns the element of the free group. """


class FiniteFreeGroupConstruct(ABC):
    @abstractmethod
    def free(self, fs: FiniteSet) -> FreeGroup:
        """ Construct the free group on a set. """


class Monoid(Semigroup, ABC):
    @abstractmethod
    def identity(self) -> Element:
        ...


class Group(Monoid, ABC):
    @abstractmethod
    def inverse(self) -> Mapping:
        """ Returns the inverse of an element"""


class FiniteMonoid(Monoid, FiniteSemigroup, ABC):
    """"""


class FiniteGroup(Group, FiniteMonoid, ABC):
    @abstractmethod
    def inverse(self) -> FiniteMap:
        ...


# TODO: equational theories


class Poset(ABC):
    @abstractmethod
    def carrier(self) -> Setoid:
        ...

    @abstractmethod
    def holds(self) -> Mapping:
        ...


class FinitePoset(Poset, ABC):
    """ Implementation of finite posets. """

    @abstractmethod
    def carrier(self) -> FiniteSet:
        ...

    @abstractmethod
    def holds(self) -> FiniteMap:
        ...


class FinitePosetSubsetProperties(ABC):
    @abstractmethod
    def is_chain(self, fp: FinitePoset, s: List[Element]) -> bool:
        """ True if the given elements form a chain. """

    @abstractmethod
    def is_antichain(self, fp: FinitePoset, s: List[Element]) -> bool:
        """ True if the given elements form an antichain. """


class FinitePosetMeasurement(ABC):
    @abstractmethod
    def width(self, fp: FinitePoset) -> int:
        """ Return the width of the poset. """

    @abstractmethod
    def height(self, fp: FinitePoset) -> int:
        """ Return the height of the poset. """


class FinitePosetMinMax(ABC):
    @abstractmethod
    def miminal(self, fp: FinitePoset, S: List[Element]) -> List[Element]:
        """ Return the minimal elements of S """

    @abstractmethod
    def maximal(self, fp: FinitePoset, S: List[Element]) -> List[Element]:
        """ Return the maximal elements of S """


class FinitePosetInfSup(ABC):

    @abstractmethod
    def lower_bounds(self, fp: FinitePoset, s: List[Element]) -> List[Element]:
        """ Computes the lower bounds for the subset"""

    @abstractmethod
    def infimum(self, fp: FinitePoset, s: List[Element]) -> Optional[Element]:
        """ Computes the infimum / meet / greatest lower bound
            for the subset, or returns None if one does not exist. """

    @abstractmethod
    def upper_bounds(self, fp: FinitePoset, s: List[Element]) -> List[Element]:
        """ Computes the upper bounds for the subset. """

    @abstractmethod
    def supremum(self, fp: FinitePoset, s: List[Element]) -> Optional[Element]:
        """ Computes the supremum for the subset if it exists,
            or returns None if one does not exist. """


class FinitePosetSubsetProperties2(ABC):

    @abstractmethod
    def is_lower_set(self, fp: FinitePoset, s: List[Element]) -> bool:
        pass

    @abstractmethod
    def is_upper_set(self, fp: FinitePoset, s: List[Element]) -> bool:
        pass


class FinitePosetClosures(ABC):

    @abstractmethod
    def upper_closure(self, fp: FinitePoset, s: List[Element]) -> List[Element]:
        pass

    @abstractmethod
    def lower_closure(self, fp: FinitePoset, s: List[Element]) -> List[Element]:
        pass


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


class FinitePosetConstruction(ABC):

    @abstractmethod
    def product(self, p1: FinitePoset, p2: FinitePoset) -> FinitePoset:
        ...

    @abstractmethod
    def disjoint_union(self, p1: FinitePoset, p2: FinitePoset) -> FinitePoset:
        ...

    @abstractmethod
    def opposite(self, p: FinitePoset) -> FinitePoset:
        ...

    @abstractmethod
    def twisted(self, s: FinitePoset) -> FinitePoset:
        ...

    @abstractmethod
    def arrow(self, s: FinitePoset) -> FinitePoset:
        ...

    @abstractmethod
    def powerposet(self, s: FinitePoset) -> FinitePoset:
        ...




class MonotoneMap(Mapping, ABC):
    def source_poset(self) -> Poset:
        ...

    def target_poset(self) -> Poset:
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


class MeetSemilattice(Poset, ABC):
    @abstractmethod
    def meet(self, x: Element, y: Element) -> Element:
        ...

    @abstractmethod
    def top(self) -> Element:
        ...


class JoinSemilattice(Poset, ABC):
    @abstractmethod
    def join(self, x: Element, y: Element) -> Element:
        ...

    @abstractmethod
    def bottom(self) -> Element:
        ...


class Lattice(JoinSemilattice, MeetSemilattice, ABC):
    ...


class FiniteLattice(ABC):
    @abstractmethod
    def carrier(self) -> FiniteSet:
        ...


class SemiBiCategory(ABC):
    @abstractmethod
    def objects(self) -> Setoid:
        ...

    @abstractmethod
    def hom(self, ob1: Object, ob2: Object) -> Setoid:
        ...

    @abstractmethod
    def legs(self, m: Morphism) -> Tuple[Object, Object]:
        """ Return source and target of the morphism """


class SemiCategory(SemiBiCategory, ABC):
    ...


class Category(SemiCategory, ABC):
    @abstractmethod
    def identity(self, ob: Object) -> Morphism:
        """ Identity for the object """


assert [1] + [1, 2] == [1, 1, 2]
assert [1, 1, 2] + [] == [1, 1, 2]


class FiniteSemiCategory(SemiCategory, ABC):
    @abstractmethod
    def objects(self) -> FiniteSet:
        ...

    @abstractmethod
    def hom(self, ob1: Object, ob2: Object) -> FiniteSet:
        ...


class FiniteCategory(FiniteSemiCategory, Category, ABC):
    ...


class CategoryOperations:
    @abstractmethod
    def product(self, c1: Category, c2: Category) -> Category:
        """ Product of two categories. """

    @abstractmethod
    def disjoint_union(self, c1: Category, c2: Category) -> FiniteCategory:
        """ Disjoint union for the categories """

    @abstractmethod
    def arrow(self, c1: Category) -> Category:
        """ Computes the arrow category """

    @abstractmethod
    def twisted(self, c1: Category) -> Category:
        """ Computes the twisted arrow category """


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
    def twisted(self, c1: FiniteCategory) -> FiniteCategory:
        """ Computes the twisted arrow category """


class Functor(ABC):
    @abstractmethod
    def source(self) -> Category:
        ...

    @abstractmethod
    def target(self) -> Category:
        ...

    @abstractmethod
    def f_ob(self, ob: Object) -> Object:
        """ Effect on objects """

    @abstractmethod
    def f_mor(self, m: Morphism) -> Morphism:
        """ Effect on morphisms """


class FiniteFunctor(Functor, ABC):
    @abstractmethod
    def source(self) -> FiniteCategory:
        ...

    @abstractmethod
    def target(self) -> FiniteCategory:
        ...


class MonoidalCategory(Category, ABC):
    @abstractmethod
    def monoidal_unit(self) -> Object:
        """ Return the product functor. """

    @abstractmethod
    def monoidal_product(self) -> FiniteFunctor:
        """ Return the product functor. """


class FiniteMonoidalCategory(MonoidalCategory, FiniteCategory, ABC):
    ...


class NaturalTransformation(ABC):
    @abstractmethod
    def cat1(self) -> Category:
        ...

    @abstractmethod
    def cat2(self) -> Category:
        ...

    @abstractmethod
    def component(self, ob: Object) -> Morphism:
        """Returns the component for a particular object in the first category.
        This is a morphism in the second category.
        """


class FiniteNaturalTransformation(NaturalTransformation, ABC):
    @abstractmethod
    def cat1(self) -> FiniteCategory:
        ...

    @abstractmethod
    def cat2(self) -> FiniteCategory:
        ...


class Adjunction(ABC):
    @abstractmethod
    def source(self) -> Category:
        ...

    @abstractmethod
    def target(self) -> Category:
        ...

    @abstractmethod
    def left(self) -> Functor:
        ...

    @abstractmethod
    def right(self) -> Functor:
        ...


class FiniteAdjunction(Adjunction, ABC):
    @abstractmethod
    def source(self) -> FiniteCategory:
        ...

    @abstractmethod
    def target(self) -> FiniteCategory:
        ...

    @abstractmethod
    def left(self) -> FiniteFunctor:
        ...

    @abstractmethod
    def right(self) -> FiniteFunctor:
        ...


class FiniteAdjunctionsOperations(ABC):
    @abstractmethod
    def is_adjunction(self, left: FiniteFunctor, right: FiniteFunctor) -> bool:
        """ check the pair is an adjunction """

    @abstractmethod
    def compose(self, adj1: FiniteAdjunction, adj2: FiniteAdjunction) -> FiniteAdjunction:
        """ compose two compatible adjunctions"""

    @abstractmethod
    def from_relation(self, f: FiniteRelation) -> FiniteAdjunction:
        ...


class DPI(ABC):
    @abstractmethod
    def functionality(self) -> Poset:
        ...

    @abstractmethod
    def implementations(self) -> Setoid:
        ...

    @abstractmethod
    def costs(self) -> Poset:
        ...

    @abstractmethod
    def requires(self) -> Mapping:
        ...

    @abstractmethod
    def provides(self) -> Mapping:
        ...


class DPCategory(Category, ABC):
    ...


class DP(ABC):
    ...


class FiniteDP(ABC):
    ...


class DPConstructors(ABC):
    @abstractmethod
    def companion(self, f: MonotoneMap) -> DP:
        ...

    @abstractmethod
    def conjoint(self, f: MonotoneMap) -> DP:
        ...


class FiniteDPOperations(ABC):
    @abstractmethod
    def series(self, dp1: FiniteDP, dp2: FiniteDP) -> FiniteDP:
        ...

    @abstractmethod
    def union(self, dp1: FiniteDP, dp2: FiniteDP) -> FiniteDP:
        ...

    @abstractmethod
    def intersection(self, dp1: FiniteDP, dp2: FiniteDP) -> FiniteDP:
        ...

    @abstractmethod
    def from_relation(self, f: FiniteRelation) -> FiniteDP:
        ...


class Profunctor(ABC):
    def source(self) -> Category:
        ...

    def target(self) -> Category:
        ...

    def functor(self) -> Functor:
        ...


class FiniteProfunctor(ABC):
    def cat1(self) -> FiniteCategory:
        ...

    def cat2(self) -> FiniteCategory:
        ...

    def functor(self) -> FiniteFunctor:
        ...


class FiniteProfunctorOperations(ABC):
    @abstractmethod
    def series(self, p1: FiniteProfunctor, p2: FiniteProfunctor) -> FiniteProfunctor:
        ...


class FiniteEnrichedCategory(FiniteCategory, ABC):
    def enrichment(self) -> FiniteMonoidalCategory:
        ...


class SetoidOperations(ABC):
    @classmethod
    @abstractmethod
    def union_setoids(cls, a: Setoid, b: Setoid) -> Setoid:
        """ Creates the union of two Setoids. """

    @classmethod
    @abstractmethod
    def intersection_setoids(cls, a: Setoid, b: Setoid) -> Setoid:
        """ Creates the intersection of two Setoids. """


class EnumerableSetsOperations(ABC):
    @classmethod
    @abstractmethod
    def make_set_sequence(cls, f: Callable[[int], object]):
        """Creates an EnumerableSet from a function that gives the
        i-th element."""

    @classmethod
    @abstractmethod
    def union_esets(cls, a: EnumerableSet, b: EnumerableSet) -> EnumerableSet:
        """ Creates the union of two EnumerableSet. """
