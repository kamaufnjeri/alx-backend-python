#!/usr/bin/env python3
"""Using TypeVar"""
from typing import TypeVar, Mapping, Any, Union

T = TypeVar("T")


def safely_get_value(
    dct: Mapping, key: Any, default: Union[T, None] = None
) -> Union[T, None]:
    if key in dct:
        return dct[key]
    else:
        return default
