import string
from pbt_tutorial import count_vowels, merge_max_mappings

from typing import Dict

from hypothesis import given
import hypothesis.strategies as st


@given(
    in_string=st.text(alphabet=string.printable, max_size=20),
    include_y=st.booleans(),
    num_repeat=st.integers(0, max_value=100),
)
def test_count_vowels_property_based(in_string: str, include_y: bool, num_repeat: int):
    num_vowels = count_vowels(in_string, include_y)

    # Property 1:
    # `num_vowels` must be non-negative and cannot
    # exceed the length of the string itself
    assert 0 <= num_vowels <= len(in_string)

    # Property 2:
    # `N * in_string` must have N-times as many
    # vowels as `in_string`
    assert count_vowels(num_repeat * in_string, include_y) == num_repeat * num_vowels

    # Property 3:
    # The vowel count should be invariant to the string's ordering
    # Note: We can use hypothesis to shuffle our string here, but
    #       that will require use of a more advanced feature that
    #       we will learn about later.
    assert count_vowels(in_string[::-1], include_y) == num_vowels
    assert count_vowels("".join(sorted(in_string)), include_y) == num_vowels

    # Property 4:
    # Vowel count is case-insensitive
    assert count_vowels(in_string.upper(), include_y) == num_vowels
    assert count_vowels(in_string.lower(), include_y) == num_vowels


@given(
    dict1=st.dictionaries(
        keys=st.text(), values=st.integers() | st.floats(allow_nan=False)
    ),
    dict2=st.dictionaries(
        keys=st.text(), values=st.integers() | st.floats(allow_nan=False)
    ),
)
def test_merge_max_mappings_hypothesis(dict1: Dict[str, int], dict2: Dict[str, int]):
    merged_dict = merge_max_mappings(dict1, dict2)

    # Property 1:
    # Novel keys should not be introduced by the merge
    # and keys should not be lost by the merge
    assert set(merged_dict) == set(dict1).union(dict2)

    # Property 2:
    # Novel values should not be introduced by the merge
    assert set(merged_dict.values()) <= set(dict1.values()).union(dict2.values())

    # Property 3:
    # Key-value mapping pair should be preserved
    for k, v in merged_dict.items():
        assert (k, v) in dict1.items() or (k, v) in dict2.items()

    # Property 4:
    # Merged dict should only contain max values
    assert all(dict1[k] <= merged_dict[k] for k in dict1)
    assert all(dict2[k] <= merged_dict[k] for k in dict2)


# EXTRA: Test-drive development
from pbt_tutorial.basic_functions import leftpad


@given(
    in_string=st.text(max_size=20),
    width=st.integers(0, 100),
    fillchar=st.text(min_size=1, max_size=1),
)
def test_left_pad(in_string: str, width: int, fillchar: str):
    padded = leftpad(in_string, width, fillchar)
    if len(padded) <= len(in_string):
        assert width <= len(in_string)
        assert padded == in_string
    else:
        assert len(in_string) < width
        margin = width - len(in_string)
        assert set(padded[:margin]) == {fillchar}
        assert padded[margin:] == in_string
