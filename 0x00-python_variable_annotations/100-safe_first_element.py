#!/usr/bin/env python3
"""duck type annotation"""
from typing import Union, Sequence, Any, Optional


# The types of the elements of the input are not know
def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    if lst:
        return lst[0]
    else:
        return None
