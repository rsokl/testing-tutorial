from hypothesis import given, settings
import hypothesis.strategies as st

from pbt_tutorial import count_vowels


@settings(max_examples=1000)
@given(x=st.text(max_size=1000), include_y=st.booleans())
def test_test_fuzz_count_vowels(x: str, include_y: bool):
    count_vowels(x, include_y)
