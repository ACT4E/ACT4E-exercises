from typing import Any, Dict

import yaml
import zuper_html as zh
from zuper_commons.types import ZValueError
from zuper_testint import find_imp, TestContext, TestManagerInterface, tfor

import act4e_interfaces as I
from act4e_checks.data import get_test_abstract_categories, IOHelperImp, purify_data, TestData
from act4e_interfaces.categories_representation import IntegerSetoid, RichMorphism, RichObject, StringSetoid
from . import logger


@tfor(I.SemiCategoryRepresentation)
def test_semicat(tm: TestManagerInterface) -> None:
    tm.impof(I.SemiCategoryRepresentation)
    # cases = get_test_data("abstract_category")

    for name, tdata in get_test_abstract_categories().items():
        # if "equational_reasoning" in tdata.requires:
        #     continue
        logger.info(name=name, tdata=tdata)
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

        with tc.description("checking loading of abstract category", data=yaml.dump(data)):
            obsetoid = IntegerSetoid()
            morsetoid = StringSetoid()

            def compose_str(_ob1: int, _ob2: int, _ob3: int, mor1: str, mor2: str) -> str:
                return mor1 + mor2

            sc1: I.SemiCategory[RichObject[int], RichMorphism[str]]
            helper = IOHelperImp()
            sc1 = tc.check_result(f, f.load, I.SemiCategory, helper, data, obsetoid, morsetoid, compose_str)

            obsetoid = tc.check_result(sc1, sc1.objects, I.Setoid)
            obnames2ob: Dict[str, RichObject] = {}
            for ob in obsetoid.elements():
                obnames2ob[ob.label] = ob

            homsets = get("homsets")

            for ob1, d in homsets.items():
                if ob1 not in obnames2ob:
                    raise ZValueError(f"object {ob1} not in objects", obnames=obnames2ob)

                contents0: Dict[str, Any]
                for ob2, contents0 in d.items():
                    contents0 = dict(contents0)
                    if ob2 not in obnames2ob:
                        raise ZValueError(f"object {ob2} not in objects", obnames=obnames2ob)

                    if not isinstance(contents0, dict):
                        msg = "contents must be a dict"
                        raise ZValueError(msg, contents0=contents0)

                    # contents: List[str] = list(contents0)

                    with tc.description(f"Checking homset Hom({ob1};{ob2})", expected=contents0):

                        if "..." in contents0:
                            exhaustive = False
                            # contents.remove('...')
                            contents0.pop("...")
                        else:
                            exhaustive = True
                        MAX = 40
                        hom_setoid = tc.check_result(
                            sc1, sc1.hom, I.EnumerableSet, obnames2ob[ob1], obnames2ob[ob2]
                        )

                        need_to_find = set(contents0)
                        generated = {}
                        for i, x in enumerate(hom_setoid.elements()):
                            logger.info(ob1=ob1, ob2=ob2, i=i, x=x)
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
                                tc.fail(zh.p(msg), need_to_find=need_to_find, generated=generated)
                                break
                        if need_to_find:
                            msg = "Could not find some expected morphism"
                            tc.fail(zh.p(msg), need_to_find=need_to_find, generated=generated)
                        if exhaustive:
                            more = set(generated) - set(contents0)
                            if more:
                                msg = "Generated unexpected morphisms"
                                tc.fail(
                                    zh.p(msg), need_to_find=need_to_find, generated=generated, unexpected=more
                                )
