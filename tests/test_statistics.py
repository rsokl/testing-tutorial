from hypothesis import event, given, note
from hypothesis import strategies as st


@given(st.integers())
def test_demonstrating_note(x):
    note(f"noting {x}")
    print(f"printing {x}")
    assert x < 3


@given(st.integers().filter(lambda x: x % 2 == 0))
def test_even_integers(i):
    event(f"i mod 3 = {i%3}")
