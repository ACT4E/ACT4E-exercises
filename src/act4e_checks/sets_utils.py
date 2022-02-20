import itertools
from typing import Any, Callable, List, Sequence, TypeVar

import zuper_html as zh
from zuper_testint import find_imp, TestContext

import act4e_interfaces as I
from .actual_tests import good_fsr
from .data import get_test_sets, IOHelperImp, loadit_, purify_data

E = TypeVar("E")
X = TypeVar("X")


def check_lists_same(tc: TestContext, S: I.FiniteSet[X], s1: List[X], s2: List[X]) -> None:
    if len(s1) != len(s2):
        msg = "Lists have different number of elements"
        tc.fail(zh.span(msg), s1=s1, s2=s2)
        return

    for a in s1:
        included = any(tc.check_result(S, S.equal, bool, a, b) for b in s2)
        if not included:
            tc.fail(zh.span("Element not in the set"), a=a, s1=s1, s2=s2)


def load_list(tc: TestContext, S: I.FiniteSet[X], a: List[I.ConcreteRepr]) -> List[X]:
    h = IOHelperImp()
    s2 = [tc.check_result(S, S.load, object, h, _) for _ in a]
    return s2


def check_same_element(tc: TestContext, s1: I.FiniteSet[X], a: X, b: X) -> None:
    tc.check_result_value(
        s1, s1.equal, bool, True, a, b
    )  # # if not s1.equal(a, b):  #     msg = zh.span("Elements are not the same")  #     tc.fail(
    # msg, a=a, b=b)  #     raise ImplementationFail()


def check_same_set(tc: TestContext, s1: I.FiniteSet[X], s2: I.FiniteSet[X]) -> None:
    elements1 = list(s1.elements())
    elements2 = list(s2.elements())
    for e1 in elements1:
        belongs = tc.check_result(s2, s2.contains, bool, e1)
        if not belongs:
            msg = zh.span("Element in first set does not belong to the second set")
            tc.fail(msg, e1=e1)
    for e2 in elements2:
        belongs = tc.check_result(s1, s1.contains, bool, e2)
        if not belongs:
            msg = zh.span("Element in second set does not belong to the first set")
            tc.fail(msg, e2=e2)


def set_coherence(tc: TestContext, fi: I.FiniteSet[X]) -> None:
    a = len(list(fi.elements()))
    b = fi.size()
    if a != b:
        tc.fail(zh.p("size() and elements() are not coherent"))
    for element in fi.elements():
        if not fi.contains(element):
            tc.fail(zh.p("element in the set does not pass contains()"), element=element)
        if not fi.equal(element, element):
            tc.fail(zh.p("element in the set is not equal to itself"), element=element)


def make_values1(s: Sequence[X], f: Callable[[X], X]) -> List[List[X]]:
    return [[x, f(x)] for x in s]


def make_values(s: Sequence[X], f: Callable[[X, X], X]) -> List[Any]:
    return [[[x, y], f(x, y)] for x, y in itertools.product(s, s)]


def make_set(s: List[Any]) -> I.FiniteSet_desc:
    return {"elements": s}


def load_set(fsp: I.FiniteSetRepresentation, name: str) -> I.FiniteSet[Any]:
    d = get_test_sets()
    h = IOHelperImp()
    p1: I.FiniteSet[Any] = fsp.load(h, purify_data(d[name].data))
    return p1


def good_load_set(setname: str) -> I.FiniteSet[Any]:
    h = IOHelperImp()
    data = get_set_data(setname)

    return good_fsr.load(h, data)


def good_make_set(elements: Sequence[Any]) -> I.FiniteSet[Any]:
    h = IOHelperImp()
    return good_fsr.load(h, {"elements": list(elements)})


def load_set_tc(tc: TestContext, name: str) -> I.FiniteSet[Any]:
    fsr: I.FiniteSetRepresentation = find_imp(tc, I.FiniteSetRepresentation)
    data1 = get_set_data(name)
    h = IOHelperImp()
    return loadit_(tc, fsr, h, data1, I.FiniteSet)


def get_set_data(name: str) -> I.FiniteSet_desc:
    d = get_test_sets()
    data1 = purify_data(d[name].data)
    return data1
