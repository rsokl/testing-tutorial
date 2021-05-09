import numpy as np
from itertools import groupby
from typing import Any, Dict, List, Union

__all__ = ["count_vowels", "merge_max_mappings"]


def count_vowels(x: str, include_y: bool = False) -> int:
    """Returns the number of vowels contained in `x`.

    The vowel 'y' is included optionally.

    Parameters
    ----------
    x : str
        The input string

    include_y : bool, optional (default=False)
        If `True` count y's as vowels

    Returns
    -------
    vowel_count: int

    Examples
    --------
    >>> count_vowels("happy")
    1
    >>> count_vowels("happy", include_y=True)
    2
    """
    vowels = set("aeiouAEIOU")

    if include_y:
        vowels.update("yY")

    return sum(char in vowels for char in x)


def merge_max_mappings(
    dict1: Dict[str, float], dict2: Dict[str, float]
) -> Dict[str, float]:
    """Merges two dictionaries based on the largest value
    in a given mapping.

    The keys of the dictionaries are presumed to be floats.

    Parameters
    ----------
    dict1 : Dict[str, float]
    dict2 : Dict[str, float]

    Returns
    -------
    merged : Dict[str, float]
        The dictionary containing all of the keys common
        between `dict1` and `dict2`, retaining the largest
        value from common mappings.

    Examples
    --------
    >>> x = {"a": 1, "b": 2}
    >>> y = {"b": 100, "c": -1}
    >>> merge_max_mappings(x, y)
    {'a': 1, 'b': 100, 'c': -1}
    """
    # `dict(dict1)` makes a copy of `dict1`. We do this
    # so that updating `merged` doesn't also update `dict1`
    merged = dict(dict1)
    for key, value in dict2.items():
        if key not in merged or value > merged[key]:
            merged[key] = value
    return merged


# EXTRA: Test-drive development

# SOLUTION
def leftpad(string: str, width: int, fillchar: str) -> str:
    """Left-pads `string` with `fillchar` until the resulting string
    has length `width`.

    Parameters
    ----------
    string : str
        The input string

    width : int
        A non-negative integer specifying the minimum guaranteed
        width of the left-padded output string.

    fillchar : str
        The character (length-1 string) used to pad the string.

    Examples
    --------
    The following is the intended behaviour of this function:

    >>> leftpad('cat', width=5, fillchar="Z")
    'ZZcat'
    >>> leftpad('Dog', width=2, fillchar="Z")
    'Dog'
    """
    assert isinstance(width, int) and width >= 0, width
    assert isinstance(fillchar, str) and len(fillchar) == 1, fillchar
    margin = max(width - len(string), 0)
    return margin * fillchar + string


def safe_name(obj: Any, repr_allowed: bool=True) -> str:
    """Tries to get a descriptive name for an object. Returns '<unknown>`
    instead of raising - useful for writing descriptive/safe error messages."""
    if hasattr(obj, "__qualname__"):
        return obj.__qualname__

    if hasattr(obj, "__name__"):
        return obj.__name__

    if repr_allowed and hasattr(obj, "__repr__"):
        return repr(obj)

    return "<unknown>"


def run_length_encoder(in_string: str) -> List[Union[str, int]]:
    """
    >>> run_length_encoder("aaaaabbcbc")
    ['a', 'a', 5, 'b', 'b', 2, 'c', 'b', 'c']
    """
    assert isinstance(in_string, str)
    out = []
    for item, group in groupby(in_string):
        cnt = sum(1 for x in group)
        if cnt == 1:
            out.append(item)
        else:
            out.extend((item, item, cnt))
    assert isinstance(out, list)
    assert all(isinstance(x, (str, int)) for x in out)
    return out


# SOLUTION
def run_length_decoder(in_list: List[Union[str, int]]) -> str:
    """
    >>> run_length_decoder(['a', 'a', 5, 'b', 'b', 2, 'c', 'b', 'c'])
    "aaaaabbcbc"
    """
    out = ""
    for n, item in enumerate(in_list):
        if isinstance(item, int):
            out += in_list[n - 1] * (item - 2)
        else:
            out += item
    return out


def pairwise_dists(x, y):
    """ Computing pairwise Euclidean distance between the respective
    row-vectors of `x` and `y`

    Parameters
    ----------
    x : numpy.ndarray, shape=(M, D)
    y : numpy.ndarray, shape=(N, D)

    Returns
    -------
    numpy.ndarray, shape=(M, N)
        The Euclidean distance between each pair of
        rows between `x` and `y`."""
    sqr_dists = -2 * np.matmul(x, y.T)
    sqr_dists +=  np.sum(x**2, axis=1)[:, np.newaxis]
    sqr_dists += np.sum(y**2, axis=1)
    return np.sqrt(np.clip(sqr_dists, a_min=0, a_max=None))


def softmax(x):
    x = x - x.max()
    return np.exp(x) / np.exp(x).sum()
