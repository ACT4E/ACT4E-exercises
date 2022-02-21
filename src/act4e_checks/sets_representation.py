import traceback
from typing import Any, Dict, TypeVar

import zuper_html as zh
from zuper_testint import TestContext, TestManagerInterface, TestRef, tfor

import act4e_interfaces as I
from .actual_tests import good_fsr
from .data import check_good_output, get_test_data, IOHelperImp, loadit_, purify_data, TestData
from .sets_utils import check_same_set, good_load_set, set_coherence

E = TypeVar("E")
X = TypeVar("X")


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
        except NotImplementedError:
            raise
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
