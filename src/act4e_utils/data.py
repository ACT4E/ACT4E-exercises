import codecs
import os

__all__ = ['get_data_file', 'read_ustring_from_utf8_file']


def get_data_file(bn: str) -> str:
    import act4e_interfaces
    p = os.path.dirname(act4e_interfaces.__file__)
    data = os.path.join(p, 'data')
    f = os.path.join(data, bn)
    if not os.path.exists(f):
        raise Exception(f'does not exist {f}')
    return read_ustring_from_utf8_file(f)


def read_ustring_from_utf8_file(filename: str) -> str:
    with codecs.open(filename, encoding="utf-8") as f:
        try:
            return f.read()
        except UnicodeDecodeError as e:
            msg = f"Could not successfully decode file {filename!r}"
            raise UnicodeError(msg) from e
