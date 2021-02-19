import os

from zuper_commons.fs import read_ustring_from_utf8_file
from zuper_commons.types import ZException


def get_data_file(bn: str) -> str:
    import act4e_interfaces
    p = os.path.dirname(act4e_interfaces.__file__)
    data = os.path.join(p, 'data')
    f = os.path.join(data, bn)
    if not os.path.exists(f):
        raise ZException('does not exist', f=f)
    return read_ustring_from_utf8_file(f)


def visualize_data_file(bn: str):
    s = get_data_file(bn)
    print('\\begin{minted}{yaml}')
    print(s)
    print('\\end{minted}',end='')
