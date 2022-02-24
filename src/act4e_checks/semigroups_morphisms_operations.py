from typing import (
    TypeVar,
)

import zuper_html as zh
from zuper_testint import find_imp, TestContext, TestManagerInterface, tfor

import act4e_interfaces as I
from .data import get_test_data
from .semigroups_morphisms_representation import load_morphism_monoid, load_morphism_semigroup


A = TypeVar("A")
B = TypeVar("B")


@tfor(I.FiniteSemigroupMorphismsChecks)
def test_check_semigroup_morphism(tm: TestManagerInterface) -> None:
    tm.impof(I.FiniteSemigroupMorphismsChecks)
    cases = get_test_data("semigroup_morphism")

    for name, data in cases.items():
        valid = data.tags["semigroup_morphism"]
        tm.addtest(
            tc_check_semigroup_morphism, name, valid, tid0=f"tc_check_semigroup_morphism-{name}-{valid}"
        )


def tc_check_semigroup_morphism(tc: TestContext, name: str, valid: bool) -> None:
    f: I.FiniteSemigroupMorphismsChecks = find_imp(tc, I.FiniteSemigroupMorphismsChecks)
    l = load_morphism_semigroup(tc, name)

    with tc.description(f"checking {name}"):
        res = tc.check_result(f, f.is_semigroup_morphism, bool, l.source(), l.target(), l.mapping())
        if res != valid:
            msg = f"Expected: {valid} obtained {res}"
            tc.fail(zh.span(msg))


@tfor(I.FiniteSemigroupMorphismsChecks)
def test_check_monoid_morphism(tm: TestManagerInterface) -> None:
    tm.impof(I.FiniteSemigroupMorphismsChecks)
    cases = get_test_data("monoid_morphism")

    for name, data in cases.items():
        valid = data.tags["monoid_morphism"]
        tm.addtest(tc_check_semigroup_morphism, name, valid, tid0=f"tc_check_monoid_morphism-{name}-{valid}")


def tc_check_monoid_morphism(tc: TestContext, name: str, valid: bool) -> None:
    f: I.FiniteSemigroupMorphismsChecks = find_imp(tc, I.FiniteSemigroupMorphismsChecks)
    l = load_morphism_monoid(tc, name)

    with tc.description(f"checking {name}"):
        res = tc.check_result(f, f.is_monoid_morphism, bool, l.source(), l.target(), l.mapping())
        if res != valid:
            msg = f"Expected: {valid} obtained {res}"
            tc.fail(zh.span(msg))


@tfor(I.FiniteSemigroupMorphismsChecks)
def test_check_group_morphism(tm: TestManagerInterface) -> None:
    tm.impof(I.FiniteSemigroupMorphismsChecks)
    cases = get_test_data("group_morphism")

    for name, data in cases.items():
        valid = data.tags["monoid_morphism"]
        tm.addtest(tc_check_group_morphism, name, valid, tid0=f"tc_check_group_morphism-{name}-{valid}")


def tc_check_group_morphism(tc: TestContext, name: str, valid: bool) -> None:
    f: I.FiniteSemigroupMorphismsChecks = find_imp(tc, I.FiniteSemigroupMorphismsChecks)
    l = load_morphism_monoid(tc, name)

    with tc.description(f"checking {name}"):
        res = tc.check_result(f, f.is_group_morphism, bool, l.source(), l.target(), l.mapping())
        if res != valid:
            msg = f"Expected: {valid} obtained {res}"
            tc.fail(zh.span(msg))
