from typing import (
    Any,
    List,
)

from zuper_testint import find_imp, TestContext, TestManagerInterface, tfor

import act4e_interfaces as I
from .data import get_test_posets, purify_data
from .posets_utils import (
    check_is_antichain,
    check_is_chain,
    check_is_lowerset,
    check_is_upperset,
    check_poset_height,
    check_poset_width,
    load_poset_tc,
    tm_load_poset,
)
from .sets_utils import check_lists_same, load_list


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
    for rname, rinfo in d.items():

        def get(p: Any) -> Any:
            return rinfo.properties.get(p, None)

        s = get("some_upper_closures")
        if s is not None:
            for i, x in enumerate(s):
                tid = f"check_upper_closures-{rname}-{i}"
                tm.addtest(check_upper_closures, rname, x["S"], x["upper_closure"], tid0=tid)
        s = get("some_lower_closures")
        if s is not None:
            for i, x in enumerate(s):
                tid = f"check_upper_closures-{rname}-{i}"
                tm.addtest(check_lower_closures, rname, x["S"], x["lower_closure"], tid0=tid)


def check_lower_closures(
    tc: TestContext, poset_name: str, S_raw: List[I.ConcreteRepr], expected_raw: List[I.ConcreteRepr]
) -> None:
    P = load_poset_tc(tc, poset_name)
    carrier = tc.check_result(P, P.carrier, I.FiniteSet)
    S = load_list(tc, carrier, S_raw)
    expected = load_list(tc, carrier, expected_raw)

    fpc: I.FinitePosetClosures = find_imp(tc, I.FinitePosetClosures)
    cl = tc.check_result(fpc, fpc.lower_closure, list, P, S)
    with tc.description("checking correct lower closure", S=S, expected=expected, obtained=cl):
        check_lists_same(tc, carrier, expected, cl)


def check_upper_closures(
    tc: TestContext, poset_name: str, S_raw: List[I.ConcreteRepr], expected_raw: List[I.ConcreteRepr]
) -> None:
    P = load_poset_tc(tc, poset_name)
    carrier = tc.check_result(P, P.carrier, I.FiniteSet)
    S = load_list(tc, carrier, S_raw)
    expected = load_list(tc, carrier, expected_raw)

    fpc: I.FinitePosetClosures = find_imp(tc, I.FinitePosetClosures)
    cl = tc.check_result(fpc, fpc.upper_closure, list, P, S)
    with tc.description("checking correct upper closure", S=S, expected=expected, obtained=cl):
        check_lists_same(tc, carrier, expected, cl)


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
