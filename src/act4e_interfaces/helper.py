from __future__ import annotations

from abc import ABC, abstractmethod

__all__ = ['IOHelper']


class IOHelper(ABC):
    @abstractmethod
    def loadfile(self, name: str) -> dict:
        """ Load from the filesystem. """
