from zuper_testint import TestManagerInterface, TestNotImplemented, tfor

import act4e_interfaces as I


@tfor(I.SetoidOperations)
def test_SetoidOperations(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.SetoidOperations)
    raise TestNotImplemented()


@tfor(I.EnumerableSetsOperations)
def test_EnumerableSetsOperations(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.EnumerableSetsOperations)
    raise TestNotImplemented()
