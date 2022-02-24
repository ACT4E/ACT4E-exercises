from typing import (
    Any,
    TypeVar,
)

from zuper_testint import find_imp, TestContext, TestManagerInterface, tfor

import act4e_interfaces as I
from .data import dump_using, get_test_data, IOHelperImp, load_using, loadit_
from .maps import check_same_function
from .semigroups import check_same_monoid, check_same_semigroup


@tfor(I.FiniteSemigroupMorphismRepresentation)
def test_load_semigroup_morphism(tm: TestManagerInterface) -> None:
    tm.impof(I.FiniteSemigroupMorphismRepresentation)
    cases = get_test_data("semigroup_morphism")

    for name in cases:
        tm.addtest(tc_check_load_semigroup_morphism, name, tid0=f"check-load-semigroup-morphism-{name}")


A = TypeVar("A")
B = TypeVar("B")


def tc_check_load_semigroup_morphism(tc: TestContext, name: str) -> None:
    l = load_morphism_semigroup(tc, name)
    saved = save_morphism_semigroup(tc, l)
    l2 = load_morphism_semigroup_data(tc, saved)
    check_same_semigroup_morphism(tc, l, l2)


def tc_check_load_monoid_morphism(tc: TestContext, name: str) -> None:
    l = load_morphism_monoid(tc, name)
    saved = save_morphism_monoid(tc, l)
    l2 = load_morphism_monoid_data(tc, saved)
    check_same_monoid_morphism(tc, l, l2)


def tc_check_load_group_morphism(tc: TestContext, name: str) -> None:
    l = load_morphism_group(tc, name)
    saved = save_morphism_group(tc, l)
    l2 = load_morphism_group_data(tc, saved)
    check_same_group_morphism(tc, l, l2)


def check_same_semigroup_morphism(
    tc: TestContext, l1: I.FiniteSemigroupMorphism[A, B], l2: I.FiniteSemigroupMorphism[A, B]
) -> None:
    source1: I.FiniteSemigroup[A] = tc.check_result(l1, l1.source, I.FiniteSemigroup)
    source2: I.FiniteSemigroup[A] = tc.check_result(l2, l2.source, I.FiniteSemigroup)
    check_same_semigroup(tc, source1, source2)
    target1: I.FiniteSemigroup[B] = tc.check_result(l1, l1.target, I.FiniteSemigroup)
    target2: I.FiniteSemigroup[B] = tc.check_result(l2, l2.target, I.FiniteSemigroup)
    check_same_semigroup(tc, target1, target2)
    mapping1: I.FiniteMap[A, B] = tc.check_result(l1, l1.mapping, I.FiniteMap)
    mapping2: I.FiniteMap[A, B] = tc.check_result(l2, l2.mapping, I.FiniteMap)
    check_same_function(tc, mapping1, mapping2)


def check_same_monoid_morphism(
    tc: TestContext, l1: I.FiniteMonoidMorphism[A, B], l2: I.FiniteMonoidMorphism[A, B]
) -> None:
    source1: I.FiniteMonoid[A] = tc.check_result(l1, l1.source, I.FiniteMonoid)
    source2: I.FiniteMonoid[A] = tc.check_result(l2, l2.source, I.FiniteMonoid)
    check_same_monoid(tc, source1, source2)
    target1: I.FiniteMonoid[B] = tc.check_result(l1, l1.target, I.FiniteMonoid)
    target2: I.FiniteMonoid[B] = tc.check_result(l2, l2.target, I.FiniteMonoid)
    check_same_monoid(tc, target1, target2)
    mapping1: I.FiniteMap[A, B] = tc.check_result(l1, l1.mapping, I.FiniteMap)
    mapping2: I.FiniteMap[A, B] = tc.check_result(l2, l2.mapping, I.FiniteMap)
    check_same_function(tc, mapping1, mapping2)


