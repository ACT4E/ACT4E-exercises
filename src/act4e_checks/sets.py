import itertools
import traceback
from functools import partial
from typing import Any, Callable, cast, Dict, Iterable, Iterator, List, Sequence, Tuple, TypeVar, Union

import zuper_html as zh
from zuper_commons.types import ZValueError
from zuper_html_plus import html_from_object
from zuper_testint import find_imp, ImplementationFail, TestContext, TestManagerInterface, TestRef, tfor

import act4e_interfaces as I
from .actual_tests import good_fsr
from .data import check_good_output, get_test_data, get_test_sets, IOHelperImp, loadit_, purify_data, TestData

E = TypeVar("E")
X = TypeVar("X")


@tfor(I.MakeSetDisjointUnion)
def test_MakeSetDisjointUnion(tm: TestManagerInterface) -> None:
    tm.addtest(check_set_disjoint_union)


@tfor(I.MakeSetDisjointUnion)
def check_set_disjoint_union(tc: TestContext) -> None:
    msd: I.MakeSetDisjointUnion = find_imp(tc, I.MakeSetDisjointUnion)
    set_empty = load_set_tc(tc, "set_empty")

    set2 = tc.check_result(msd, msd.disjoint_union, I.FiniteSetDisjointUnion, [set_empty, set_empty])
    check_same_set(tc, set2, set_empty)

    set_one: I.FiniteSet[int] = load_set_tc(tc, "set_one")
    set_two: I.FiniteSet[int] = load_set_tc(tc, "set_two")

    one_plus_two: I.FiniteSetDisjointUnion[int, Any] = tc.check_result(
        msd, msd.disjoint_union, I.FiniteSetDisjointUnion, [set_one, set_two]
    )
    elements = list(one_plus_two.elements())

    for e in elements:
        i, x = tc.check_result(one_plus_two, one_plus_two.unpack, object, e)
        e2 = tc.check_result(one_plus_two, one_plus_two.pack, object, i, x)
        check_same_element(tc, one_plus_two, e, e2)

    # either exception or in any case not allowing it
    try:
        banana = one_plus_two.pack(0, 42)
    except ValueError:
        pass
    else:
        tc.check_result_value(one_plus_two, one_plus_two.contains, bool, False, banana)

    with tc.description("Checking that bad indexes are not allowed."):
        # either exception or in any case not allowing it
        try:
            banana2 = one_plus_two.pack(-1, 42)
        except ValueError:
            pass
        else:
            tc.fail(zh.span("pack() should not allow negative index"), banana2=banana2)

        try:
            banana3 = one_plus_two.pack(3, 42)
        except ValueError:
            pass
        else:
            tc.fail(zh.span("pack() should not allow index too high"), banana3=banana3)

    with tc.description("Making sure it works for n = 0 sets."):
        zero = tc.check_result(msd, msd.disjoint_union, I.FiniteSetDisjointUnion, [])
        elements = list(zero.elements())
        tc.fail_not_equal2(0, len(elements), zh.span("Expected 0 elements"))


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


@tfor(I.FiniteSetRepresentation, level="Product")
def test_FiniteSetRepresentationProduct(tm: TestManagerInterface) -> None:
    d = get_test_data("set")
    res = {}
    for k, v in d.items():
        requires = dict(v.requires)
        requires.pop("set_product", None)
        if requires:
            continue
        res[k] = v

    doit_sets_simple(tm, res)


def check_set(tc: TestContext, m: I.FiniteSet[X]) -> None:
    n = 0
    for e in m.elements():
        n += 1
        if not m.equal(e, e):
            tc.fail(zh.span("equal is not True"), e=e)
    size = m.size()
    if n != size:
        tc.fail(zh.span("size() is not correct"), size=size, n=n)


@tfor(I.FiniteSetRepresentation)
def test_FiniteSetRepresentation(tm: TestManagerInterface) -> None:
    d = get_test_data("set")
    res = {}
    for k, v in d.items():
        requires = v.requires
        # requires.pop('set_product', None)
        if requires:
            continue
        res[k] = v

    doit_sets(tm, res)


