from typing import Any, TypeVar

import zuper_html as zh
from zuper_testint import find_imp, TestContext, TestManagerInterface, tfor

import act4e_interfaces as I
from .sets_utils import check_same_element, check_same_set, load_set_tc

E = TypeVar("E")
X = TypeVar("X")


@tfor(I.FiniteMakeSetDisjointUnion)
def test_FiniteMakeSetDisjointUnion(tm: TestManagerInterface) -> None:
    tm.addtest(check_set_disjoint_union)


@tfor(I.FiniteMakeSetDisjointUnion)
def check_set_disjoint_union(tc: TestContext) -> None:
    msd: I.FiniteMakeSetDisjointUnion = find_imp(tc, I.FiniteMakeSetDisjointUnion)
    set_empty = load_set_tc(tc, "set_empty")

    set2 = tc.check_result(msd, msd.disjoint_union, I.FiniteSetDisjointUnion, [set_empty, set_empty])
    check_same_set(tc, set2, set_empty)

    set_one: I.FiniteSet[int] = load_set_tc(tc, "set_one")
    set_two: I.FiniteSet[int] = load_set_tc(tc, "set_two")

    one_plus_two: I.FiniteSetDisjointUnion[int, Any] = tc.check_result(
        msd, msd.disjoint_union, I.FiniteSetDisjointUnion, [set_one, set_two]
    )
    elements = list(one_plus_two.elements())

    for e in elements:
        i, x = tc.check_result(one_plus_two, one_plus_two.unpack, object, e)
        e2 = tc.check_result(one_plus_two, one_plus_two.pack, object, i, x)
        check_same_element(tc, one_plus_two, e, e2)

    # either exception or in any case not allowing it
    try:
        banana = one_plus_two.pack(0, 42)
    except ValueError:
        pass
    else:
        tc.check_result_value(one_plus_two, one_plus_two.contains, bool, False, banana)

    with tc.description("Checking that bad indexes are not allowed."):
        # either exception or in any case not allowing it
        try:
            banana2 = one_plus_two.pack(-1, 42)
        except ValueError:
            pass
        else:
            tc.fail(zh.span("pack() should not allow negative index"), banana2=banana2)

        try:
            banana3 = one_plus_two.pack(3, 42)
        except ValueError:
            pass
        else:
            tc.fail(zh.span("pack() should not allow index too high"), banana3=banana3)

    with tc.description("Making sure it works for n = 0 sets."):
        zero = tc.check_result(msd, msd.disjoint_union, I.FiniteSetDisjointUnion, [])
        elements = list(zero.elements())
        tc.fail_not_equal2(0, len(elements), zh.span("Expected 0 elements"))
