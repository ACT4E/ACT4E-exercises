from typing import (
    Any,
    Callable,
    cast,
    Dict,
    TypeVar,
)

import zuper_html as zh
from zuper_testint import (
    find_imp,
    ImplementationFail,
    TestContext,
    TestManagerInterface,
    TestNotImplemented,
    TestRef,
    tfor,
)

import act4e_interfaces as I
from .data import check_good_output, get_test_data, get_test_maps, IOHelperImp, loadit_, purify_data, TestData
from .relations import check_same_relation, load_relation_tc
from .sets_utils import check_same_element, check_same_set, load_set_tc, set_coherence

E = TypeVar("E")
A = TypeVar("A")
B = TypeVar("B")


@tfor(I.FiniteMapOperations)
def test_FiniteMapOperations_bool(tc: TestContext) -> None:
    fmo: I.FiniteMapOperations = find_imp(tc, I.FiniteMapOperations)

    with tc.description("Checking that we can create identities."):
        # Load the Bool set
        set_bool: I.FiniteSet[Any] = load_set_tc(tc, "set_bool")
        # Load the identity
        map_bool_identity_expected = load_map_tc(tc, "map_bool_identity")
        # Ask to create the identity
        map_bool_identity = cast(I.FiniteMap[Any, Any], tc.check_result(fmo, fmo.identity, I.FiniteMap, set_bool))
        check_map(tc, map_bool_identity)
        check_same_map(tc, map_bool_identity, map_bool_identity_expected)

    with tc.description("Checking that we can compose maps"):
        map_bool_not = load_map_tc(tc, "map_bool_not")
        map_bool_not_twice = tc.check_result(fmo, fmo.compose, I.FiniteMap, map_bool_not, map_bool_not)
        check_map(tc, map_bool_not_twice)

        check_same_map(tc, map_bool_not_twice, map_bool_identity_expected)


@tfor(I.FiniteRelationOperations)
def test_FiniteRelationOperations_bool(tc: TestContext) -> None:
    fmo: I.FiniteRelationOperations = find_imp(tc, I.FiniteRelationOperations)
    with tc.description("Checking conversion of map to rel"):
        map_bool_not = load_map_tc(tc, "map_bool_not")
        rel_bool_not_expected = load_relation_tc(tc, "rel_bool_not")
        rel_bool_not = tc.check_result(fmo, fmo.as_relation, I.FiniteRelation, map_bool_not)
        check_same_relation(tc, rel_bool_not_expected, rel_bool_not)


@tfor(I.FiniteMapOperations)
def test_FiniteMapOperations(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.FiniteMapOperations)

    raise TestNotImplemented()


def check_map(tc: TestContext, m: I.FiniteMap[Any, Any]) -> None:
    source = tc.check_result(m, m.source, I.FiniteSet)
    target = tc.check_result(m, m.target, I.FiniteSet)
    set_coherence(tc, source)
    set_coherence(tc, target)
    for a in source.elements():
        b = m.__call__(a)  # TODO: check it does not fail
        if not target.contains(b):
            tc.fail(zh.span("invalid result"), x=a, y=b)


def check_same_map(tc: TestContext, m1: I.FiniteMap[A, B], m2: I.FiniteMap[A, B]) -> None:
    m1_target = tc.check_call(m1.target, I.FiniteSet)
    m2_target = tc.check_call(m2.target, I.FiniteSet)
    m1_source = tc.check_call(m1.source, I.FiniteSet)
    m2_source = tc.check_call(m2.source, I.FiniteSet)

    check_same_set(tc, m1_source, m2_source)
    check_same_set(tc, m1_target, m2_target)
    for a in m1_source.elements():  # XXX: not wrapped
        # noinspection PyTypeChecker
        y1 = tc.check_call(m1, object, a)
        # noinspection PyTypeChecker
        y2 = tc.check_call(m2, object, a)

        equal = tc.check_call(m1_target.equal, bool, y1, y2)

        if not equal:
            tc.fail(zh.span("Maps have different results"), x=a, y1=y1, y2=y2)


