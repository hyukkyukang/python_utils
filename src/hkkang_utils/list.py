import functools
import operator
from typing import Any, List


def do_flatten_list(list_of_list: List[List[Any]])-> List[Any]:
    """Flatten a list of list to a list

    :param list_of_list: list to flatten
    :type list_of_list: List[List[Any]]
    :return: flatten list
    :rtype: List[Any]
    """
    return functools.reduce(operator.iconcat, list_of_list, [])

def map_many(functions: List, iterable:List[Any]) -> List[Any]:
    return list(functools.reduce(lambda x, y: map(y, x), functions, iterable))

def get(items: List[Any], idx: int, default: Any="") -> Any:
    if idx < 0:
        return default
    try:
        return items[idx]
    except IndexError:
        return default