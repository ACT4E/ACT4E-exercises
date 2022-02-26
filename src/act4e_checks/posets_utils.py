import itertools
from typing import Any, List, TypeVar

import zuper_html as zh
from zuper_testint import find_imp, TestContext, TestManagerInterface, TestRef

import act4e_interfaces as I
from .data import dumpit_, get_test_data, get_test_posets, IOHelperImp, loadit_, purify_data
from .sets_utils import check_same_set

X = TypeVar("X")


def check_same_poset(tc: TestContext, s1: I.FinitePoset[X], s2: I.FinitePoset[X]) -> None:
    check_same_set(tc, s1.carrier(), s2.carrier())

    es = list(s1.carrier().elements())

    for a, b in itertools.product(es, es):
        h1 = tc.check_result(s1, s1.holds, bool, a, b)
        h2 = tc.check_result(s2, s2.holds, bool, a, b)
        if h1 != h2:
            tc.fail(zh.span("Different at"), a=a, b=b, h1=h1, h2=h2)

    # check_same_map(c, s1.holds(), s2.holds())


def check_poset_width(
    tc: TestContext, frp: I.FinitePosetMeasurement, s: I.FinitePoset[Any], width: int
) -> None:
    res = tc.check_result(frp, frp.width, int, s)
    if res != width:
        msg = zh.span(f"Expected width = {width}, obtained {res}.")
        tc.fail(msg)


def check_poset_height(
    tc: TestContext, frp: I.FinitePosetMeasurement, s: I.FinitePoset[Any], height: int
) -> None:
    res = tc.check_result(frp, frp.height, int, s)
    if res != height:
        msg = zh.span(f"Expected height = {height}, obtained {res}.")
        tc.fail(msg)


def check_is_upperset(
    tc: TestContext,
    frp: I.FinitePosetSubsetProperties2,
    s: I.FinitePoset[Any],
    subset: List[I.ConcreteRepr],
    expect: bool,
) -> None:
    # TODO: wrap for safety
    h = IOHelperImp()
    carrier = s.carrier()
    elements = [carrier.load(h, _) for _ in subset]
    res = tc.check_result(frp, frp.is_upper_set, bool, s, elements)

    if res != expect:
        msg = zh.span(f"Expected is_upper_set = {expect}, obtained {res}.")
        tc.fail(msg)


def check_is_lowerset(
    tc: TestContext,
    frp: I.FinitePosetSubsetProperties2,
    s: I.FinitePoset[Any],
    subset: List[I.ConcreteRepr],
    expect: bool,
) -> None:
    # TODO: wrap for safety
    h = IOHelperImp()
    carrier = s.carrier()
    elements = [carrier.load(h, _) for _ in subset]
    res = tc.check_result(frp, frp.is_lower_set, bool, s, elements)

    if res != expect:
        msg = zh.span(f"Expected is_lower_set = {expect}, obtained {res}.")
        tc.fail(msg)


def check_is_chain(
    tc: TestContext,
    frp: I.FinitePosetSubsetProperties,
    s: I.FinitePoset[Any],
    subset: List[I.ConcreteRepr],
    expect: bool,
) -> None:
    # TODO: wrap for safety
    h = IOHelperImp()
    carrier = s.carrier()
    elements = [carrier.load(h, _) for _ in subset]
    res = tc.check_result(frp, frp.is_chain, bool, s, elements)

    if res != expect:
        msg = zh.span(f"Expected is_chain = {expect}, obtained {res}.")
        tc.fail(msg)


def check_is_antichain(
    tc: TestContext,
    frp: I.FinitePosetSubsetProperties,
    s: I.FinitePoset[Any],
    subset: List[I.ConcreteRepr],
    expect: bool,
) -> None:
    h = IOHelperImp()
    carrier = s.carrier()
    elements = [carrier.load(h, _) for _ in subset]
    res = tc.check_result(frp, frp.is_antichain, bool, s, elements)

    if res != expect:
        msg = zh.span(f"Expected is_antichain = {expect}, obtained {res}.")
        tc.fail(msg)


def load_the_poset(tm: TestManagerInterface, name: str) -> TestRef[I.FinitePoset[Any]]:
    d = get_test_posets()
    p1 = tm_load_poset(tm, name, tm.store(purify_data(d[name].data)))
    return p1


def tm_load_poset(
    tm: TestManagerInterface, name: str, data: TestRef[I.FinitePoset_desc]
) -> TestRef[I.FinitePoset[Any]]:
    h = IOHelperImp()

    def loadit(
        tc: TestContext, fsr: I.FinitePosetRepresentation, data1: I.FinitePoset_desc
    ) -> I.FinitePoset[Any]:
        return loadit_(tc, fsr, h, data1, I.FinitePoset)

    fsr_ = tm.impof(I.FinitePosetRepresentation)
    return tm.addtest(loadit, fsr_, data, tid0=f"load-poset-{name}")


def tm_save_poset(
    tm: TestManagerInterface, name: str, sgr: TestRef[I.FinitePoset[Any]]
) -> TestRef[I.FinitePoset_desc]:
    h = IOHelperImp()

    def dumpit(
        tc: TestContext, fsr: I.FinitePosetRepresentation, sgr_: I.FinitePoset[Any]
    ) -> I.FinitePoset_desc:
        return dumpit_(tc, fsr, h, sgr_)

    fsr_ = tm.impof(I.FinitePosetRepresentation)
    return tm.addtest(dumpit, fsr_, sgr, tid0=f"dump-poset-{name}")


def load_poset_tc(tc: TestContext, name: str) -> I.FinitePoset[Any]:
    fsr: I.FinitePosetRepresentation = find_imp(tc, I.FinitePosetRepresentation)
    data1 = get_poset_data(name)
    h = IOHelperImp()
    return loadit_(tc, fsr, h, data1, I.FinitePoset)


def get_poset_data(name: str) -> I.FinitePoset_desc:
    d = get_test_data("poset")
    data1 = purify_data(d[name].data)
    return data1


def poset_coherence(tc: TestContext, fi: I.FinitePoset[X]) -> None:
    carrier = tc.check_result(fi, fi.carrier, I.FiniteSet[X])
    elements = list(tc.check_result(fi, carrier.elements, object))
    for a in elements:
        tc.check_result_value(fi, fi.holds, bool, True, a, a)
