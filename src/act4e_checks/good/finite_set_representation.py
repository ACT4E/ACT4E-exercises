from typing import Any

import act4e_interfaces as I
from .finite_set import MyFiniteSet

__all__ = ["MyFiniteSetRepresentation"]


class MyFiniteSetRepresentation(I.FiniteSetRepresentation):
    def load(self, h: I.IOHelper, data: I.FiniteSet_desc) -> I.FiniteSet[Any]:
        if not isinstance(data, dict):
            raise I.InvalidFormat(f"not a dictionary: {data}")
        if "elements" in data:
            elements = data["elements"]
            if not isinstance(elements, list):
                raise I.InvalidFormat()
            return MyFiniteSet(elements)
        raise I.InvalidFormat()

    def save(self, h: I.IOHelper, f: I.FiniteSet[Any]) -> I.FiniteSet_desc:
        elements = sorted(f.elements())
        data = {"elements": elements}
        return data
