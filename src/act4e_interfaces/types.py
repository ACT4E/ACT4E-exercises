from typing import NewType, TypeVar

__all__ = ["Object", "Morphism", "Element", "ConcreteRepr"]

Object = TypeVar("Object")
Morphism = TypeVar("Morphism")

Element = TypeVar("Element")
ConcreteRepr = NewType("ConcreteRepr", object)
