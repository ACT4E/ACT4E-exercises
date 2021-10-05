from abc import ABC, abstractmethod

from .sets import FiniteMap, FiniteSet, Mapping, Setoid


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
