from typing import (
    List,
    TypeVar,
)

from zuper_testint import TestManagerInterface, tfor

import act4e_interfaces as I
from .data import get_test_posets, purify_data
from .posets_utils import tm_load_poset, tm_save_poset

__all__: List[str] = []

X = TypeVar("X")


@tfor(I.FinitePosetRepresentation)
def test_FinitePosetRepresentation(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.FinitePosetRepresentation)
    posets = get_test_posets()

    for name, p in posets.items():
        r1 = tm_load_poset(tm, name, tm.store(purify_data(p.data)))
        r1_dumped = tm_save_poset(tm, name, r1)
        r2 = tm_load_poset(tm, name + "-re", r1_dumped)
