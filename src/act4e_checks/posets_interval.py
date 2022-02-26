from typing import Any

import zuper_html as zh
from zuper_testint import find_imp, TestContext, TestManagerInterface, tfor

import act4e_interfaces as I
from .posets_utils import load_poset_tc, poset_coherence


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
    p_arrow = tc.check_result(mks, mks.arrow, I.FinitePosetOfIntervals, p)
    poset_coherence(tc, p_arrow)


@tfor(I.FinitePosetConstructionArrow)
def check_arrow_alphabet(tc: TestContext) -> None:
    mks: I.FinitePosetConstructionArrow = find_imp(tc, I.FinitePosetConstructionArrow)
    p = load_poset_tc(tc, "poset_alphabet")
    p_arrow: I.FinitePosetOfIntervals[str, Any] = tc.check_result(mks, mks.arrow, I.FinitePosetOfIntervals, p)
    poset_coherence(tc, p_arrow)

    # logger.info(elements=list(p_arrow.carrier().elements()))

    def construct(a: Any, b: Any) -> object:
        return tc.check_result(p_arrow, p_arrow.construct, object, a, b)

    def fail_construct(a: Any, b: Any) -> None:
        tc.check_result_raises(p_arrow, p_arrow.construct, ValueError, a, b)

    with tc.description("Should not allow to create bad interval [a,1]"):
        fail_construct("a", 1)

    with tc.description("Should not allow to create bad interval [1,a]"):
        fail_construct(1, "a")

    with tc.description("Should not allow to create unordered interval [b,a]"):
        fail_construct("b", "a")

    i1 = construct("a", "d")
    i2 = construct("c", "e")
    tc.check_result_value(p_arrow, p_arrow.holds, object, True, i1, i2)
    tc.check_result_value(p_arrow, p_arrow.holds, object, False, i2, i1)


@tfor(I.FinitePosetConstructionTwisted)
def check_twisted_alphabet(tc: TestContext) -> None:
    mks: I.FinitePosetConstructionTwisted = find_imp(tc, I.FinitePosetConstructionTwisted)
    p0 = load_poset_tc(tc, "poset_alphabet")
    P: I.FinitePosetOfIntervals[str, Any] = tc.check_result(mks, mks.twisted, I.FinitePosetOfIntervals, p0)
    poset_coherence(tc, P)

    # logger.info(elements=list(P.carrier().elements()))

    def construct(a: Any, b: Any) -> object:
        return tc.check_result(P, P.construct, object, a, b)

    def fail_construct(a: Any, b: Any) -> None:
        tc.check_result_raises(P, P.construct, ValueError, a, b)

    with tc.description("Should not allow to create bad interval [a,1]"):
        fail_construct("a", 1)

    with tc.description("Should not allow to create bad interval [1,a]"):
        fail_construct(1, "a")

    with tc.description("Should not allow to create unordered interval [b,a]"):
        fail_construct("b", "a")

    i1 = construct("e", "f")
    i2 = construct("a", "z")
    tc.check_result_value(P, P.holds, object, True, i1, i2)
    tc.check_result_value(P, P.holds, object, False, i2, i1)


def check_twisted1(tc: TestContext, poset_name: str) -> None:
    mks: I.FinitePosetConstructionTwisted = find_imp(tc, I.FinitePosetConstructionTwisted)
    p = load_poset_tc(tc, poset_name)
    p_twisted = tc.check_result(mks, mks.twisted, I.FinitePosetOfIntervals, p)
    poset_coherence(tc, p_twisted)


@tfor(I.FinitePosetConstructionArrow)
def test_twisted_one(tc: TestContext) -> None:
    mks: I.FinitePosetConstructionArrow = find_imp(tc, I.FinitePosetConstructionArrow)
    p = load_poset_tc(tc, "poset_one")
    p_twisted: I.FinitePosetOfIntervals[Any, Any] = tc.check_result(
        mks, mks.arrow, I.FinitePosetOfIntervals, p
    )
    pairs = [p_twisted.boundaries(_) for _ in p_twisted.carrier().elements()]

    tc.fail_not_equal2(pairs, [(1, 1)], zh.p("Expected only one element"))
