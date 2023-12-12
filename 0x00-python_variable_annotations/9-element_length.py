#!/usr/bin/env python3
"""use annotations for this function"""
from typing import List, Tuple, Sequence


def element_length(lst: List) -> List[Tuple[Sequence, int]]:
    """
    returns a list with a tuple and a tuple with a equence and int
    """
    return [(i, len(i)) for i in lst]
