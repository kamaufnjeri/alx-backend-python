#!/usr/bin/env python3
"""returns a function multiplied by multiplier"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """return function multiplied by multiplier"""
    def my_func(x: float):
        return x * multiplier
    return my_func
