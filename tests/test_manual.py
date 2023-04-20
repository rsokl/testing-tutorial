from pbt_tutorial.basic_functions import merge_max_mappings, count_vowels


def test_count_vowels():
    # test basic strings with uppercase and lowercase letters
    assert count_vowels("aA bB yY", include_y=False) == 2
    assert count_vowels("aA bB yY", include_y=True) == 4

    # test empty strings
    assert count_vowels("", include_y=False) == 0
    assert count_vowels("", include_y=True) == 0


def test_merge_max_mappings():
    # test documented behavior
    dict1 = {"a": 1.0, "b": 2.0}
    dict2 = {"b": 20.0, "c": -1}
    expected = {"a": 1.0, "b": 20.0, "c": -1.0}
    assert merge_max_mappings(dict1, dict2) == expected

    # test empty dict1
    dict1 = {}
    dict2 = {"a": 10.2, "f": -1.0}
    expected = dict2
    assert merge_max_mappings(dict1, dict2) == expected

    # test empty dict2
    dict1 = {"a": 10.2, "f": -1.0}
    dict2 = {}
    expected = dict1
    assert merge_max_mappings(dict1, dict2) == expected

    # test both empty
    dict1 = {}
    dict2 = {}
    expected = {}
    assert merge_max_mappings(dict1, dict2) == expected
