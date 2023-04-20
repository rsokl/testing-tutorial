import hypothesis.extra.numpy as hnp
import hypothesis.strategies as st
import numpy as np
from hypothesis import given

from pbt_tutorial.basic_functions import merge_max_mappings, pairwise_dists


@given(
    dict1=st.dictionaries(
        keys=st.text(), values=st.integers() | st.floats(allow_nan=False)
    ),
    dict2=st.dictionaries(
        keys=st.text(), values=st.integers() | st.floats(allow_nan=False)
    ),
)
def test_merge_max_mappings_fixed_point(dict1, dict2):
    max_dict = merge_max_mappings(dict1, dict2)
    assert max_dict == merge_max_mappings(max_dict, dict2)
    assert max_dict == merge_max_mappings(dict1, max_dict)


@given(
    arr=st.lists(st.floats(allow_nan=False)),
    bounds=st.tuples(st.floats(allow_nan=False), st.floats(allow_nan=False)).map(
        sorted
    ),
)
def test_clip_fixed_point(arr, bounds):
    clipped = np.clip(arr, *bounds)
    assert np.all(clipped == np.clip(clipped, *bounds))


@given(x=st.lists(st.integers()), data=st.data())
def test_sorted_permutation_invariant(x, data):
    x_shuffled = data.draw(st.permutations(x))
    assert sorted(x) == sorted(x_shuffled)


@given(
    M=st.integers(0, 5),
    N=st.integers(0, 5),
    D=st.integers(0, 5),
    data=st.data(),
    shift=st.floats(-100, 100),
)
def test_pairwise_dists_translational_invariance(M, N, D, data, shift):
    x = data.draw(
        hnp.arrays(shape=(M, D), elements=st.floats(-1e20, 1e20), dtype=float)
    )
    y = data.draw(
        hnp.arrays(shape=(N, D), elements=st.floats(-1e20, 1e20), dtype=float)
    )
    dists = pairwise_dists(x, y)
    assert np.allclose(
        dists, pairwise_dists(x + shift, y + shift), atol=1e-3, rtol=1e-3
    )


@given(
    M=st.integers(0, 5),
    N=st.integers(0, 5),
    D=st.integers(0, 5),
    data=st.data(),
    scale=st.floats(0, 100),
)
def test_pairwise_dists_linear_scaling(M, N, D, data, scale):
    x = data.draw(
        hnp.arrays(shape=(M, D), elements=st.floats(-1e20, 1e20), dtype=float)
    )
    y = data.draw(
        hnp.arrays(shape=(N, D), elements=st.floats(-1e20, 1e20), dtype=float)
    )
    dists = pairwise_dists(x, y)
    assert np.allclose(
        scale * dists, pairwise_dists(x * scale, y * scale), atol=1e-3, rtol=1e-3
    )
