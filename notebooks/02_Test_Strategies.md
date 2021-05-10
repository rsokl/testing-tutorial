---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.5.0
  kernelspec:
    display_name: Python [conda env:testing-tutorial]
    language: python
    name: conda-env-testing-tutorial-py
---

# Common Test Tactics

In the previous section we are familiarized ourselves with Hypothesis' core strategies for describing data, along with the various methods for augmenting them and combining thing.
Now we will put these to good use and discuss some common tactics for writing effective property-based tests for our code.

<!-- #region -->
## Simple Properties to Test

### Valid Inputs Don't Crash The Code (i.e. "Fuzzing")

We already encountered fuzzing in the first section of this tutorial, but it is worth reiterating that *simply calling your code with diverse, valid inputs - to see if your code crashes - works shockingly well*.
This is especially true if your code contains internal assertions to guarantee that specific assumptions made about the code's internal logic are never violated.

Consider the following function:


```python
from typing import Any

def safe_name(obj: Any, repr_allowed: bool=True) -> str:
    """Tries to get a descriptive name for an object. Returns '<unknown>`
    instead of raising - useful for writing descriptive/safe error messages."""
    if hasattr(obj, "__qualname__"):
        return obj.__qualname__

    if hasattr(obj, "__name__"):
        return obj.__name__

    if repr_allowed and hasattr(obj, "__repr__"):
        return repr(obj)

    return "<unknown>"
```

This is a function that is meant to be used when writing error messages; we never want *it* to raise an error.
While we will want to be sure to test that this returns correct/descriptive names, we certainly want to make sure that this function never crashes.
<!-- #endregion -->

<div class="alert alert-info">

**Exercise: An object by any other name (would cause a bug)**

Add `safe_name` to `pbt_tutorial/basic_functions.py`.
Next, in `test_fuzz.py`, add a test that fuzzes `safe_name` with a diverse set of inputs.
Consider using the `st.from_type(type)` and `st.from_type(type).flatmap(st.from_type)` "recipes" for generating a wide-variety of types and values for this test. 

You can also use the `@example` decorator to add specific edge cases that you want to test against.
</div>


### Rountrip Pairs

Saving and loading, encoding and decoding, sending and receiving, to-yaml from-yaml: these are all examples of pairs of functions that form "roundtrip" relationships.

```
# f and g form a "roundtrip" (i.e. f is g's inverse)

g(f(x)) == x
``` 

The "roundtrip" property is a wonderful thing to test; such a test is simple to write, permits very flexible/complicated inputs, and tests for correctness in a meaningful way.

Note that we can often choose the direction of the roundtrip that we test; e.g. `f(g(x)) == x` vs `g(f(x)) == x`.
You might pick the roundtrip direction by considering which function of the pair - `f` of `g` - has an input that is easier to describe using Hypothesis' strategies.
 

<!-- #region -->
<div class="alert alert-info">

**Exercise: Roundtripping Run-Length Encoding**

Run-length encoding is a simple method for compressing data that contains long sequences of repeated characters.

In this compression algorithm:

1. A standalone character will be unchanged. E.g "a" $\rightarrow$ ["a"].
2. A run of a character, c, repeated N times will be compressed to ["c", "c", N]. E.g. "bbbb" $\rightarrow$ ['b', 'b', 4].
    
These two rules are all that you need to perform run-length encoding.

Let's look at a few examples of run-length-encoding:

- "abcd" $\rightarrow$ ['a', 'b', 'c', 'd']
- "abbbba" $\rightarrow$ ['a', 'b', 'b', 4, 'a']
- "aaaabbcccd" $\rightarrow$ ['a', 'a', 4, 'b', 'b', 2, 'c', 'c', 3, 'd']
- "" $\rightarrow$ []
- "1" $\rightarrow$ ["1"]

The decompression algorithm, run-length decoding, simply reverses this process:

- ['q', 'a', 'a', 4, 'b', 'b', 2, 'c', 'c', 3, 'd'] $\rightarrow$ 'qaaaabbcccd'

Here is an implementation of the encoder for this compressions scheme:
    
```python
from itertools import groupby
from typing import List, Union

def run_length_encoder(in_string: str) -> List[Union[str, int]]:
    """
    >>> run_length_encoder("aaaaabbcbc")
    ['a', 'a', 5, 'b', 'b', 2, 'c', 'b', 'c']
    """
    assert isinstance(in_string, str)
    out = []
    for item, group in groupby(in_string):
        cnt = sum(1 for x in group)
        if cnt == 1:
            out.append(item)
        else:
            out.extend((item, item, cnt))
    assert isinstance(out, list)
    assert all(isinstance(x, (str, int)) for x in out)
    return out
```
    
Add this function to the `basic_functions.py` file.
Next, begin writing the corresponding decoder
    
```python
def run_length_decoder(in_list: List[Union[str, int]]) -> str:
    """
    >>> run_length_decoder(['a', 'a', 5, 'b', 'b', 2, 'c', 'b', 'c'])
    "aaaaabbcbc"
    """
    # YOUR CODE HERE
```

But write this function using test-driven development.
Consider which direction of the roundtrip is easier to test.

Also, consider combining strategies via `st.one_of` to help ensure that your roundtrip is being exercised with a diverse set of inputs as well as a diverse set of patterns.
That is, if you you draw highly-varied string inputs to your encoder, then you might not often encounter intricate or lengthy patterns of repetition.
There is a tradeoff to be managed here.

</div>
<!-- #endregion -->

### Equivalent Functions

There are times where we are fortunate enough to have access to two distinct functions that are meant to exhibit the same behavior.
Often times this comes in the form of a slow function (e.g. single-threaded) vs a faster one (multi-threaded), or "cousin implementations" of functions (e.g. NumPy's and PyTorch's respective implementations of `matmul`).

- `f_old()` vs `f_new`
- `f_singlethread()` vs `f_multithread()`
- `func()` vs `numba.njit(func)()`
- `numpy.matmul()` vs `torch.matmul()`
- `numpy.einsum(..., optimize=False)` vs `numpy.einsum(..., optimize=True)`



<!-- #region -->
### Metamorphic Relationships

A metamorphic relationship is one in which a known transformation made to the input of a function has a *known* and *necessary* affect of the function's output.
We already saw an example of this when we tested our `count_vowels` function:

```python
assert count_vowels(n * input_string) == n * count_vowels(input_string)
```

That is, if we replicate the input-string `n` times, then the number of vowels counted in the string should be scaled by a factor of `n` as well.
Note that we had to evaluate our function twice to check its metamorphic property.
**All metamorphic tests will require multiple evaluations of the function of interest.**

Metamorphic testing is often a *highly* effective method of testing, which enables us to exercise our code and test for correctness under a wider range of inputs, without our needing to concoct a sophisticated "oracle" for validating the code's exact behavior.
Basically, these tests give you a lot of bang for your buck!

Let's consider some common metamorphic relationships that crop up in functions:

**Linearity**

```
f(a * x) = a * f(x)
```

The example involving `count_vowels` is a demonstration of a "linear" metamorphic relationship.

```
mag = abs(x)
assert a * mag == abs(a * x)
```

**Monotonicity**

```
f(x) <= f(x + |δ|)

or

f(x) >= f(x + |δ|)
```

A function is monotonic if transforming the input of th function leads an "unwavering" change - only-increasing or only-decreasing - in the function's output.
Consider, for example, a database that returns some number of results for a query;
making the query more precise *should not increase the number of results*

```
len(db.query(query_a)) >= len(db.query(query_a & query_b)) 
```

**Fixed-Point Location**

```python
y = f(x)
assert y == f(y)
```

A fixed point of a function `f` is any value `y` such that `f(y) -> y`.
It might be surprising to see just how many functions always return fixed-points of themselves:

```python
y = sort(x)
assert y == sort(y)

sanitized = sanitize_input(x)
assert sanitized == sanitize_input(sanitized)

formatted_code = black_formatter(code)
assert formatted_code == black_formatter(formatted_code)

normed_vec = l2_normalize(vec)
assert normed_vec == l2_normalize(vec)

result = find_minimum(f, starting_point=x, err_tol=delta)
assert result == find_minimum(f, starting_point=result, err_tol=delta)

padded = left_pad(string=x, width=4, fillchar="a")
assert padded == left_pad(string=padded, width=4, fillchar="a")
```

**Invariance Under Transformation**

If `T(x)` is a function such that the following holds:

```
f(x) = f(T(x))
```

This might be an invariance to scaling (`f(x) == f(a * x)`), translation (`f(x) == f(x + a)`), permutation (`f(coll) == f(shuffle(coll))`).

In the case of a computer-vision algorithm, like an image classifier, this could be an invariance under a change of brightness in the image or a horizontal flip of the image (e.g. these things shouldn't change if the model sees a cat in the image).
<!-- #endregion -->

<!-- #region -->
<div class="alert alert-info">

**Exercise: Metamorphic testing**

Create the file `tests/test_metamorphic.py`.
For each of the following functions identify one or more metamorphic relationships that are exhibited by the function and write tests that exercise them.
    
- [`numpy.clip`](https://numpy.org/doc/stable/reference/generated/numpy.clip.html)
- `sorted` (don't test the fixed-point relationship; identify a different metamorphic relationship)
- `merge_max_mappings`
- `pairwise_dists` (defined below.. add this to `basic_functions.py`)

```python
import numpy as np

def pairwise_dists(x, y):
    """ Computing pairwise Euclidean distance between the respective
    row-vectors of `x` and `y`

    Parameters
    ----------
    x : numpy.ndarray, shape=(M, D)
    y : numpy.ndarray, shape=(N, D)

    Returns
    -------
    numpy.ndarray, shape=(M, N)
        The Euclidean distance between each pair of
        rows between `x` and `y`."""
    sqr_dists = -2 * np.matmul(x, y.T)
    sqr_dists +=  np.sum(x**2, axis=1)[:, np.newaxis]
    sqr_dists += np.sum(y**2, axis=1)
    return np.sqrt(np.clip(sqr_dists, a_min=0, a_max=None))
```

</div>
<!-- #endregion -->

<!-- #region -->
<div class="alert alert-info">

**Exercise: Testing the softmax function**

The so-called "softmax" function is a means of normalizing a set of numbers such that **they will have the properties of a probability distribution**. I.e., post-softmax, each number will reside in $[0, 1]$ and the resulting numbers will sum to $1$.

The softmax of a set of $M$ numbers is:

\begin{equation}
softmax([s_{k} ]_{k=1}^{M}) = \Bigl [ \frac{e^{s_k}}{\sum_{i=1}^{M}{e^{s_i}}} \Bigr ]_{k=1}^{M}
\end{equation}

```python
>>> softmax([10., 10., 10.])
array([0.33333333, 0.33333333, 0.33333333])

>>> softmax([0., 10000., 0.])
array([0., 1., 0.])

>>> softmax([-100., 0., -100.])
array([3.72007598e-44, 1.00000000e+00, 3.72007598e-44])
```

Write an implementation of `softmax` in `basic_functions.py` and test the two properties of `softmax` that we described above.
Note: you should use `math.isclose` when checking if two floats are approximately equal.


If you implemented `softmax` in a straight-forward way (i.e. you implemented the function based on the exact equation above) then you property-based test should fail.
This is due to the use of the exponential function in `softmax`, which quickly creates a numerical instability.

We can fix the numerical instability by recognizing a metamorphic relationship that is satisfied by the softmax equation: it exhibits translational invariance:

\begin{align}
softmax([s_{k} - a]_{k=1}^{M}) &= \Bigl [ \frac{e^{s_k - a}}{\sum_{i=1}^{M}{e^{s_i - a}}} \Bigr ]_{k=1}^{M}\\
&= \Bigl [ \frac{e^{-a}e^{s_k}}{e^{-a}\sum_{i=1}^{M}{e^{s_i}}} \Bigr ]_{k=1}^{M}\\
&= \Bigl [ \frac{e^{s_k}}{\sum_{i=1}^{M}{e^{s_i}}} \Bigr ]_{k=1}^{M}\\
&= softmax([s_{k}]_{k=1}^{M})
\end{align}

Thus we can address this instability by finding the max value in our vector of number, subtracting that number from each of the values in the vector, and *then* compute the softmax.
Update your definition of `softmax` and see that your property-based tests now pass.

Reflect on the fact that using Hypothesis to drive a property-based test lead us to identify a subtle-but-critical oversight in our function.
Had we simply manually tested our function with known small inputs and outputs, we might not have discovered this issue.
    
Are there any other properties that we could test here?
Consider how to set that the respective ordering of the input and output are the same (e.g. `numpy.argsort` can get at this).
</div>
<!-- #endregion -->
