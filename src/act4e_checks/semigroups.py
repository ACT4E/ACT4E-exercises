import itertools
from functools import partial
from typing import (
    Any,
    Callable,
    List,
    TypeVar,
)

import zuper_html as zh
from zuper_commons.types import check_isinstance
from zuper_testint import find_imp, ImplementationFail, TestContext, TestManagerInterface, TestRef, tfor

import act4e_interfaces as I
from .data import dumpit_, get_test_data, IOHelperImp, loadit_, purify_data
from .maps import check_map_involutive
from .sets_utils import check_same_set, good_load_set, make_set, make_values

E = TypeVar("E")
X = TypeVar("X")


@tfor(I.FiniteSemigroupConstruct)
def test_FiniteSemigroupConstruct(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.FiniteSemigroupConstruct)

    A = good_load_set("set1")
    B = good_load_set("set2")
    for s in (A, B):
        tm.addtest(check_free_semigroup, mks, s)


def check_free_semigroup(tc: TestContext, fsg: I.FiniteSemigroupConstruct, s: I.FiniteSet[X]) -> None:
    fs = tc.check_result(fsg, fsg.free, I.FreeSemigroup, s)
    carrier = fs.carrier()

    for a0, b0 in itertools.product(s.elements(), s.elements()):
        a = tc.check_result(fs, fs.unit, object, a0)
        b = tc.check_result(fs, fs.unit, object, b0)
        res = tc.check_result(fs, fs.compose, object, a, b)
        if not carrier.contains(res):
            msg = "Composition result does not belong to set."
            raise ImplementationFail(msg, a=a, b=b, res=res)


def check_semigroup(tc: TestContext, m: I.FiniteSemigroup[E]) -> None:
    carrier = m.carrier()
    elements = list(carrier.elements())
    for e1, e2 in itertools.product(elements, elements):
        e = tc.check_result(m, m.compose, object, e1, e2)
        inside = tc.check_result(carrier, carrier.contains, object, e)
        if not inside:
            tc.fail(zh.span("composition fails"), e1=e1, e2=e2, e=e, inside=inside)


def check_monoid(tc: TestContext, m: I.FiniteMonoid[E]) -> None:
    check_semigroup(tc, m)
    m.identity()


def check_group(tc: TestContext, m: I.FiniteGroup[E]) -> None:
    with tc.description("checking it is a valid monoid"):
        check_monoid(tc, m)

    with tc.description("checking group composition"):
        check_group_composition(tc, m)

    with tc.description("checking that the inverse is involutive"):
        check_map_involutive(tc, m.carrier(), m.inverse)


def check_group_composition(tc: TestContext, G: I.FiniteGroup[E]) -> None:
    carrier = G.carrier()
    neutral = G.identity()
    for e in carrier.elements():
        e_inv = G.inverse(e)  # TODO: wrap
        e_ei = G.compose(e, e_inv)
        e_ie = G.compose(e_inv, e)

        with tc.description("Checking that id = e*inv(e)"):
            tc.f_expect_equal2(
                partial(carrier.equal, neutral, e_ei),
                lambda: True,
                zh.span("id != e*i"),
                neutral=neutral,
                e=e,
                e_inv=e_inv,
                e_times_e_inv=e_ei,
            )
        with tc.description("Checking that id = inv(e)*e"):
            tc.f_expect_equal2(
                partial(carrier.equal, neutral, e_ie),
                lambda: True,
                zh.span("id != i*e"),
                neutral=neutral,
                e=e,
                e_inv=e_inv,
                e_inv_times_e=e_ie,
            )


def check_same_semigroup(tc: TestContext, g1: I.FiniteSemigroup[X], g2: I.FiniteSemigroup[X]) -> None:
    carrier = g1.carrier()
    check_same_set(tc, g1.carrier(), g2.carrier())
    elements = list(carrier.elements())

    for a, b in itertools.product(elements, elements):
        r1 = g1.compose(a, b)
        r2 = g2.compose(a, b)
        eq = carrier.equal(r1, r2)
        if not eq:
            msg = zh.span("Not equal at ")
            tc.fail(msg, a=a, b=b, r1=r1, r2=r2)


