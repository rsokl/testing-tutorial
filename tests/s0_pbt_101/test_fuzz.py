import hypothesis.strategies as st
from hypothesis import given, settings

from pbt_tutorial.basic_functions import count_vowels, safe_name


@settings(max_examples=1000)
@given(x=st.text(max_size=1000), include_y=st.booleans())
def test_test_fuzz_count_vowels(x: str, include_y: bool):
    count_vowels(x, include_y)


@given(
    name=st.from_type(type) | st.from_type(type).flatmap(st.from_type),
    allowed_repr=st.booleans(),
)
def test_fuzz_safe_name(name, allowed_repr):
    safe_name(name, allowed_repr)
