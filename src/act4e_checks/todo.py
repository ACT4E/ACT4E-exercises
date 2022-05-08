from zuper_testint import TestManagerInterface, TestNotImplemented, tfor

import act4e_interfaces as I


@tfor(I.FiniteNaturalTransformationRepresentation)
def test_FiniteNaturalTransformationRepresentation(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.FiniteNaturalTransformationRepresentation)
    raise TestNotImplemented()


@tfor(I.FiniteFunctorRepresentation)
def test_FiniteFunctorRepresentation(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.FiniteFunctorRepresentation)
    raise TestNotImplemented()


@tfor(I.FiniteProfunctorRepresentation)
def test_FiniteProfunctorRepresentation(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.FiniteProfunctorRepresentation)
    raise TestNotImplemented()


@tfor(I.FiniteDPRepresentation)
def test_FiniteDPRepresentation(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.FiniteDPRepresentation)

    raise TestNotImplemented()


#
# @tfor(I.CategoryOperations)
# def test_CategoryOperations(tm: TestManagerInterface) -> None:
#     mks = tm.impof(I.CategoryOperations)
#     raise TestNotImplemented()


@tfor(I.FiniteAdjunctionsOperations)
def test_FiniteAdjunctionsOperations(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.FiniteAdjunctionsOperations)
    raise TestNotImplemented()


@tfor(I.FiniteDPOperations)
def test_FiniteDPOperations(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.FiniteDPOperations)
    raise TestNotImplemented()


@tfor(I.FiniteProfunctorOperations)
def test_FiniteProfunctorOperations(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.FiniteProfunctorOperations)
    raise TestNotImplemented()


@tfor(I.FiniteAdjunctionRepresentation)
def test_FiniteAdjunctionRepresentation(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.FiniteAdjunctionRepresentation)
    raise TestNotImplemented()
