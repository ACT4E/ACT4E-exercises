from functools import partial
from typing import Any, cast, List, TypeVar

import zuper_html as zh
from zuper_testint import ImplementationFail, TestContext, TestManagerInterface, TestRef, tfor

import act4e_interfaces as I
from .sets import check_save_all_elements
from .sets_utils import good_make_set

E = TypeVar("E")
X = TypeVar("X")


@tfor(I.FiniteMakeSetProduct)
def test_FiniteMakeSetProduct(tm: TestManagerInterface) -> None:
    A: I.FiniteSet[int] = good_make_set([1, 2])
    B: I.FiniteSet[str] = good_make_set(["a", "b"])

    AxB = tm_make_set_product(tm, A, B)

    tm.addtest(check_product, A, B, AxB)
    tm.addtest(check_save_all_elements, AxB)


def tm_make_set_product(tm: TestManagerInterface, *args: Any) -> TestRef[I.SetProduct[Any, Any]]:
    def f(
        tc: TestContext, imp: I.FiniteMakeSetProduct, *components: I.FiniteSet[Any]
    ) -> I.SetProduct[Any, Any]:
        return tc.check_result(
            imp, imp.product, I.FiniteSetProduct, list(components)
        )  # return imp.product(list(components))

    i = tm.impof(I.FiniteMakeSetProduct)
    return tm.addtest(f, i, *args)


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
