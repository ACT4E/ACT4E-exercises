from typing import (
    Any,
)

import zuper_html as zh
from zuper_testint import find_imp, TestContext, TestManagerInterface, tfor

import act4e_interfaces as I
from act4e_checks.posets_utils import load_poset_tc


@tfor(I.FinitePosetConstructionArrow)
def test_FinitePosetConstructionArrow(tm: TestManagerInterface) -> None:
    _mks = tm.impof(I.FinitePosetConstructionArrow)
    for poset_name in ["poset_empty", "poset_one", "poset_two"]:
        tm.addtest(check_arrow1, poset_name, tid0=f"FinitePosetConstructionArrow-{poset_name}")


@tfor(I.FinitePosetConstructionTwisted)
def test_FinitePosetConstructionTwisted(tm: TestManagerInterface) -> None:
    _mks = tm.impof(I.FinitePosetConstructionTwisted)
    for poset_name in ["poset_empty", "poset_one", "poset_two"]:
        tm.addtest(check_twisted1, poset_name, tid0=f"FinitePosetConstructionTwisted-{poset_name}")


def check_arrow1(tc: TestContext, poset_name: str) -> None:
    mks: I.FinitePosetConstructionArrow = find_imp(tc, I.FinitePosetConstructionArrow)
    p = load_poset_tc(tc, poset_name)
    p_arrow = tc.check_result(mks, mks.arrow, I.PosetOfIntervals, p)


def check_twisted1(tc: TestContext, poset_name: str) -> None:
    mks: I.FinitePosetConstructionArrow = find_imp(tc, I.FinitePosetConstructionArrow)
    p = load_poset_tc(tc, poset_name)
    p_twisted = tc.check_result(mks, mks.arrow, I.PosetOfIntervals, p)


@tfor(I.FinitePosetConstructionArrow)
def test_twisted_one(tc: TestContext) -> None:
    mks: I.FinitePosetConstructionArrow = find_imp(tc, I.FinitePosetConstructionArrow)
    p = load_poset_tc(tc, "poset_one")
    p_twisted: I.FinitePosetOfIntervals[Any, Any] = tc.check_result(
        mks, mks.arrow, I.FinitePosetOfIntervals, p
    )
    pairs = [p_twisted.boundaries(_) for _ in p_twisted.carrier().elements()]

    tc.fail_not_equal2(pairs, [(1, 1)], zh.p("Expected only one element"))
