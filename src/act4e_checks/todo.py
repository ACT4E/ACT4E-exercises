from zuper_testint import TestManagerInterface, tfor

import act4e_interfaces as I


@tfor(I.FiniteNaturalTransformationRepresentation)
def test_FiniteNaturalTransformationRepresentation(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.FiniteNaturalTransformationRepresentation)


@tfor(I.FiniteFunctorRepresentation)
def test_FiniteFunctorRepresentation(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.FiniteFunctorRepresentation)


@tfor(I.FiniteProfunctorRepresentation)
def test_FiniteProfunctorRepresentation(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.FiniteProfunctorRepresentation)


@tfor(I.FiniteDPRepresentation)
def test_FiniteDPRepresentation(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.FiniteDPRepresentation)


@tfor(I.CategoryOperations)
def test_CategoryOperations(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.CategoryOperations)


@tfor(I.FiniteAdjunctionsOperations)
def test_FiniteAdjunctionsOperations(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.FiniteAdjunctionsOperations)


@tfor(I.FiniteDPOperations)
def test_FiniteDPOperations(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.FiniteDPOperations)


@tfor(I.FiniteProfunctorOperations)
def test_FiniteProfunctorOperations(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.FiniteProfunctorOperations)


@tfor(I.SetoidOperations)
def test_SetoidOperations(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.SetoidOperations)


@tfor(I.EnumerableSetsOperations)
def test_EnumerableSetsOperations(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.EnumerableSetsOperations)


@tfor(I.FiniteAdjunctionRepresentation)
def test_FiniteAdjunctionRepresentation(tm: TestManagerInterface) -> None:
    mks = tm.impof(I.FiniteAdjunctionRepresentation)
