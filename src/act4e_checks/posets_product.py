from typing import Any

import zuper_html as zh
from zuper_testint import TestContext, TestManagerInterface, tfor

import act4e_interfaces as I
from . import logger
from .posets_utils import load_the_poset


@tfor(I.FinitePosetConstructionProduct)
def test_FinitePosetConstructionProduct(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.FinitePosetConstructionProduct)

    p1 = load_the_poset(tm, "poset_two")
    p2 = load_the_poset(tm, "poset_two")
    tm.addtest(check_product2, mks, p1, p2, tid0=f"check_product-poset_one-poset_one")


def check_product2(
    tc: TestContext, frp: I.FinitePosetConstructionProduct, p1: I.FinitePoset[Any], p2: I.FinitePoset[Any]
) -> None:
    logger.info(frp=frp, p1=p1, p2=p2)
    p1_p2 = tc.check_result(frp, frp.product, I.FinitePoset, [p1, p2])
    logger.info(p1_p2=p1_p2)
    carrier = p1_p2.carrier()
    elements = list(carrier.elements())
    logger.info(elements=list(carrier.elements()))
    e0 = elements[0]
    tc.fail_not_equal2(True, p1_p2.holds(e0, e0), zh.p("p1_p2.holds(e0, e0)"))
