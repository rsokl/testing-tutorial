import json
from hypothesis import Phase, given, settings, strategies as st


# Running
#       pytest --hypothesis-show-statisticstest_settings.py
#
# will report lines which were always and only run by failing examples.
# How useful is the report in this case?  Would it be useful on your
# code?  Does it report the same lines if you re-run the tests?


@settings(phases=tuple(Phase))  # Activates the `explain` phase!
@given(
    allow_nan=st.booleans(),
    obj=st.recursive(
        st.none() | st.booleans() | st.floats() | st.text(),
        extend=lambda x: st.lists(x) | st.dictionaries(st.text(), x),
    ),
)
def test_roundtrip_dumps_loads(allow_nan, obj):
    encoded = json.dumps(obj=obj, allow_nan=allow_nan)
    decoded = json.loads(s=encoded)
    assert obj == decoded
