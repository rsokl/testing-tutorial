from typing import Dict

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