def check_same_function(tc: TestContext, m1: I.FiniteMap[A, B], m2: I.FiniteMap[A, B]) -> None:
    check_same_set(tc, m1.source(), m2.source())
    check_same_set(tc, m1.target(), m2.target())
    S = m1.source()
    T = m1.target()
    for x1 in S.elements():
        y1 = m1.__call__(x1)
        y2 = m2.__call__(x1)
        check_same_element(tc, T, y1, y2)


@tfor(I.FiniteMapRepresentation)
def test_FiniteMapRepresentation(tm: TestManagerInterface) -> None:
    maps = get_test_data("map")

    doit_maps(tm, maps)


@tfor(I.FiniteMapRepresentation, level="Product")
def test_FiniteMapRepresentationProduct(tm: TestManagerInterface) -> None:
    d = get_test_data("map")
    res = {}
    for k, v in d.items():
        requires = dict(v.requires)
        requires.pop("set_product", None)
        if requires:
            continue
        res[k] = v
    doit_maps(tm, res)


def check_map_involutive(tc: TestContext, fs: I.FiniteSet[A], m: Callable[[A], A]) -> None:
    for e in fs.elements():
        e_inv = m(e)
        e2 = m(e_inv)
        equal = fs.equal(e, e2)
        if not equal:
            msg = zh.span("Not involutive")
            tc.fail(msg=msg, e=e, e_inv=e_inv, e2=e2)


def doit_maps(tm: TestManagerInterface, collection: Dict[str, TestData[I.FiniteMap_desc]]) -> None:
    def dump(tc: TestContext, fmr: I.FiniteMapRepresentation, fi: I.FiniteMap[A, B], keys: Dict[str, Any]) -> I.FiniteMap_desc:
        h = IOHelperImp()
        try:
            res = fmr.save(h, fi)
        except BaseException as e:
            msg = "Cannot save the object"
            raise ImplementationFail(msg, fi=fi, **keys) from e
        check_good_output(tc, res)
        return res

    def load(tc: TestContext, fmr: I.FiniteMapRepresentation, data: I.FiniteMap_desc, keys: Dict[str, Any]) -> I.FiniteMap[A, B]:
        h = IOHelperImp()
        try:
            return fmr.load(h, data)
        except I.InvalidFormat as e:
            msg = "The implementation could not read back the data that it wrote."
            raise ImplementationFail(msg, writtendata=data, **keys) from e

    _ = tm.impof(I.FiniteMapRepresentation)
    for mapname, md in collection.items():
        mapdata = tm.store(purify_data(md.data))
        m: TestRef[I.FiniteMap[Any, Any]] = tm_load_map(tm, mapname, mapdata)
        b = tm.addtest(dump, _, m, dict(mapname=mapname, orig_data=mapdata), tid0=f"map-{mapname}-dump")
        m2 = tm.addtest(load, _, b, dict(mapname=mapname, orig_data=mapdata), tid0=f"map-{mapname}-load2")

        tm.addtest(check_map, m)
        tm.addtest(check_map, m2)
        tm.addtest(check_same_map, m, m2)


def tm_load_map(tm: TestManagerInterface, name: str, data: TestRef[I.FiniteMap_desc]) -> TestRef[I.FiniteMap[Any, Any]]:
    h = IOHelperImp()

    def loadit(tc: TestContext, fsr: I.FiniteMapRepresentation, data1: I.FiniteMap_desc) -> I.FiniteMap[A, B]:
        return loadit_(tc, fsr, h, data1, I.FiniteMap)

    _ = tm.impof(I.FiniteMapRepresentation)

    return tm.addtest(loadit, _, data, tid0=f"load-map-{name}")


def load_map_tc(tc: TestContext, name: str) -> I.FiniteMap[Any, Any]:
    fsr: I.FiniteMapRepresentation = find_imp(tc, I.FiniteMapRepresentation)
    data1 = get_map_data(name)
    h = IOHelperImp()
    return loadit_(tc, fsr, h, data1, I.FiniteMap)


def get_map_data(name: str) -> I.FiniteSet_desc:
    d = get_test_maps()
    data1 = purify_data(d[name].data)
    return data1
