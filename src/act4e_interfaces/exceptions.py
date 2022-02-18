__all__ = [
    "InvalidFormat",
    "InvalidValue",
]


class InvalidFormat(Exception):
    """Raise this if the input data to parse is invalid."""


class InvalidValue(ValueError):
    """Raise this if the input does not make sense."""
