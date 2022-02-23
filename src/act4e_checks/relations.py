import itertools
from dataclasses import dataclass
from typing import (
    Any,
    Callable,
    cast,
    List,
    Optional,
    Set,
    Tuple,
    TypeVar,
)

import zuper_html as zh
from zuper_testint import find_imp, TestContext, TestManagerInterface, TestRef, tfor

import act4e_interfaces as I
from .data import dumpit_, get_test_relations, IOHelperImp, loadit_, purify_data
from .sets_utils import check_same_set, make_set

A = TypeVar("A")
B = TypeVar("B")


def check_same_relation(tc: TestContext, m1: I.FiniteRelation[A, B], m2: I.FiniteRelation[A, B]) -> bool:
    m1_source = tc.check_result(m1, m1.source, I.FiniteSet)
    m2_source = tc.check_result(m2, m2.source, I.FiniteSet)
    m1_target = tc.check_result(m1, m1.target, I.FiniteSet)
    m2_target = tc.check_result(m2, m2.target, I.FiniteSet)
    check_same_set(tc, m1_source, m2_source)
    check_same_set(tc, m1_target, m2_target)
    S = m1_source
    T = m1_target
    for x, y in itertools.product(S.elements(), T.elements()):
        a = tc.check_result(m1, m1.holds, bool, x, y)  # TODO: wrap
        b = tc.check_result(m2, m2.holds, bool, x, y)  # TODO: wrap
        if a != b:
            tc.fail(zh.span("not the same relation"), x=x, y=y, a=a, b=b)
            return False
    return True


@tfor(I.FiniteRelationCompose)
def check_FiniteRelationCompose(tc: TestContext) -> None:
    frc: I.FiniteRelationCompose = find_imp(tc, I.FiniteRelationCompose)

    with tc.description("Checking that we can compose relations"):
        rel_bool_not = load_relation_tc(tc, "rel_bool_not")
        rel_bool_not_twice = tc.check_result(frc, frc.compose, I.FiniteRelation, rel_bool_not, rel_bool_not)
        rel_bool_identity = load_relation_tc(tc, "rel_bool_identity")

        check_same_relation(tc, rel_bool_not_twice, rel_bool_identity)


@tfor(I.FiniteEndorelationProperties)
def test_FiniteEndorelationProperties(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.FiniteEndorelationProperties)

    d = get_test_relations()
    for rname, rinfo in d.items():
        data = rinfo.data

        def get(p: Any) -> Any:
            return rinfo.properties.get(p, None)

        r1 = tm_load_relation(tm, rname, tm.store(purify_data(data)))
        rp = EndoRelProps(
            reflexive=get("reflexive"),
            irreflexive=get("irreflexive"),
            transitive=get("transitive"),
            symmetric=get("symmetric"),
            asymmetric=get("asymmetric"),
        )
        tm.addtest(check_endorel_props, mks, r1, rp, tid0=f"check_endorel_props-{rname}")


@tfor(I.FiniteEndorelationOperations)
def test_FiniteEndorelationOperations(tm: TestManagerInterface) -> None:
    frp = tm.impof(I.FiniteRelationRepresentation)
    feo = tm.impof(I.FiniteEndorelationOperations)

    tm.addtest(check_closure1, frp, feo)


def check_closure1(
    tc: TestContext, frp: I.FiniteRelationRepresentation, feo: I.FiniteEndorelationOperations
) -> None:
    h = IOHelperImp()
    S = [1, 2, 3]
    r1 = make_relation(S, S, {(1, 2), (2, 3)})
    R1 = frp.load(h, r1)
    r2 = make_relation(S, S, {(1, 2), (2, 3), (1, 3)})
    R2 = frp.load(h, r2)
    R3 = feo.transitive_closure(R1)
    tc.expect_type2(R3, I.FiniteRelation, zh.span("Expected a FiniteRelation"))
    check_same_relation(tc, R2, R3)


@tfor(I.FiniteRelationProperties)
def test_FiniteRelationProperties(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.FiniteRelationProperties)

    d = get_test_relations()
    for rname, rinfo in d.items():

        def get(p: Any) -> Any:
            return rinfo.properties.get(p, None)

        r1 = tm_load_relation(tm, rname, tm.store(purify_data(rinfo.data)))
        rp = RelProps(
            injective=get("injective"),
            surjective=get("surjective"),
            single_valued=get("single_valued"),
            defined_everywhere=get("defined_everywhere"),
        )
        tm.addtest(check_rel_props, mks, r1, rp, tid0=f"check_rel_props-{rname}")


@tfor(I.FiniteRelationProperties)
def check_FiniteRelationProperties_nothashable(tc: TestContext) -> None:
    frp: I.FiniteRelationProperties = find_imp(tc, I.FiniteRelationProperties)

    # TODO: implement not hashable tests
    # rp = RelProps(injective=True)


@dataclass
class RelProps:
    injective: Optional[bool]
    surjective: Optional[bool]
    single_valued: Optional[bool]
    defined_everywhere: Optional[bool]


