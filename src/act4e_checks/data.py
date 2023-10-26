import traceback
from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache
from io import StringIO
from typing import Any, Dict, Generic, List, Type, TypeVar

import zuper_html as zh
from ruamel.yaml import YAML
from zuper_commons.types import add_context, ZValueError
from zuper_testint import find_imp, ImplementationFail, TestContext

import act4e_interfaces as I
from act4e_interfaces.helper import Loader, Saver
from . import logger

X = TypeVar("X")

R = TypeVar("R")


@dataclass
class TestData(Generic[X]):
    tags: Dict[str, bool]
    requires: Dict[str, bool]
    data: X
    properties: Dict[str, Any]


ALLOWED_TAGS = {
    "poset",
    "set",
    "semigroup",
    "monoid",
    "group",
    "relation",
    "map",
    "dp",
    "category",
    "natural_transform",
    "semigroup_morphism",
    "monoid_morphism",
    "group_morphism",
    "semifunctor",
    "functor",
    "semicategory",
    "abstract_category",
    "currency_category",
}

ALLOWED_PROPERTIES = {
    "powerset",
    "some_antichains",
    "some_not_antichains",
    "some_chains",
    "some_not_chains",
    "surjective",
    "defined_everywhere",
    "single_valued",
    "injective",
    "reflexive",
    "irreflexive",
    "transitive",
    "asymmetric",
    "symmetric",
    "antisymmetric",
    "has_top",
    "height",
    "width",
    "has_bottom",
    "top",
    "opposite",
    "bottom",
    "lattice",
    "some_not_uppersets",
    "some_lowersets",
    "some_uppersets",
    "some_not_lowersets",
    "some_upper_closures",
    "some_lower_closures",
    "some_maximal",
    "some_supremum",
    "some_upper_bounds",
    "some_minimal",
    "some_lower_bounds",
    "some_infimum",
    "homsets",
    "optimal_paths",
}
ALLOWED_REQUIRES = {
    "set_product",
    "poset_product",
    "set_union",
    "poset_sum",
    "equational_reasoning",
}

import os

ENV_VAR = "ACT4E_DATA"


def find_yamls(dirnames: List[str]) -> List[str]:
    res = []
    for dirname in dirnames:
        for f in os.listdir(dirname):
            if f.endswith(".yaml"):
                res.append(os.path.join(dirname, f))
    return res


def get_default_data_dir() -> str:
    dirname = os.path.join(os.path.dirname(__file__), "thedata")
    return dirname


@lru_cache()
def get_all_test_data(load: bool = True) -> Dict[str, TestData[Any]]:
    from_env = os.environ.get(ENV_VAR, None)
    if from_env:
        dirname = from_env
        logger.info(f"loading data from environment variable {ENV_VAR} = {dirname}")

    else:
        msg = f"Using embedded data. You can use the environment variable {ENV_VAR} to give a different " f"directory. "
        logger.info(msg)
        dirname = get_default_data_dir()

    dirnames = [dirname]
    yamls = find_yamls(dirnames)
    if not yamls:
        msg = "I could not find any YAML file."
        raise ZValueError(msg, dirnames=dirnames)

    res: Dict[str, TestData[Any]] = {}

    for fn in yamls:
        with open(fn) as f:
            data = f.read()

        yaml = YAML(typ="rt")
        d = yaml.load(data)
        if not isinstance(d, dict):
            msg = f"Invalid data file {fn}"
            raise ZValueError(msg)
        for k, v in d.items():
            if k in res:
                msg = f"Found duplicate key {k} in {fn}"
                raise ZValueError(msg)

            vv = dict(v)
            tags = vv.pop("tags", {})

            try:
                data = vv.pop("data")
            except KeyError:
                raise ZValueError(k=k, v=v)

            requires = vv.pop("requires", {})
            properties = vv.pop("properties", {})

            if vv:
                msg = "Unknown properties"
                raise ZValueError(msg=msg, v=v, vv=vv)

            extra_requires = set(requires) - set(ALLOWED_REQUIRES)
            if extra_requires:
                msg = f'Extra "requires" for entry {k!r}'
                raise ZValueError(msg, extra_requires=extra_requires, allowed=ALLOWED_REQUIRES)

            extra_properties = set(properties) - set(ALLOWED_PROPERTIES)
            if extra_properties:
                msg = "Extra properties"
                raise ZValueError(msg, extra_properties=extra_properties)

            extra_tags = set(tags) - set(ALLOWED_TAGS)
            if extra_tags:
                msg = "Extra tags"
                raise ZValueError(msg, extra_tags=extra_tags)

            res[k] = TestData(tags=tags, requires=requires, data=data, properties=properties)

    entries = {k: v.data for k, v in res.items()}
    if load:
        for k, v in res.items():
            with add_context(k=k):
                res[k].data = substitute(entries, res[k].data)

    return res


def substitute(entries: Dict[str, object], a: object) -> object:
    if isinstance(a, dict):
        if "load" in a:
            loadit = a["load"]
            if loadit not in entries:
                msg = "Cannot find entry to load"
                raise ZValueError(msg, a=a)
            else:
                return substitute(entries, entries[loadit])
        else:
            return {k: substitute(entries, v) for k, v in a.items()}

    elif isinstance(a, list):
        return [substitute(entries, x) for x in a]
    else:
        return a


