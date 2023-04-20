import pytest

from pbt_tutorial.basic_functions import count_vowels, merge_max_mappings


@pytest.mark.parametrize("size", [0, 1, 2, 3])
def test_range_length(size):
    assert len(range(size)) == size


@pytest.mark.parametrize("a, b, c", [(1, 2, 3), (4, 5, 6), (7, 8, 9), (10, 11, 12)])
def test_inequality(a, b, c):
    assert a < b < c


@pytest.mark.parametrize(
    "input_string, include_y, expected_count",
    [("aA bB yY", False, 2), ("aA bB yY", True, 4), ("", False, 0), ("", True, 0)],
)
def test_count_vowels_parameterized(
    input_string: str, include_y: bool, expected_count: int
):
    assert count_vowels(input_string, include_y) == expected_count


@pytest.mark.parametrize(
    "dict_a, dict_b, expected_merged",
    [
        (dict(a=1, b=2), dict(b=20, c=-1), dict(a=1, b=20, c=-1)),
        (dict(), dict(b=20, c=-1), dict(b=20, c=-1)),
        (dict(a=1, b=2), dict(), dict(a=1, b=2)),
        (dict(), dict(), dict()),
    ],
)
def test_merge_max_mappings_parameterized(
    dict_a: dict, dict_b: dict, expected_merged: dict
):
    assert merge_max_mappings(dict_a, dict_b) == expected_merged
