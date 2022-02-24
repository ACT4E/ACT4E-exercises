from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Generic, Protocol, TypeVar

__all__ = ["IOHelper", "Loader", "Saver", "Serializer"]

# Rcov = TypeVar("Rcov", covariant=True)
# Rcon = TypeVar("Rcon", contravariant=True)
#
# Xcov = TypeVar("Xcov", covariant=True)
# Xcon = TypeVar("Xcon", contravariant=True)

R = TypeVar("R")
X = TypeVar("X")


class IOHelper(ABC):
    @abstractmethod
    def loadfile(self, name: str) -> Dict[str, object]:
        """Load from the filesystem."""


class Loader(Protocol[X, R]):
    def load(self, h: IOHelper, data: R) -> X:
        """Load a finite set from data structure.
        Throw InvalidFormat if the format is incorrect.
        """
        ...


class Saver(Protocol[X, R]):
    def save(self, h: IOHelper, ob: X) -> R:
        ...


class Serializer(Generic[X, R], Loader[X, R], Saver[X, R]):
    ...