def doit_sets(tm: TestManagerInterface, collection2: Dict[str, TestData[I.FiniteSet_desc]]) -> None:
    def dump(tc: TestContext, fmr: I.FiniteSetRepresentation, fi: I.FiniteSet[Any]) -> I.FiniteSet_desc:
        h = IOHelperImp()
        res = fmr.save(h, fi)
        check_good_output(tc, res)
        return res

    def load(tc: TestContext, fmr: I.FiniteSetRepresentation, data: I.FiniteSet_desc) -> I.FiniteSet[Any]:
        h = IOHelperImp()
        return fmr.load(h, data)

    fsr = tm.impof(I.FiniteSetRepresentation)
    for setname, info in collection2.items():
        setdata = tm.store(purify_data(info.data))
        fs = tm_load_set(tm, setname, setdata)
        good_fs = good_load_set(setname)

        t1 = tm.addtest(set_coherence, fs)
        t2 = tm.addtest(check_same_set, fs, good_fs, extra_dep=t1)
        # your FSR, your set
        b = tm.addtest(dump, fsr, fs, tid0=f"set-{setname}-dump")
        tm.addtest(load, fsr, b, tid0=f"set-{setname}-load2")
        # our FSR, your set
        b = tm.addtest(dump, good_fsr, fs, tid0=f"set-{setname}-dump")
        tm.addtest(load, good_fsr, b, tid0=f"set-{setname}-load2")
        # your FSR, our set
        b = tm.addtest(dump, fsr, good_fs, tid0=f"set-{setname}-dump")
        tm.addtest(load, fsr, b, tid0=f"set-{setname}-load2")

    def check_throws(tc: TestContext, fsr_: I.FiniteSetRepresentation, data: I.FiniteSet_desc) -> None:
        h = IOHelperImp()
        try:
            res = fsr_.load(h, data)
        except I.InvalidFormat:
            pass
        except BaseException as e:
            msg = zh.p(f"Invalid data should throw InvalidFormat, {type(e)} was thrown")
            tc.fail(msg, btr=traceback.format_exc(), data=repr(data))
        else:
            msg = zh.p(f"For invalid data you should throw InvalidFormat")
            tc.fail(msg, data=repr(data), returned=res)

    tm.addtest(check_throws, fsr, {})
    tm.addtest(check_throws, fsr, {"els": 1})
    tm.addtest(check_throws, fsr, [])
    tm.addtest(check_throws, fsr, "invalid")
    tm.addtest(check_throws, fsr, {"elements": 1})
    tm.addtest(check_throws, fsr, {"elements": {}})
    tm.addtest(check_throws, fsr, {"elements": "what ever"})


def doit_sets_simple(tm: TestManagerInterface, collection: Dict[str, TestData[I.FiniteSet_desc]]) -> None:
    def dump(tc: TestContext, fmr: I.FiniteSetRepresentation, fi: I.FiniteSet[Any]) -> I.FiniteSet_desc:
        h = IOHelperImp()
        res = fmr.save(h, fi)
        check_good_output(tc, res)
        return res

    def load(tc: TestContext, fmr: I.FiniteSetRepresentation, data: I.FiniteSet_desc) -> I.FiniteSet[Any]:
        h = IOHelperImp()
        return fmr.load(h, data)

    fsr = tm.impof(I.FiniteSetRepresentation)
    for setname, ss in collection.items():
        fs = tm_load_set(tm, setname, tm.store(purify_data(ss.data)))

        tm.addtest(set_coherence, fs)
        b = tm.addtest(dump, fsr, fs, tid0=f"set-{setname}-dump")
        tm.addtest(load, fsr, b, tid0=f"set-{setname}-load2")


def tm_load_set(
    tm: TestManagerInterface, name: str, data: TestRef[I.FiniteSet_desc]
) -> TestRef[I.FiniteSet[Any]]:
    h = IOHelperImp()

    # if 'data' in data:
    #     raise ValueError(data)
    def loadit(tc: TestContext, fsr: I.FiniteSetRepresentation, data1: I.FiniteSet_desc) -> I.FiniteSet[Any]:
        return loadit_(tc, fsr, h, data1, I.FiniteSet)

    fsr_ = tm.impof(I.FiniteSetRepresentation)
    return tm.addtest(loadit, fsr_, data, tid0=f"load-set-{name}")


@tfor(I.MakeSetUnion)
def test_MakeSetUnion(tm: TestManagerInterface) -> None:
    A = good_load_set("set1")
    B = good_load_set("set2")
    msu = tm.impof(I.MakeSetUnion)
    AuB = tm.addtest(set_union, msu, A, B)
    tm.addtest(set_coherence, AuB)
    tm_check_subset(tm, A, AuB, True, "A-union")
    tm_check_subset(tm, B, AuB, True, "B-union")