def check_same_monoid(tc: TestContext, g1: I.FiniteMonoid[X], g2: I.FiniteMonoid[X]) -> None:
    check_same_semigroup(tc, g1, g2)
    id1 = g1.identity()
    id2 = g2.identity()
    carrier = g1.carrier()
    eq = carrier.equal(id1, id2)
    if not eq:
        msg = zh.span("Different identity")
        tc.fail(msg, id1=id1, id2=id2)


def check_same_group(tc: TestContext, g1: I.FiniteGroup[X], g2: I.FiniteGroup[X]) -> None:
    check_same_monoid(tc, g1, g2)
    carrier = g1.carrier()

    for a in carrier.elements():
        r1 = g1.inverse(a)
        r2 = g2.inverse(a)
        eq = carrier.equal(r1, r2)
        if not eq:
            msg = zh.span("Inverse not equal to  a")
            tc.fail(msg, a=a, r1=r1, r2=r2)


def tm_load_semigroup(
    tm: TestManagerInterface,
    name: str,
    data: TestRef[I.FiniteSemigroup_desc],
) -> TestRef[I.FiniteSemigroup[Any]]:
    h = IOHelperImp()

    # if 'data' in data:
    #     raise ValueError(data)

    def loadit(
        c: TestContext, fsr: I.FiniteSemigroupRepresentation, data1: I.FiniteSemigroup_desc
    ) -> I.FiniteSemigroup[Any]:
        return loadit_(c, fsr, h, data1, I.FiniteSemigroup)

    fsr_ = tm.impof(I.FiniteSemigroupRepresentation)
    return tm.addtest(loadit, fsr_, data, tid0=f"load-semigroup-{name}")


def tm_save_semigroup(
    tm: TestManagerInterface, name: str, sgr: TestRef[I.FiniteSemigroup[Any]]
) -> TestRef[I.FiniteSemigroup_desc]:
    h = IOHelperImp()

    def dumpit(
        c: TestContext, fsr: I.FiniteSemigroupRepresentation, sgr_: I.FiniteSemigroup[Any]
    ) -> I.FiniteSemigroup_desc:
        return dumpit_(c, fsr, h, sgr_)

    fsr_ = tm.impof(I.FiniteSemigroupRepresentation)
    return tm.addtest(dumpit, fsr_, sgr, tid0=f"save-semigroup-{name}")


def tm_save_monoid(
    tm: TestManagerInterface, name: str, sgr: TestRef[I.FiniteMonoid[Any]]
) -> TestRef[I.FiniteMonoid_desc]:
    h = IOHelperImp()

    def dumpit(
        c: TestContext, fsr: I.FiniteMonoidRepresentation, sgr_: I.FiniteMonoid[Any]
    ) -> I.FiniteMonoid_desc:
        return dumpit_(c, fsr, h, sgr_)

    fsr_ = tm.impof(I.FiniteMonoidRepresentation)
    return tm.addtest(dumpit, fsr_, sgr, tid0=f"save-monoid-{name}")


def tm_save_group(
    tm: TestManagerInterface, name: str, sgr: TestRef[I.FiniteGroup[Any]]
) -> TestRef[I.FiniteGroup_desc]:
    h = IOHelperImp()

    def dumpit(
        tc: TestContext, fsr: I.FiniteGroupRepresentation, sgr_: I.FiniteGroup[Any]
    ) -> I.FiniteGroup_desc:
        return dumpit_(tc, fsr, h, sgr_)

    fsr_ = tm.impof(I.FiniteGroupRepresentation)
    return tm.addtest(dumpit, fsr_, sgr, tid0=f"dump-group-{name}")


def tm_load_group(
    tm: TestManagerInterface, name: str, data: TestRef[I.FiniteGroup_desc]
) -> TestRef[I.FiniteGroup[Any]]:
    h = IOHelperImp()

    def loadit(
        tc: TestContext, fsr: I.FiniteGroupRepresentation, data1: I.FiniteGroup_desc
    ) -> I.FiniteGroup[Any]:
        return loadit_(tc, fsr, h, data1, I.FiniteGroup)

    fsr_ = tm.impof(I.FiniteGroupRepresentation)
    return tm.addtest(loadit, fsr_, data, tid0=f"load-group-{name}")


