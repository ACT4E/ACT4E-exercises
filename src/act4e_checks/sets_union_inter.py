from typing import TypeVar

from zuper_testint import TestContext, TestManagerInterface, tfor

import act4e_interfaces as I
from .sets import tm_check_subset
from .sets_utils import good_load_set, set_coherence

E = TypeVar("E")
X = TypeVar("X")


@tfor(I.FiniteMakeSetUnion)
def test_MakeSetUnion(tm: TestManagerInterface) -> None:
    A = good_load_set("set1")
    B = good_load_set("set2")
    msu = tm.impof(I.FiniteMakeSetUnion)
    AuB = tm.addtest(set_union, msu, A, B)
    tm.addtest(set_coherence, AuB)
    tm_check_subset(tm, A, AuB, True, "A-union")
    tm_check_subset(tm, B, AuB, True, "B-union")


@tfor(I.FiniteMakeSetIntersection)
def test_FiniteMakeSetIntersection(tm: TestManagerInterface) -> None:
    A = good_load_set("set1")
    B = good_load_set("set2")
    msi = tm.impof(I.FiniteMakeSetIntersection)
    intersection = tm.addtest(set_intersection, msi, A, B)
    tm_check_subset(tm, intersection, A, True, "A-intersection")
    tm_check_subset(tm, intersection, B, True, "B-intersection")


def set_intersection(
    tc: TestContext, fso: I.FiniteMakeSetIntersection, a: I.FiniteSet[X], b: I.FiniteSet[X]
) -> I.FiniteSet[X]:
    return fso.intersection([a, b])  # FIXME: exceptions


def set_union(
    tc: TestContext, fso: I.FiniteMakeSetUnion, a: I.FiniteSet[X], b: I.FiniteSet[X]
) -> I.FiniteSet[X]:
    return fso.union([a, b])  # FIXME: exceptions
