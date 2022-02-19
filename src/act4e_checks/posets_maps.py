from zuper_testint import TestManagerInterface, TestNotImplemented, tfor

import act4e_interfaces as I


@tfor(I.FiniteMonotoneMapProperties)
def test_FiniteMonotoneMapProperties(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.FiniteMonotoneMapProperties)
    raise TestNotImplemented()
