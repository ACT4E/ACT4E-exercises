import os
from typing import List


def get_data_dir() -> str:
    from . import __file__

    d = os.path.join(os.path.dirname(__file__), "thedata")
    return d


def list_data_files() -> List[str]:
    d = get_data_dir()
    return [f for f in os.listdir(d) if f.endswith(".yaml")]


def load_test_data_file(fn: str) -> str:
    d = get_data_dir()

    fn2 = os.path.join(d, fn)
    if not os.path.exists(fn2):
        msg = f"Cannot find filename: {fn2}"
        raise ValueError(msg)

    with open(fn2) as f:
        return f.read()