def check_same_group_morphism(
    tc: TestContext, l1: I.FiniteGroupMorphism[A, B], l2: I.FiniteGroupMorphism[A, B]
) -> None:
    source1: I.FiniteGroup[A] = tc.check_result(l1, l1.source, I.FiniteGroup)
    source2: I.FiniteGroup[A] = tc.check_result(l2, l2.source, I.FiniteGroup)
    check_same_monoid(tc, source1, source2)
    target1: I.FiniteGroup[B] = tc.check_result(l1, l1.target, I.FiniteGroup)
    target2: I.FiniteGroup[B] = tc.check_result(l2, l2.target, I.FiniteGroup)
    check_same_monoid(tc, target1, target2)
    mapping1: I.FiniteMap[A, B] = tc.check_result(l1, l1.mapping, I.FiniteMap)
    mapping2: I.FiniteMap[A, B] = tc.check_result(l2, l2.mapping, I.FiniteMap)
    check_same_function(tc, mapping1, mapping2)


@tfor(I.FiniteMonoidMorphismRepresentation)
def test_load_monoid_morphism(tm: TestManagerInterface) -> None:
    tm.impof(I.FiniteMonoidMorphismRepresentation)
    cases = get_test_data("monoid_morphism")

    for name in cases:
        tm.addtest(tc_check_load_monoid_morphism, name, tid0=f"check-load-monoid-morphism-{name}")


@tfor(I.FiniteGroupMorphismRepresentation)
def test_load_group_morphism(tm: TestManagerInterface) -> None:
    tm.impof(I.FiniteGroupMorphismRepresentation)
    cases = get_test_data("group_morphism")

    for name in cases:
        tm.addtest(tc_check_load_group_morphism, name, tid0=f"check-load-group-morphism-{name}")


def load_morphism_semigroup(tc: TestContext, name: str) -> I.FiniteSemigroupMorphism[Any, Any]:
    return load_using(tc, name, I.FiniteSemigroupMorphismRepresentation, I.FiniteSemigroupMorphism)


def load_morphism_semigroup_data(
    tc: TestContext, data: I.FiniteSemigroupMorphism_desc
) -> I.FiniteSemigroupMorphism[Any, Any]:
    h = IOHelperImp()
    fsr = find_imp(tc, I.FiniteSemigroupMorphismRepresentation)
    return loadit_(tc, fsr, h, data, I.FiniteSemigroupMorphism)


def load_morphism_monoid_data(
    tc: TestContext, data: I.FiniteMonoidMorphism_desc
) -> I.FiniteMonoidMorphism[Any, Any]:
    h = IOHelperImp()
    fsr = find_imp(tc, I.FiniteMonoidMorphismRepresentation)
    return loadit_(tc, fsr, h, data, I.FiniteMonoidMorphism)


def load_morphism_group_data(
    tc: TestContext, data: I.FiniteGroupMorphism_desc
) -> I.FiniteGroupMorphism[Any, Any]:
    h = IOHelperImp()
    fsr = find_imp(tc, I.FiniteGroupMorphismRepresentation)
    return loadit_(tc, fsr, h, data, I.FiniteGroupMorphism)


def load_morphism_monoid(tc: TestContext, name: str) -> I.FiniteMonoidMorphism[Any, Any]:
    return load_using(tc, name, I.FiniteMonoidMorphismRepresentation, I.FiniteMonoidMorphism)


def load_morphism_group(tc: TestContext, name: str) -> I.FiniteGroupMorphism[Any, Any]:
    return load_using(tc, name, I.FiniteGroupMorphismRepresentation, I.FiniteGroupMorphism)


def save_morphism_semigroup(
    tc: TestContext, x: I.FiniteSemigroupMorphism[Any, Any]
) -> I.FiniteSemigroupMorphism_desc:
    return dump_using(tc, I.FiniteSemigroupMorphismRepresentation, x)


def save_morphism_monoid(tc: TestContext, x: I.FiniteMonoidMorphism[Any, Any]) -> I.FiniteMonoidMorphism_desc:
    return dump_using(tc, I.FiniteMonoidMorphismRepresentation, x)


def save_morphism_group(tc: TestContext, x: I.FiniteGroupMorphism[Any, Any]) -> I.FiniteGroupMorphism_desc:
    return dump_using(tc, I.FiniteGroupMorphismRepresentation, x)
