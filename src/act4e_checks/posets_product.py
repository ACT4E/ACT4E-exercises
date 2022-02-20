from typing import Any, List

import zuper_html as zh
from zuper_testint import find_imp, TestContext, tfor

import act4e_interfaces as I
from .posets_utils import load_poset_tc


@tfor(I.FinitePosetConstructionProduct)
def test_FinitePosetConstructionProduct(tc: TestContext) -> None:
    mks: I.FinitePosetConstructionProduct = find_imp(tc, I.FinitePosetConstructionProduct)

    poset_empty = load_poset_tc(tc, "poset_empty")
    poset_one = load_poset_tc(tc, "poset_one")
    poset_two = load_poset_tc(tc, "poset_two")

    with tc.description("product of 1 and 1"):
        check_product2(tc, mks, [poset_one, poset_one], n=1)
    with tc.description("product of 1 and 2"):
        check_product2(tc, mks, [poset_one, poset_two], n=2)
    with tc.description("product of 2 and 2"):
        check_product2(tc, mks, [poset_two, poset_two], n=4)
    with tc.description("product of 0 and 2"):
        check_product2(tc, mks, [poset_empty, poset_two], n=0)
    with tc.description("product of nothing"):
        check_product2(tc, mks, [], n=1)


def check_product2(
    tc: TestContext, frp: I.FinitePosetConstructionProduct, ps: List[I.FinitePoset[Any]], n: int
) -> None:
    # logger.info(frp=frp, p1=p1, p2=p2)
    p1_p2 = tc.check_result(frp, frp.product, I.FinitePoset, ps)
    # logger.info(p1_p2=p1_p2)
    carrier = tc.check_result(p1_p2, p1_p2.carrier, I.FiniteSet)
    elements = list(carrier.elements())
    with tc.description(f"Checking that it has {n} elements"):
        tc.fail_not_equal2(len(elements), n, zh.p("not equal"), elements=elements)
    # logger.info(elements=list(carrier.elements()))
    if elements:
        e0 = elements[0]
        tc.fail_not_equal2(True, p1_p2.holds(e0, e0), zh.p("p1_p2.holds(e0, e0)"))
