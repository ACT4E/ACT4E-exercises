import math
import traceback
from typing import Any

import zuper_html as zh
from zuper_testint import find_imp, TestContext, TestManagerInterface, tfor

import act4e_interfaces as I
from act4e_interfaces import AllCurrencyExchangers, currency_exchange_compose, CurrencyExchanger
from act4e_interfaces.categories_representation import RichMorphism, RichObject, StringSetoid
from .data import dump_to_yaml_string, get_test_currency_categories, IOHelperImp, purify_data, TestData


@tfor(I.CurrencyOptimization)
def test_currency_optimization(tm: TestManagerInterface) -> None:
    tm.impof(I.CurrencyOptimization)
    tm.impof(I.SemiCategoryRepresentation)
    # cases = get_test_data("abstract_category")

    for name, tdata in get_test_currency_categories().items():
        # if "equational_reasoning" in tdata.requires:
        #     continue
        # logger.info(name=name, tdata=tdata)
        tm.addtest(check_currency_cat, name, tdata, tid0=f"check_currency_cat-{name}")


def check_currency_cat(tc: TestContext, name: str, tdata: TestData[I.FiniteSemiCategory_desc]) -> None:
    f: I.SemiCategoryRepresentation = find_imp(tc, I.SemiCategoryRepresentation)
    opt: I.CurrencyOptimization = find_imp(tc, I.CurrencyOptimization)
    data = purify_data(tdata.data)

    def get(p: Any) -> Any:
        return tdata.properties.get(p, {})

    the_data_s = dump_to_yaml_string(data)
    with tc.description(f"check_currency_cat {name}", name=name, data=the_data_s):
        obsetoid = StringSetoid()
        morsetoid = AllCurrencyExchangers()

        # def compose_str(_ob1: int, _ob2: int, _ob3: int, mor1: str, mor2: str) -> str:
        #     return mor1 + mor2

        sc1: I.SemiCategory[RichObject[str], RichMorphism[CurrencyExchanger]]
        helper = IOHelperImp()
        sc1 = tc.check_result(f, f.load, I.SemiCategory, helper, data, obsetoid, morsetoid, currency_exchange_compose)

        optimal_paths = get("optimal_paths")
        for testname, testdata in optimal_paths.items():
            source = testdata["source"]
            target = testdata["target"]
            amount = testdata["amount"]
            path = testdata["path"]
            result = testdata["result"]

            try:
                obtained = tc.check_result(opt, opt.compute_optimal_conversion, I.OptimalSolution, sc1, source, amount, target)
            except I.InvalidValue:
                if path is not None:
                    msg = "Expected result but no solution was found"
                    tc.fail(zh.p(msg), testdata=testdata, tb=traceback.format_exc())
                    continue
            else:
                if path is None:
                    msg = "Expected no result but the  result was provided."
                    tc.fail(zh.p(msg), testdata=testdata, result=obtained)
                    continue
                if obtained.optimal_path != path:
                    msg = "The obtained path is not the expected one."
                    tc.fail(zh.p(msg), testdata=testdata, result=obtained)
                    continue

                diff = math.fabs(obtained.final_amount - result)
                if diff > 0.001:
                    msg = "The obtained result is not the expected one."
                    tc.fail(zh.p(msg), testdata=testdata, result=obtained)
                    continue

        #
        # obsetoid = tc.check_result(sc1, sc1.objects, I.Setoid)
        # obnames2ob: Dict[str, RichObject] = {}
        # for ob in obsetoid.elements():
        #     obnames2ob[ob.label] = ob
        #

        #
        # for ob1, d in homsets.items():
        #     if ob1 not in obnames2ob:
        #         raise ZValueError(f"object {ob1} not in objects", obnames=obnames2ob)
        #
        #     contents0: Dict[str, Any]
        #     for ob2, contents0 in d.items():
        #         contents0 = dict(contents0)
        #         if ob2 not in obnames2ob:
        #             raise ZValueError(f"object {ob2} not in objects", obnames=obnames2ob)
        #
        #         if not isinstance(contents0, dict):
        #             msg = "contents must be a dict"
        #             raise ZValueError(msg, contents0=contents0)
        #
        #         # contents: List[str] = list(contents0)
        #
        #         with tc.description(f"Checking homset Hom({ob1};{ob2})", expected=contents0):
        #
        #             if "..." in contents0:
        #                 exhaustive = False
        #                 # contents.remove('...')
        #                 contents0.pop("...")
        #             else:
        #                 exhaustive = True
        #             MAX = 40
        #             hom_setoid = tc.check_result(
        #                 sc1, sc1.hom, I.EnumerableSet, obnames2ob[ob1], obnames2ob[ob2]
        #             )
        #
        #             need_to_find = set(contents0)
