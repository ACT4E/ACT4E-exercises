from typing import Any

import zuper_html as zh
from zuper_testint import find_imp, TestContext, tfor

import act4e_interfaces as I
from .posets_utils import check_same_poset, load_poset_tc


@tfor(I.FinitePosetConstructionSum)
def check_poset_disjoint_union(tc: TestContext) -> None:
    msd: I.FinitePosetConstructionSum = find_imp(tc, I.FinitePosetConstructionSum)
    poset_empty = load_poset_tc(tc, "poset_empty")

    poset2 = tc.check_result(msd, msd.disjoint_union, I.FinitePosetDisjointUnion, [poset_empty, poset_empty])
    # logger.info(poset2=poset2)

    check_same_poset(tc, poset2, poset_empty)

    set_one: I.FinitePoset[int] = load_poset_tc(tc, "poset_one")
    set_two: I.FinitePoset[int] = load_poset_tc(tc, "poset_two")

    one_plus_two: I.FinitePosetDisjointUnion[int, Any] = tc.check_result(
        msd, msd.disjoint_union, I.FinitePosetDisjointUnion, [set_one, set_two]
    )
    carrier = tc.check_result(one_plus_two, one_plus_two.carrier, I.FiniteSetDisjointUnion)
    elements = list(carrier.elements())

    for e in elements:
        one_plus_two.holds(e, e)

    with tc.description("Making sure it works for n = 0 sets."):
        zero = tc.check_result(msd, msd.disjoint_union, I.FinitePosetDisjointUnion, [])
        elements = list(zero.carrier().elements())
        tc.fail_not_equal2(0, len(elements), zh.span("Expected 0 elements"))
