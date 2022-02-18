from dataclasses import dataclass
from typing import cast, Generic, Iterator, List, TypeVar

import act4e_interfaces as I

__all__ = ["MyFiniteSet"]
X = TypeVar("X")


@dataclass
class MyFiniteSet(Generic[X], I.FiniteSet[X]):
    def save(self, h: I.IOHelper, x: X) -> I.ConcreteRepr:
        return cast(I.ConcreteRepr, x)

    def load(self, h: I.IOHelper, o: I.ConcreteRepr) -> X:
        return cast(X, o)

    _elements: List[X]

    def size(self) -> int:
        return len(self._elements)

    def contains(self, x: X) -> bool:
        for y in self._elements:
            if self.equal(x, y):
                return True
        return False

    def elements(self) -> Iterator[X]:
        for _ in self._elements:
            yield _
