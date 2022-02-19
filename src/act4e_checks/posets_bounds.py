from typing import (
    Any,
)

from zuper_testint import TestManagerInterface, TestNotImplemented, tfor

import act4e_interfaces as I
from .data import get_test_posets, purify_data
from .posets_utils import (
    check_is_antichain,
    check_is_chain,
    check_is_lowerset,
    check_is_upperset,
    check_poset_height,
    check_poset_width,
    tm_load_poset,
)


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
