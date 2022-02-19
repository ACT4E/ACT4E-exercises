from zuper_testint import TestManagerInterface, TestNotImplemented, tfor

import act4e_interfaces as I


@tfor(I.MonoidalPosetOperations)
def test_MonoidalPosetOperations(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.MonoidalPosetOperations)
    raise TestNotImplemented()
