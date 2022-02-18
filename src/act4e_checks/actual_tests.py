from typing import TypeVar

from zuper_typing import is_Set

from .good import MyFiniteSetRepresentation

X = TypeVar("X")
E = TypeVar("E")
Y = TypeVar("Y")
_ = is_Set

good_fsr = MyFiniteSetRepresentation()
