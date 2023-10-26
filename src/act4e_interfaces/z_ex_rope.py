from abc import ABC
from dataclasses import dataclass
from typing import List

__all__ = [
    "Brick",
    "Component",
    "Elastic",
    "Rope",
    "RupeGoldbergSolver",
    "Solution",
    "Sphere",
]


@dataclass
class Component:
    mass: float
    length: float
    spring_const_pull: float
    spring_const_push: float
    max_compression: float
    max_extension: float


@dataclass
class Rope(Component):
    length: float


@dataclass
class Elastic(Rope):
    elasticity: float  # meaning?


@dataclass
class Brick(Component):
    pass  # add other components / properties


@dataclass
class Sphere(Component):
    pass  # add other components / properties


@dataclass
class Solution:
    # does it break?
    breaks: bool
    # what is the total length (if not broken)?
    total_length: float


class RupeGoldbergSolver(ABC):
    def hang(self, components: List[Component]) -> Solution:
        """What if we hang the first component, and let the others hang below it?"""

    def push(self, components: List[Component], force: float) -> Solution:
        """What if we fix one endpoint, and we compress it?"""

    def pull(self, components: List[Component], force: float) -> Solution:
        """What if we fix one endpoint, and we pull the other end?"""
