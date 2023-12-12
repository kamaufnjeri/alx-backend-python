#!/usr/bin/env python3
"""function takes in string and int/float as parameters"""
from typing import Tuple, Union
import math


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """Returns a tuple"""
    return (k, math.pow(v, 2))
