import itertools
from typing import (
    Any,
    List,
    TypeVar,
)

import zuper_html as zh
from zuper_testint import find_imp, TestContext, TestManagerInterface, TestNotImplemented, TestRef, tfor

import act4e_interfaces as I
from . import logger
from .data import dumpit_, get_test_data, get_test_posets, IOHelperImp, loadit_, purify_data
from .sets import check_same_set

__all__: List[str] = []
X = TypeVar("X")


@tfor(I.FinitePosetConstructionProduct)
def test_FinitePosetConstructionProduct(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.FinitePosetConstructionProduct)

    p1 = load_the_poset(tm, "poset_two")
    p2 = load_the_poset(tm, "poset_two")
    tm.addtest(check_product2, mks, p1, p2, tid0=f"check_product-poset_one-poset_one")


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


@tfor(I.FiniteMonotoneMapProperties)
def test_FiniteMonotoneMapProperties(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.FiniteMonotoneMapProperties)
    raise TestNotImplemented()


@tfor(I.MonoidalPosetOperations)
def test_MonoidalPosetOperations(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.MonoidalPosetOperations)
    raise TestNotImplemented()


@tfor(I.FinitePosetRepresentation)
def test_FinitePosetRepresentation(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.FinitePosetRepresentation)
    posets = get_test_posets()

    for name, p in posets.items():
        r1 = tm_load_poset(tm, name, tm.store(purify_data(p.data)))
        r1_dumped = tm_save_poset(tm, name, r1)
        r2 = tm_load_poset(tm, name + "-re", r1_dumped)


@tfor(I.FinitePosetMeasurement)
def test_FinitePosetMeasurements(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.FinitePosetMeasurement)

    d = get_test_posets()
    for rname, rinfo in d.items():

        def get(p: Any) -> Any:
            return rinfo.properties.get(p, None)

        r1 = tm_load_poset(tm, rname, tm.store(purify_data(rinfo.data)))
        width = get("width")
        if width is not None:
            tm.addtest(check_poset_width, mks, r1, width, tid0=f"check_poset_width-{rname}")
        height = get("height")
        if height is not None:
            tm.addtest(check_poset_height, mks, r1, height, tid0=f"check_poset_height-{rname}")


@tfor(I.FinitePosetClosures)
def test_FinitePosetClosures(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.FinitePosetClosures)
    d = get_test_posets()
    raise TestNotImplemented()


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

    # p2 = tc.check_result(frp, frp.opposite, I.FinitePoset, p_op)  # check_same_poset(tc, p, p2)


def check_same_poset(tc: TestContext, s1: I.FinitePoset[X], s2: I.FinitePoset[X]) -> None:
    check_same_set(tc, s1.carrier(), s2.carrier())

    es = list(s1.carrier().elements())

    for a, b in itertools.product(es, es):
        h1 = tc.check_result(s1, s1.holds, bool, a, b)
        h2 = tc.check_result(s2, s2.holds, bool, a, b)
        if h1 != h2:
            tc.fail(zh.span("Different at"), a=a, b=b, h1=h1, h2=h2)

    # check_same_map(c, s1.holds(), s2.holds())


@tfor(I.FinitePosetSubsetProperties)
def test_FinitePosetSubsetProperties(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.FinitePosetSubsetProperties)
    d = get_test_posets()
    for rname, rinfo in d.items():

        def get(p: Any) -> Any:
            return rinfo.properties.get(p, {})

        r1 = tm_load_poset(tm, rname, tm.store(purify_data(rinfo.data)))
        some_chains = get("some_chains")
        for k, v in some_chains.items():
            tm.addtest(check_is_chain, mks, r1, v, True, tid0=f"check_is_chain-{rname}-{k}")
        some_not_chains = get("some_not_chains")
        for k, v in some_not_chains.items():
            tm.addtest(check_is_chain, mks, r1, v, False, tid0=f"check_is_not_chain-{rname}-{k}")
        some_antichains = get("some_antichains")
        for k, v in some_antichains.items():
            tm.addtest(check_is_antichain, mks, r1, v, True, tid0=f"check_is_antichain-{rname}-{k}")
        some_not_antichains = get("some_not_antichains")
        for k, v in some_not_antichains.items():
            tm.addtest(check_is_antichain, mks, r1, v, False, tid0=f"check_is_not_antichain-{rname}-{k}")


@tfor(I.FinitePosetSubsetProperties2)
def test_FinitePosetSubsetProperties2(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.FinitePosetSubsetProperties2)
    d = get_test_posets()
    for rname, rinfo in d.items():

        def get(p: Any) -> Any:
            return rinfo.properties.get(p, {})

        r1 = tm_load_poset(tm, rname, tm.store(purify_data(rinfo.data)))
        some_uppersets = get("some_uppersets")
        for k, v in some_uppersets.items():
            tm.addtest(check_is_upperset, mks, r1, v, True, tid0=f"check_is_upperset-{rname}-{k}")
        some_not_uppersets = get("some_not_uppersets")
        for k, v in some_not_uppersets.items():
            tm.addtest(check_is_upperset, mks, r1, v, False, tid0=f"check_is_not_upperset-{rname}-{k}")
        some_lowersets = get("some_lowersets")
        for k, v in some_lowersets.items():
            tm.addtest(check_is_lowerset, mks, r1, v, True, tid0=f"check_is_lowerset-{rname}-{k}")
        some_not_uppersets = get("some_not_lowersets")
        for k, v in some_not_uppersets.items():
            tm.addtest(check_is_lowerset, mks, r1, v, False, tid0=f"check_is_not_lowerset-{rname}-{k}")


@tfor(I.FinitePosetConstructionSum)
def check_poset_disjoint_union(tc: TestContext) -> None:
    msd: I.FinitePosetConstructionSum = find_imp(tc, I.FinitePosetConstructionSum)
    poset_empty = load_poset_tc(tc, "poset_empty")

    poset2 = tc.check_result(msd, msd.disjoint_union, I.FinitePosetDisjointUnion, [poset_empty, poset_empty])
    logger.info(poset2=poset2)

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
        msg = zh.span(f"Expected is_antichain = {expect}, obtained {res}.")
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


#
# def load_group_tc(tc: TestContext, name: str):
#     fgr = find_imp(tc, I.FiniteGroupRepresentation)
#     h = IOHelperImp()
#     data1 = get_group_data(name)
#     return loadit_(tc, fgr, h, data1, I.FiniteGroup)
