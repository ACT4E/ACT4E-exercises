from zuper_testint import find_imp, TestContext, tfor

import act4e_interfaces as I
from .maps import load_map_tc
from .posets_utils import load_poset_tc


@tfor(I.FiniteMonotoneMapProperties)
def check_FiniteMonotoneMapProperties(tc: TestContext) -> None:
    frc: I.FiniteMonotoneMapProperties = find_imp(tc, I.FiniteMonotoneMapProperties)

    with tc.description("Checking that we can compose relations"):
        map_bool_not = load_map_tc(tc, "map_bool_not")
        map_bool_identity = load_map_tc(tc, "map_bool_identity")
        poset_bool = load_poset_tc(tc, "poset_bool")

        with tc.description("not() is antitone"):
            tc.check_result_value(frc, frc.is_monotone, bool, False, poset_bool, poset_bool, map_bool_not)
            tc.check_result_value(frc, frc.is_antitone, bool, True, poset_bool, poset_bool, map_bool_not)

        with tc.description("identity() is monotone"):
            tc.check_result_value(frc, frc.is_monotone, bool, True, poset_bool, poset_bool, map_bool_identity)
            tc.check_result_value(
                frc, frc.is_antitone, bool, False, poset_bool, poset_bool, map_bool_identity
            )