def purify_data(a: X) -> X:
    """Strip comments etc."""
    loader = YAML()
    loader.indent(mapping=4, sequence=4, offset=2)
    loader.preserve_quotes = True
    loader.default_flow_style = False
    i = StringIO()
    loader.dump(a, i)  # ok
    s = i.getvalue()
    res = loader.load(s)
    return res


def dump_to_yaml_string(a: object) -> str:
    loader = YAML()
    loader.indent(mapping=4, sequence=4, offset=2)
    loader.preserve_quotes = True
    loader.default_flow_style = False
    i = StringIO()
    loader.dump(a, i)  # ok
    return i.getvalue()


def get_test_relations() -> Dict[str, TestData[I.FiniteRelation_desc]]:
    return get_test_data("relation")


def get_test_posets() -> Dict[str, TestData[I.FinitePoset_desc]]:
    return get_test_data("poset")


def get_test_sets() -> Dict[str, TestData[I.FiniteSet_desc]]:
    return get_test_data("set")


def get_test_maps() -> Dict[str, TestData[I.FiniteSet_desc]]:
    return get_test_data("map")


def get_test_abstract_categories() -> Dict[str, TestData[I.FiniteSemiCategory_desc]]:
    return get_test_data("abstract_category")


def get_test_currency_categories() -> Dict[str, TestData[I.FiniteSemiCategory_desc]]:
    return get_test_data("currency_category")


def get_test_data(tagname: str) -> Dict[str, TestData[Any]]:
    alldata = get_all_test_data()
    res = {}
    for k, v in alldata.items():
        if tagname in v.tags:
            res[k] = v
    return res


def get_purified_data(name: str) -> Any:
    d = get_all_test_data()
    return purify_data(d[name].data)


class IOHelperImp(I.IOHelper):
    def loadfile(self, name: str) -> Dict[str, Any]:
        raise NotImplementedError(name)


def dumpit_(tc: TestContext, fsr: Saver[X, R], h: I.IOHelper, ob: X) -> R:
    KN = type(fsr).__name__

    try:
        res = fsr.save(h, ob)
    except Exception as e:
        tc.fail(zh.span(f"{KN}:save() raised an exception"), tb=traceback.format_exc(), ob=ob)
        raise ImplementationFail() from e

    if res is None:
        tc.fail(zh.span(f"{KN}:save() returned None"), ob=ob)
        raise ImplementationFail()
    check_good_output(tc, res)
    tc.raise_if_failures()
    return res


def dump_using(tc: TestContext, K: Any, x: X) -> R:  # Type[Saver[X, R]]
    fsr = find_imp(tc, K)
    h = IOHelperImp()
    return dumpit_(tc, fsr, h, x)


def loadit_(tc: TestContext, loader: Loader[X, R], h: I.IOHelper, data: R, K: type) -> X:
    yaml = YAML(typ="rt")

    LN = type(loader).__name__
    try:
        res = loader.load(h, data)
    except NotImplementedError:
        raise
    except I.InvalidFormat as e:
        msg = f"Implementation of {LN}.load() threw InvalidFormat but the format is valid."
        tc.fail(zh.span(msg), data=dump_to_yaml_string(data), tb=traceback.format_exc())
        raise ImplementationFail() from e
    except BaseException as e:
        msg = f"Implementation of {LN}.load() threw {type(e).__name__} but the format is valid."
        tc.fail(zh.span(msg), data=dump_to_yaml_string(data), tb=traceback.format_exc())
        raise ImplementationFail() from e
    tc.expect_type2(res, K, zh.span(f"Expected that {LN}.load() returns a {K.__name__}"))
    tc.raise_if_failures()
    return res


def load_using(tc: TestContext, name: str, K: Type[Loader[X, R]], T: Type[X]) -> X:
    fsr = find_imp(tc, K)
    data1 = get_purified_data(name)
    h = IOHelperImp()
    return loadit_(tc, fsr, h, data1, T)


def check_good_output(tc: TestContext, x: object) -> None:
    OK = (int, float, bool, datetime, dict, list, str)
    if isinstance(x, tuple):
        msg = (
            "You cannot use tuples for the concrete representation because they cannot be serialized in "
            "YAML. Try using lists. (You can use tuples for the internal representation.)"
        )
        tc.fail(zh.span(msg), x=x)
        return
    # noinspection PyTypeChecker
    if not isinstance(x, OK):
        msg = (
            f"In the concrete representation you can use only one of the usable datatypes; you used "
            f"an object of type {type(x).__name__}"
        )
        tc.fail(zh.span(msg), x=x)
        return  # raise ZValueError(msg)
    if isinstance(x, list):
        for _ in x:
            check_good_output(tc, _)
    if isinstance(x, dict):
        for k, v in x.items():
            check_good_output(tc, v)


def filter_reqs(d: Dict[str, TestData[X]], req: str) -> Dict[str, TestData[X]]:
    res = {}
    for k, v in d.items():
        requires = set(v.requires)
        if requires == {req}:
            res[k] = v

    return res
