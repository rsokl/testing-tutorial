from hypothesis import given
from hypothesis import strategies as st
from hypothesis import target

# OK, what's going on here?
#
# If you run this test, it'll fail with x=1, y=-1 ... and you might wonder
# if we have some kind of comparison bug involving the sign bit.
# Uncomment the `target()` though, and you'll see a new line of output:
#
#       Highest target score: ______  (label='difference between x and y')
#
# and that large score should make it obvious that the bug is not small!


@given(st.integers(), st.integers())
def test_positive_and_negative_integers_are_equal(x, y):
    if x and y:
        # target(abs(x - y), label="difference between x and y")
        assert x == y
