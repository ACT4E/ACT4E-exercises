from typing import TypeVar, Union

import zuper_html as zh
from zuper_commons.types import ZValueError
from zuper_html_plus import html_from_object
from zuper_testint import TestContext, TestManagerInterface, TestRef, tfor

import act4e_interfaces as I
from .data import check_good_output, get_test_data, IOHelperImp
from .sets_representation import tm_load_set

E = TypeVar("E")
X = TypeVar("X")


def tm_check_subset(
    tm: TestManagerInterface,
    a: Union[I.FiniteSet[X], TestRef[I.FiniteSet[X]]],
    b: Union[I.FiniteSet[X], TestRef[I.FiniteSet[X]]],
    expect: bool,
    tid: str,
) -> TestRef[None]:
    fsp = tm.impof(I.FiniteSetProperties)
    return tm.addtest(check_subset, fsp, a, b, expect, tid0="subset-" + tid)


def test_notnone(tc: TestContext, x: X) -> X:
    if x is None:
        tc.fail(zh.p("None obtained"))
    return x


@tfor(I.FiniteSetProperties)
def test_FiniteSetProperties(tm: TestManagerInterface) -> None:
    sets = get_test_data("set")
    set1 = tm_load_set(tm, "set1", sets["set1"].data)
    set2 = tm_load_set(tm, "set2", sets["set2"].data)
    tm_check_subset(tm, set1, set1, True, "set1-set1")
    tm_check_subset(tm, set1, set2, True, "set1-set2")
    tm_check_subset(tm, set2, set1, False, "set2-set1")

    # print(yaml.dump(alldata))


def check_subset(
    tc: TestContext, fsp: I.FiniteSetProperties, a: I.FiniteSet[X], b: I.FiniteSet[X], expect: bool
) -> None:
    res = fsp.is_subset(a, b)
    if res != expect:
        msg = zh.p(
            "fis_subset() returned",
            zh.code(str(res)),
            " instead of ",
            zh.code(str(expect)),
        )
        tc.fail(msg, a=set(a.elements()), b=set(b.elements()))


def check_save_all_elements(tc: TestContext, S: I.FiniteSet[X]) -> None:
    h = IOHelperImp()
    for a in S.elements():
        ra = S.save(h, a)
        try:
            check_good_output(tc, ra)
        except ZValueError as e:
            msg = zh.span(f"Invalid serialization", html_from_object(e))
            tc.fail(msg, element=a, representation=ra)
            continue  # raise ImplementationFail(msg, element=a, representation=ra) from e
        a2 = S.load(h, ra)
        if not S.equal(a, a2):
            msg = zh.span("Saving and reloading gives a different object")
            tc.fail(msg, element=a, representation=ra, element_reloaded=a2)

            # raise ImplementationFail(msg, element=a, representation=ra, element_reloaded=a2)
