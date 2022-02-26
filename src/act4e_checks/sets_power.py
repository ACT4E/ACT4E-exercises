import itertools
from typing import Iterable, Iterator, Tuple, TypeVar

import zuper_html as zh
from zuper_testint import TestContext, TestManagerInterface, tfor

import act4e_interfaces as I
from .data import get_test_sets, purify_data
from .sets_representation import tm_load_set

E = TypeVar("E")
X = TypeVar("X")


@tfor(I.FiniteMakePowerSet)
def test_FiniteMakePowerSet(tm: TestManagerInterface) -> None:
    mps = tm.impof(I.FiniteMakePowerSet)

    d = get_test_sets()

    names = ["set_empty", "set_one", "set_two", "set2"]

    for name in names:
        info = d[name]
        # def get(p):
        #     return info.properties.get(p, None)

        # powerset = get('powerset')
        # if powerset:
        s1 = tm_load_set(tm, name, tm.store(purify_data(info.data)))
        # info2 = d[powerset]
        # s2 = tm_load_set(tm, powerset, tm.store(info2.data))

        tm.addtest(check_powerset, mps, s1, tid0=f"check_power_set-{name}")


def powerset(iterable: Iterable[X]) -> Iterator[Tuple[X, ...]]:
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s) + 1))


def check_powerset(tc: TestContext, fsp: I.FiniteMakePowerSet, a: I.FiniteSet[X]) -> None:
    if a.size() > 5:
        return

    res = tc.check_result(fsp, fsp.powerset, I.FiniteSetOfFiniteSubsets, a)

    S = list(a.elements())
    for _ in powerset(S):
        e = tc.check_result(res, res.construct, object, list(_))
        contained = tc.check_result(res, res.contains, bool, e)
        if not contained:
            tc.fail(
                zh.span("element not contained"), e=e
            )  # # logger.info(original=a, expected=b, res=str(res))  # check_set(c,  # res)  #
            # check_same_set(c, res, b)  # for e in res.elements():  #     inside = list(  # res.contents(
            # e))  #     e2 = res.construct(inside)  #     equal = res.equal(e2, e)  #     if  # not equal:
            #         tc.fail(zh.span('Elements should be equal'), e=e, inside=inside, e2=e2,  # equal=equal)
