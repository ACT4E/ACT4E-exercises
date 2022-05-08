import itertools
from typing import (
    Any,
    TypeVar,
)

import zuper_html as zh
from zuper_testint import find_imp, TestContext, TestManagerInterface, tfor

import act4e_interfaces as I
from .data import get_test_posets, purify_data
from .posets_utils import check_same_poset, poset_coherence, tm_load_poset
from .sets_utils import load_set_tc

X = TypeVar("X")


@tfor(I.FinitePosetConstructionOpposite)
def test_FinitePosetConstructionOpposite(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.FinitePosetConstructionOpposite)

    d = get_test_posets()
    for rname, rinfo in d.items():

        def get(p: Any) -> Any:
            return rinfo.properties.get(p, None)

        r1 = tm_load_poset(tm, rname, tm.store(purify_data(rinfo.data)))
        rname2 = get("opposite")
        if rname2 is not None:
            rinfo2 = d[rname2].data
            r2 = tm_load_poset(tm, rname2, tm.store(purify_data(rinfo2)))

            tm.addtest(check_opposite, mks, r1, r2, tid0=f"check_opposite-{rname}-{rname2}")


def check_opposite(
    tc: TestContext, frp: I.FinitePosetConstructionOpposite, p: I.FinitePoset[X], p_op: I.FinitePoset[X]
) -> None:
    p_op2: I.FinitePoset[X] = tc.check_result(frp, frp.opposite, I.FinitePoset, p)  # type: ignore
    # logger.info(p=p, p_op=p_op, p_op2=p_op2)
    check_same_poset(tc, p_op, p_op2)

    carrier = p.carrier()
    elements = list(carrier.elements())

    for a, b in itertools.product(elements, elements):
        h = p.holds(a, b)
        h1 = p_op.holds(b, a)
        tc.fail_not_equal2(h, h1, zh.span("Poset is not opposite"), a=a, b=b)


@tfor(I.FinitePosetConstructionPower)
def check_FinitePosetConstructionPower1(tc: TestContext) -> None:
    mks: I.FinitePosetConstructionPower = find_imp(tc, I.FinitePosetConstructionPower)
    s = load_set_tc(tc, "set_two")
    p: I.FinitePosetOfFiniteSubsets[int, Any]
    p = tc.check_result(mks, mks.powerposet, I.FinitePosetOfFiniteSubsets, s)
    poset_coherence(tc, p)

    # logger.info(el=list(p.carrier().elements()))

    carrier = tc.check_result(p, p.carrier, object)

    def construct(x: Any) -> Any:
        return tc.check_result(carrier, carrier.construct, object, x)

    c1 = construct([])
    c2 = construct([1])

    tc.check_result_value(c1, p.holds, bool, True, c1, c2)
    tc.check_result_value(c1, p.holds, bool, False, c2, c1)
