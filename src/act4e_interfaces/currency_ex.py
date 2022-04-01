from abc import abstractmethod
from dataclasses import dataclass
from typing import Iterator, List, Tuple, TypedDict

from act4e_interfaces import ConcreteRepr, FiniteSemiCategory, InvalidValue, IOHelper, Setoid
from .exceptions import InvalidFormat
from .sets import FiniteSet


class CurrencyExchanger_desc(TypedDict):
    rate: float
    commission: float


class NoneSetoid(FiniteSet[None]):
    """Represents a setoid with a unique element, None,
    which is represented as None.
    """

    def contains(self, x: None) -> bool:
        return x is None

    def save(self, _: IOHelper, x: None) -> None:
        if x is not None:
            raise InvalidValue("NoneSetoid.save: x is not None")
        return None

    def load(self, _: IOHelper, o: None) -> None:
        if o is not None:
            raise InvalidFormat("NoneSetoid.load: x is not None")
        return None

    def elements(self) -> Iterator[None]:
        for x in [None]:
            yield x

    def size(self) -> int:
        return 1


def compose_none(ob1: None, ob2: None, ob3: None, t1: None, t2: None) -> None:
    assert ob1 is None, ob1
    assert ob2 is None, ob2
    assert ob3 is None, ob3
    assert t1 is None, t1
    assert t2 is None, t2
    return None


@dataclass
class CurrencyExchanger:
    rate: float
    commission: float


class AllCurrencyExchangers(Setoid[CurrencyExchanger]):
    """A setoid of CurrencyExchangers."""

    def contains(self, x: CurrencyExchanger) -> bool:
        return isinstance(x, CurrencyExchanger) and x.rate > 0 and x.commission >= 0

    def save(self, h: IOHelper, x: CurrencyExchanger) -> ConcreteRepr:
        return {"rate": x.rate, "commission": x.commission}

    def load(self, h: IOHelper, o: CurrencyExchanger_desc) -> CurrencyExchanger:
        return CurrencyExchanger(rate=o["rate"], commission=o["commission"])


@dataclass
class OptimalSolution:
    morphism_path: List[str]
    transformer: CurrencyExchanger


@dataclass
class CurrencyOptimization:
    @abstractmethod
    def compute_optimal_conversion(
        self,
        desc: FiniteSemiCategory[Tuple[str, None], Tuple[str, CurrencyExchanger]],
        source: str,
        amount: str,
        target: str,
    ) -> CurrencyExchanger:
        """Returns the optimal path for converting a certain amount from source to target."""


def compose(
    ob1: None, ob2: None, ob3: None, t1: CurrencyExchanger, t2: CurrencyExchanger
) -> CurrencyExchanger:
    # <a, d> ; <b, e> = <ad, bd+e>
    a = t1.rate
    d = t1.commission
    b = t2.rate
    e = t2.commission
    return CurrencyExchanger(rate=a * b, commission=b * d + e)
