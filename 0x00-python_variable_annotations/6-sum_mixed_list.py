#!/usr/bin/env python3
"""list with mixed integers and floats"""
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[float, int]]) -> float:
    """sum of values of mixed lists"""
    return sum(mxd_lst)
