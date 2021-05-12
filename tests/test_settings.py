import hypothesis.strategies as st
from hypothesis import event, given, note


@given(st.integers())
def test_demonstrating_note(x):
    note(f"noting {x}")
    print(f"printing {x}")
    assert x < 3
