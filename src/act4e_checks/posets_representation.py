from typing import (
    List,
    TypeVar,
)

from zuper_testint import TestContext, TestManagerInterface, tfor

import act4e_interfaces as I
from .data import filter_reqs, get_test_posets, purify_data
from .posets_utils import load_poset_tc, tm_load_poset, tm_save_poset

__all__: List[str] = []

X = TypeVar("X")


@tfor(I.FinitePosetRepresentation)
def test_FinitePosetRepresentation_basic(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.FinitePosetRepresentation)
    posets = get_test_posets()

    for name, p in posets.items():
        r1 = tm_load_poset(tm, name, tm.store(purify_data(p.data)))
        r1_dumped = tm_save_poset(tm, name, r1)
        r2 = tm_load_poset(tm, name + "-re", r1_dumped)


@tfor(I.FinitePosetRepresentation, level="Product")
def test_FinitePosetRepresentation_Product(tm: TestManagerInterface) -> None:
    d = get_test_posets()
    use = filter_reqs(d, "poset_product")
    for k, v in use.items():
        tm.addtest(test_loading_poset, k, tid0=f"test_loading_poset_product-{k}")


def test_loading_poset(tc: TestContext, poset_name: str) -> None:
    poset = load_poset_tc(tc, poset_name)