def check_rel_props(
    tc: TestContext, frp: I.FiniteRelationProperties, s: I.FiniteRelation[Any, Any], rp: RelProps
) -> None:
    def expect(f: Callable[[I.FiniteRelation[Any, Any]], bool], a: Optional[bool], desc: str) -> None:
        if a is None:
            return
        res = f(s)
        if res not in (True, False):
            tc.fail(zh.p("Expected boolean"), f=f.__name__, res=res)
            return
        msg = zh.span(f"Checking {desc}: expect {a} obtained {res} ")
        tc.fail_not_equal2(res, a, msg=msg)

    expect(frp.is_injective, rp.injective, "injective")
    expect(frp.is_surjective, rp.surjective, "surjective")
    expect(frp.is_single_valued, rp.single_valued, "single_valued")
    expect(frp.is_defined_everywhere, rp.defined_everywhere, "defined_everywhere")


def check_rel_transpose(tc: TestContext, frp: I.FiniteRelationOperations, fr: I.FiniteRelation[A, B]) -> None:
    fr2 = frp.transpose(fr)
    if not isinstance(fr2, I.FiniteRelation):
        tc.fail(zh.p("Expected FiniteRelation"), fr2=fr2)
        return

    fr3 = frp.transpose(fr2)
    check_same_relation(tc, fr, fr3)


@dataclass
class EndoRelProps:
    reflexive: Optional[bool] = None
    irreflexive: Optional[bool] = None
    transitive: Optional[bool] = None
    symmetric: Optional[bool] = None
    antisymmetric: Optional[bool] = None
    asymmetric: Optional[bool] = None


def check_endorel_props(
    tc: TestContext, frp: I.FiniteEndorelationProperties, s: I.FiniteRelation[A, B], rp: EndoRelProps
) -> None:
    def expect(f: Callable[[Any], bool], a: Optional[bool], desc: str) -> None:
        if a is None:
            return
        res = f(s)
        if res not in (True, False):
            tc.fail(zh.p("Expected boolean"), f=f.__name__, res=res)
            return
        msg = zh.span(f"Checking {desc}")
        tc.fail_not_equal2(res, a, msg=msg, f=f.__name__)

    expect(frp.is_reflexive, rp.reflexive, "reflexive")
    expect(frp.is_irreflexive, rp.irreflexive, "irreflexive")
    expect(frp.is_transitive, rp.transitive, "transitive")
    expect(frp.is_symmetric, rp.symmetric, "symmetric")
    expect(frp.is_antisymmetric, rp.antisymmetric, "antisymmetric")
    expect(frp.is_asymmetric, rp.asymmetric, "asymmetric")


def tm_load_relation(
    tm: TestManagerInterface, name: str, data: TestRef[I.FiniteRelation_desc]
) -> TestRef[I.FiniteRelation[Any, Any]]:
    h = IOHelperImp()

    def loadit(
        c: TestContext, fsr: I.FiniteRelationRepresentation, data1: I.FiniteRelation_desc
    ) -> I.FiniteRelation[Any, Any]:
        return loadit_(c, fsr, h, data1, I.FiniteRelation)

    fsr_ = tm.impof(I.FiniteRelationRepresentation)
    return tm.addtest(loadit, fsr_, data, tid0=f"load-relation-{name}")


@tfor(I.FiniteRelationOperations)
def test_FiniteRelationOperations(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.FiniteRelationOperations)

    rels = get_test_relations()

    for name, r in rels.items():
        r1 = tm_load_relation(tm, name, tm.store(purify_data(r.data)))

        tm.addtest(check_rel_transpose, mks, r1)


X = TypeVar("X")
Y = TypeVar("Y")


def make_relation(s: List[X], t: List[Y], data: Set[Tuple[X, Y]]) -> I.FiniteRelation_desc:
    source = make_set(s)
    target = make_set(t)
    values: List[List[I.ConcreteRepr]] = list(cast(List[I.ConcreteRepr], list(_)) for _ in data)
    res: I.FiniteRelation_desc = {
        "source": source,
        "target": target,
        "values": values,
    }
    return res


def tm_save_relation(
    tm: TestManagerInterface, name: str, sgr: TestRef[I.FiniteRelation[Any, Any]]
) -> TestRef[I.FiniteRelation_desc]:
    h = IOHelperImp()

    def dumpit(
        c: TestContext, fsr: I.FiniteRelationRepresentation, sgr_: I.FiniteRelation[Any, Any]
    ) -> I.FiniteRelation_desc:
        return dumpit_(c, fsr, h, sgr_)

    fsr_ = tm.impof(I.FiniteRelationRepresentation)
    return tm.addtest(dumpit, fsr_, sgr, tid0=f"dump-relation-{name}")


@tfor(I.FiniteRelationRepresentation)
def test_FiniteRelationRepresentation(tm: TestManagerInterface) -> None:
    # mks = tm.impof(I.FiniteRelationRepresentation)
    rels = get_test_relations()

    for name, r in rels.items():
        r1 = tm_load_relation(tm, name, tm.store(purify_data(r.data)))
        r1_dumped = tm_save_relation(tm, name, r1)
        r2 = tm_load_relation(tm, name + "-re", r1_dumped)


def load_relation_tc(tc: TestContext, name: str) -> I.FiniteRelation[Any, Any]:
    fsr: I.FiniteRelationRepresentation = find_imp(tc, I.FiniteRelationRepresentation)
    data1 = get_relation_data(name)
    h = IOHelperImp()
    return loadit_(tc, fsr, h, data1, I.FiniteRelation)


def get_relation_data(name: str) -> I.FiniteRelation_desc:
    d = get_test_relations()
    data1 = purify_data(d[name].data)
    return data1
