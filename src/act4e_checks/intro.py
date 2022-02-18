import zuper_html as zh
from zuper_testint import find_imp, TestContext, tfor

import act4e_interfaces as I


@tfor(I.SimpleIntro)
def check_sum(tc: TestContext) -> None:
    si: I.SimpleIntro = find_imp(tc, I.SimpleIntro)
    a = 3
    b = 4
    tc.fail_not_equal2(a + b, si.sum(a, b), zh.span("Sum not correct"))
