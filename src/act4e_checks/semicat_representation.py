from typing import Any, Dict

import zuper_html as zh
from ruamel.yaml import YAML

from zuper_commons.types import ZValueError
from zuper_testint import find_imp, TestContext, TestManagerInterface, tfor

import act4e_interfaces as I
from act4e_interfaces import IntegerSetoid, RichMorphism, RichObject, StringSetoid
from . import logger
from .data import dump_to_yaml_string, get_test_abstract_categories, IOHelperImp, purify_data, TestData


@tfor(I.SemiCategoryRepresentation)
def test_semicat(tm: TestManagerInterface) -> None:
    tm.impof(I.SemiCategoryRepresentation)
    # cases = get_test_data("abstract_category")

    for name, tdata in get_test_abstract_categories().items():
        # if "equational_reasoning" in tdata.requires:
        #     continue
        # logger.info(name=name, tdata=tdata)
        tm.addtest(check_semicat_repr, name, tdata, tid0=f"test_semicat_repr-{name}")


#
# @tgroup("TestSemiCategoryRepresentationEquational")
# def test_semicat_hard(tm: TestManagerInterface) -> None:
#     tm.impof(I.SemiCategoryRepresentation)
#     # cases = get_test_data("abstract_category")
#
#     for name, tdata in get_test_abstract_categories().items():
#         if "equational_reasoning" not in tdata.requires:
#             continue
#         logger.info(name=name, tdata=tdata)
#         tm.addtest(check_semicat_repr, name, tdata, tid0=f"test_semicat_repr-{name}")


def check_semicat_repr(tc: TestContext, name: str, tdata: TestData[I.FiniteSemiCategory_desc]) -> None:
    f: I.SemiCategoryRepresentation = find_imp(tc, I.SemiCategoryRepresentation)

    with tc.description(f"checking {name}"):
        data = purify_data(tdata.data)

        def get(p: Any) -> Any:
            return tdata.properties.get(p, {})

        yaml = YAML(typ="rt")
        data_s: str = dump_to_yaml_string(data)

        with tc.description("checking loading of abstract category", data=data_s):
            obsetoid = IntegerSetoid()
            morsetoid = StringSetoid()

            def compose_str(_ob1: int, _ob2: int, _ob3: int, mor1: str, mor2: str) -> str:
                return mor1 + mor2

            sc1: I.SemiCategory[RichObject[int], RichMorphism[str]]
            helper = IOHelperImp()
            sc1 = tc.check_result(f, f.load, I.SemiCategory, helper, data, obsetoid, morsetoid, compose_str)

            obsetoid = tc.check_result(sc1, sc1.objects, I.Setoid)
            obnames2ob: Dict[str, RichObject[Any]] = {}
            for ob in obsetoid.elements():
                obnames2ob[ob.label] = ob

            homsets = get("homsets")

            for ob1, d in homsets.items():
                if ob1 not in obnames2ob:
                    raise ZValueError(f"object {ob1} not in objects", obnames=obnames2ob)

                for ob2, generations in d.items():
                    if ob2 not in obnames2ob:
                        raise ZValueError(f"object {ob2} not in objects", obnames=obnames2ob)

                    if not isinstance(generations, dict):
                        msg = "generations must be a dict"
                        raise ZValueError(msg, generations=generations)

                    gens = sorted(generations)
                    for gen in gens:
                        if not isinstance(gen, int):
                            msg = "generations must be a dict of ints"
                            raise ZValueError(msg, generations=generations)

                    tocheck: Dict[int, Any] = {}
                    for i, x in enumerate(gens):
                        expected = {}
                        for k in range(0, i):
                            expected.update(generations[k] or {})
                        expected.update(generations[x] or {})
                        tocheck[x] = expected

                    with tc.description(f"Checking homset Hom({ob1};{ob2})", tocheck_atlevels=tocheck):
                        for k, v in tocheck.items():
                            logger.info(f"Expected for generation {i}", expected=expected)
                            ok = go_check(tc, sc1, obnames2ob, ob1, ob2, v, k)
                            if not ok:
                                break


def go_check(tc: TestContext, sc1, obnames2ob, ob1, ob2, contents0: Dict[str, str], level: int) -> bool:
    contents0 = dict(contents0)

    if not isinstance(contents0, dict):  # type: ignore
        msg = "contents must be a dict"
        raise ZValueError(msg, contents0=contents0)

    # contents: List[str] = list(contents0)
    ok = True
    with tc.description(f"Checking homset Hom({ob1};{ob2}) for uptolevel = {level}", expected=contents0):
        if "..." in contents0:
            exhaustive = False
            # contents.remove('...')
            contents0.pop("...")
        else:
            exhaustive = True
        MAX = 40
        hom_setoid = tc.check_result(sc1, sc1.hom, I.EnumerableSet, obnames2ob[ob1], obnames2ob[ob2], level)

        need_to_find = set(contents0)
        generated = {}
        for i, x in enumerate(hom_setoid.elements()):
            logger.info("enumerating", ob1=ob1, ob2=ob2, i=i, x=x)
            if x.label in generated:
                msg = f"Generated double element {x.label!r}"
                tc.fail(zh.p(msg), generated=generated)
                continue

            generated[x.label] = x
            if x.label in need_to_find:
                need_to_find.remove(x.label)
            if not need_to_find:
                break

            if i > MAX:
                msg = f"Over {MAX} iterations, cannot find elements"
                tc.fail(zh.p(msg), missing=need_to_find, generated=generated)
                break

        if need_to_find:
            msg = "Could not find some expected morphism"
            tc.fail(zh.p(msg), missing=need_to_find, generated=generated)
            ok = False
        if exhaustive:
            more = set(generated) - set(contents0)
            if more:
                msg = "Generated unexpected morphisms"
                tc.fail(zh.p(msg), need_to_find=need_to_find, generated=generated, unexpected=more)
                ok = False
    return ok