def tm_load_monoid(
    tm: TestManagerInterface, name: str, data: TestRef[I.FiniteMonoid_desc]
) -> TestRef[I.FiniteMonoid[Any]]:
    h = IOHelperImp()

    def loadit(
        c: TestContext, fsr: I.FiniteMonoidRepresentation, data1: I.FiniteMonoid_desc
    ) -> I.FiniteMonoid[Any]:
        return loadit_(c, fsr, h, data1, I.FiniteMonoid)

    fsr_ = tm.impof(I.FiniteMonoidRepresentation)
    return tm.addtest(loadit, fsr_, data, tid0=f"load-monoid-{name}")


def make_semigroup(s: List[X], f: Callable[[X, X], X]) -> I.FiniteSemigroup_desc:
    check_isinstance(s, list)
    fs = make_set(s)
    res: I.FiniteSemigroup_desc = {
        "carrier": fs,
        "composition": make_values(s, f),
    }
    # logger.info(res=res)
    return res


@tfor(I.FiniteMonoidRepresentation)
def test_FiniteMonoidRepresentation(tm: TestManagerInterface) -> None:
    monoids = get_test_data("monoid")

    for name, m in monoids.items():
        data = m.data
        mon = tm_load_monoid(tm, name, data)
        mon2 = tm_save_monoid(tm, name, mon)
        tm_load_monoid(tm, name + "-re", mon2)
        tm.addtest(check_monoid, mon)


@tfor(I.FiniteSemigroupRepresentation)
def test_FiniteSemigroupRepresentation(tm: TestManagerInterface) -> None:
    semigroups = get_test_data("semigroup")
    for sgrp_name, s in semigroups.items():
        data = s.data

        fs = tm_load_semigroup(tm, sgrp_name, data)
        data2 = tm_save_semigroup(tm, sgrp_name, fs)
        fs = tm_load_semigroup(tm, sgrp_name + "-re", data2)


@tfor(I.FiniteGroupRepresentation)
def test_FiniteGroupRepresentation(tm: TestManagerInterface) -> None:
    groups = get_test_data("group")

    for name in groups:
        tm.addtest(check_group_load_save, name, tid0=f"check_group_load_save-{name}")


def check_group_load_save(tc: TestContext, name: str) -> None:
    desc = f"Checking if we can save/load the test group called {name}"
    with tc.description(desc):
        with tc.description(f"Trying to load the group {name}"):
            g1 = load_group_tc(tc, name)

        with tc.description("Checking it is a valid group"):
            check_group(tc, g1)

        with tc.description("Trying to save the group"):
            g1_dumped = save_group_tc(tc, g1)

        with tc.description("Trying to re-load the saved group"):
            fgr: I.FiniteGroupRepresentation = find_imp(tc, I.FiniteGroupRepresentation)
            h = IOHelperImp()
            g2 = fgr.load(h, g1_dumped)

        with tc.description("Checking the reloaded is a valid group"):
            check_group(tc, g1)

        tc.raise_if_failures()
        with tc.description("Checking the original and reloaded groups are the same"):
            check_same_group(tc, g1, g2)


def save_group_tc(tc: TestContext, g: I.FiniteGroup[Any]) -> I.FiniteGroup_desc:
    fgr: I.FiniteGroupRepresentation = find_imp(tc, I.FiniteGroupRepresentation)
    h = IOHelperImp()

    return dumpit_(tc, fgr, h, g)


def get_group_data(name: str) -> I.ConcreteRepr:
    d = get_test_data("group")
    data1 = purify_data(d[name].data)
    return data1


def load_group_tc(tc: TestContext, name: str) -> I.FiniteGroup[Any]:
    fgr: I.FiniteGroupRepresentation = find_imp(tc, I.FiniteGroupRepresentation)
    h = IOHelperImp()
    data1 = get_group_data(name)
    # not sure why
    return loadit_(tc, fgr, h, data1, I.FiniteGroup)  # type: ignore
