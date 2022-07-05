from abc import abstractmethod
from dataclasses import dataclass
from typing import Iterator, List, TypedDict

from .categories import SemiCategory
from .categories_representation import (
    RichMorphism,
    RichObject,
)
from .exceptions import InvalidFormat, InvalidValue
from .helper import IOHelper
from .sets import FiniteSet, Setoid
from .types import ConcreteRepr

__all__ = [
    "AllCurrencyExchangers",
    "CurrencyExchanger",
    "currency_exchange_compose",
    "OptimalSolution",
    "CurrencyOptimization",
]


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
    def contains(self, x: CurrencyExchanger) -> bool:
        return isinstance(x, CurrencyExchanger) and x.rate > 0 and x.commission >= 0

    def save(self, h: IOHelper, x: CurrencyExchanger) -> ConcreteRepr:
        return dict(rate=x.rate, commission=x.commission)

    def load(self, h: IOHelper, o: CurrencyExchanger_desc) -> CurrencyExchanger:
        return CurrencyExchanger(o["rate"], o["commission"])


def currency_exchange_compose(
    _ob1: None, _ob2: None, _ob3: None, t1: CurrencyExchanger, t2: CurrencyExchanger
) -> CurrencyExchanger:
    rate = t1.rate * t2.rate
    commission = t1.commission * t2.rate + t2.commission
    return CurrencyExchanger(rate, commission)


@dataclass
class OptimalSolution:
    optimal_path: List[str]
    final_amount: float


class CurrencyOptimization:
    @abstractmethod
    def compute_optimal_conversion(
        self,
        available: SemiCategory[RichObject[str], RichMorphism[CurrencyExchanger]],
        source: str,
        amount: float,
        target: str,
    ) -> OptimalSolution:
        """Returns the optimal path for converting a certain amount from source to target.
        Raises InvalidValue if there is no path."""