@tfor(I.MakeSetProduct)
def test_MakeSetProduct(tm: TestManagerInterface) -> None:
    A: I.FiniteSet[int] = good_make_set([1, 2])
    B: I.FiniteSet[str] = good_make_set(["a", "b"])

    AxB = tm_make_set_product(tm, A, B)

    tm.addtest(check_product, A, B, AxB)
    tm.addtest(check_save_all_elements, AxB)


def tm_make_set_product(tm: TestManagerInterface, *args: Any) -> TestRef[I.SetProduct[Any, Any]]:
    def f(tc: TestContext, imp: I.MakeSetProduct, *components: I.FiniteSet[Any]) -> I.SetProduct[Any, Any]:
        return tc.check_result(
            imp, imp.product, I.FiniteSetProduct, list(components)
        )  # return imp.product(list(components))

    i = tm.impof(I.MakeSetProduct)
    return tm.addtest(f, i, *args)


@tfor(I.MakePowerSet)
def test_MakePowerSet(tm: TestManagerInterface) -> None:
    mps = tm.impof(I.MakePowerSet)

    d = get_test_sets()

    for name, info in d.items():
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


def check_powerset(tc: TestContext, fsp: I.MakePowerSet, a: I.FiniteSet[X]) -> None:
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


@tfor(I.MakeSetIntersection)
def test_MakeSetIntersection(tm: TestManagerInterface) -> None:
    A = good_load_set("set1")
    B = good_load_set("set2")
    msi = tm.impof(I.MakeSetIntersection)
    intersection = tm.addtest(set_intersection, msi, A, B)
    tm_check_subset(tm, intersection, A, True, "A-intersection")
    tm_check_subset(tm, intersection, B, True, "B-intersection")


def tm_check_subset(
    tm: TestManagerInterface,
    a: Union[I.FiniteSet[X], TestRef[I.FiniteSet[X]]],
    b: Union[I.FiniteSet[X], TestRef[I.FiniteSet[X]]],
    expect: bool,
    tid: str,
) -> TestRef[None]:
    fsp = tm.impof(I.FiniteSetProperties)
    return tm.addtest(check_subset, fsp, a, b, expect, tid0="subset-" + tid)


def set_intersection(
    tc: TestContext, fso: I.MakeSetIntersection, a: I.FiniteSet[X], b: I.FiniteSet[X]
) -> I.FiniteSet[X]:
    return fso.intersection([a, b])  # FIXME: exceptions


def set_union(tc: TestContext, fso: I.MakeSetUnion, a: I.FiniteSet[X], b: I.FiniteSet[X]) -> I.FiniteSet[X]:
    return fso.union([a, b])  # FIXME: exceptions


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


def check_product(
    tc: TestContext, A: I.FiniteSet[X], B: I.FiniteSet[X], AxB: I.FiniteSetProduct[Any, X]
) -> None:
    n = A.size() * B.size()
    tc.fail_not_equal2(n, AxB.size(), zh.span("Wrong size"))

    tc.f_expect_equal2(partial(AxB.contains, "Banana"), lambda: False, zh.span("Banana check"))

    a = list(A.elements())[0]
    b = list(B.elements())[0]

    ab = tc.check_result(AxB, AxB.pack, object, [a, b])
    unpacked = tc.check_result(AxB, AxB.unpack, List, ab)

    if len(unpacked) != 2:
        msg = zh.span("Expected unpacked to be a list of length 2")
        tc.fail(msg, unpacked=unpacked)
        raise ImplementationFail()
    tc.fail_not_equal2(unpacked[0], a, zh.span("Projection pA not working"))
    tc.fail_not_equal2(unpacked[1], b, zh.span("Projection pB not working"))

    # pA, pB = AxB.projections()
    #
    # tc.f_expect_equal2(L(pA, ab), lambda: a, zh.span("Projection pA not working"))
    # tc.f_expect_equal2(L(pB, ab), lambda: b, zh.span("Projection pB not working"))

    tc.f_expect_equal2(
        lambda: AxB.contains(cast(Any, 1)),
        lambda: False,
        zh.span('Expected that the element "1" is not contained'),
    )
    tc.f_expect_equal2(
        lambda: AxB.contains(ab), lambda: True, zh.span("Expected that the element is not contained")
    )


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
