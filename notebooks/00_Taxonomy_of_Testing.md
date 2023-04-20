---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.5
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

# Traversing the Taxonomy of Testing

In this section we will take a tour through the taxonomy of testing: encountering manual tests, parameterized tests, and property-based tests.
In the meanwhile, we will be introduced to the testing library Hypothesis, which provides us with automated test-case generation and reduction.


## Getting Started

We expect your to write your to write pytest-style tests, which is exemplified by `test_count_vowels`, which can be found below at the beginning of the Manual Tests section.
All this entails is defining a function that has the word "test" in its name, and place it in a Python script that has the word test in *its* name, in order for pytest to find-and-run that test function.

You can run these tests from the terminal with:

```shell
pytest tests
```

presuming that you place your test scripts in the `tests/` directory.

You can also configure IDEs to "look for" pytest-style tests and make individual tests and files easy to run from the IDE.
The following links point to detailed instructions for configuring pytest with PyCharm and VSCode, respectively:

- [Running tests in PyCharm](https://www.jetbrains.com/help/pycharm/pytest.html)
- [Running tests in VSCode](https://code.visualstudio.com/docs/python/testing)


<!-- #region -->
## Manual Tests

A manual test will use inputs and corresponding outputs to a function that we have constructed "by hand", and simply assert that `func(hand_crafted_input) == expected_output`.
This is the most rudimentary form of testing that one will encounter in software testing.
For example, the following is a manual test of `pbt_tutorial.count_vowels`:

```python
from pbt_tutorial.basic_functions import count_vowels

def test_count_vowels():
    # test basic strings with uppercase and lowercase letters
    assert count_vowels("aA bB yY", include_y=False) == 2
    assert count_vowels("aA bB yY", include_y=True) == 4
```


<!-- #endregion -->

<!-- #region -->
<div class="alert alert-info">

**Exercise: Writing Manual Tests**

The following tests should be placed in `tests/s0_pbt_101/test_manual.py`.

Let's write some manual tests for `count_vowels`  and `merge_max_mappings`, both of which are defined in `src/pbt_tutorial/basic_functions.py`.
For each function:
   - Write a single test that includes multiple assertions, akin to `test_count_vowels` shown above.
   - In a comment or docstring associated with the test, document what sorts of behaviors and edge cases that you have covered with the test.
      - An example of an edge case might be: providing empty sequences/containers as inputs to your function

(Are you finding this to be tedious? Good!)

 
</div>

<!-- #endregion -->

<!-- #region -->
## Parameterized Tests

Looking back to both `test_count_vowels_basic` and `test_merge_max_mappings`, we see that there is a lot of redundancy within the bodies of these test functions.
The assertions that we make within a given test-function share identical forms - they differ only in the parameters that we feed into our functions and their expected output.
Another shortcoming of this test-structure is that a failing assertion will block subsequent assertions from being evaluated.
That is, if the second assertion in `test_count_vowels_basic` fails, the third and fourth assertions will not be evaluated in that run.
This precludes us from potentially seeing useful patterns among the failing assertions.

pytest provides a useful tool that will allow us to eliminate these structural shortcomings by transforming our test-functions into so-called _parameterized tests_. Let's parametrize the following test:

```python
# a simple test with redundant assertions

def test_range_length_unparameterized():
    assert len(range(0)) == 0
    assert len(range(1)) == 1
    assert len(range(2)) == 2
    assert len(range(3)) == 3
```

This test is checking the property `len(range(n)) == n`, where `n` is any non-negative integer.
Thus, the parameter to be varied here is the "size" of the range-object being created.
Let's treat it as such by using pytest to write a parameterized test:

```python
# parameterizing a test
import pytest

# note that this test must be run by pytest to work properly
@pytest.mark.parametrize("size", [0, 1, 2, 3])
def test_range_length(size):
    assert len(range(size)) == size
```


Make note that a pytest-parameterized test must be run using pytest; an error will raise if we manually call `test_range_length()` from within a Python REPL.
When executed, pytest will treat this parameterized test as _four separate tests_ - one for each parameter value:

```
test_basic_functions.py::test_range_length[0] PASSED                     [ 25%]
test_basic_functions.py::test_range_length[1] PASSED                     [ 50%]
test_basic_functions.py::test_range_length[2] PASSED                     [ 75%]
test_basic_functions.py::test_range_length[3] PASSED                     [100%]
```

See that we have successfully eliminated the redundancy from `test_range_length`;
the body of the function now contains only a single assertion, making obvious the property that is being tested.
Furthermore, the four assertions are now being run independently from one another and thus we can potentially see patterns across multiple fail cases in concert.
<!-- #endregion -->

<!-- #region -->
#### Parameterization Syntax

The general form for creating a parameterizing decorator with *a single parameter*, as we formed above, is:

```python
@pytest.mark.parametrize("<param-name>", [<val-1>, <val-2>, ...])
def test_function(<param-name>):
    ...
```

We will often have tests that require multiple parameters.
The general form for creating the parameterization decorator for $N$ parameters,
each of which assume $J$ values, is:

```python
@pytest.mark.parametrize("<param-name1>, <param-name2>, [...], <param-nameN>", 
                         [(<param1-val1>, <param2-val1>, [...], <paramN-val1>),
                          (<param1-val2>, <param2-val2>, [...], <paramN-val2>),
                          ...
                          (<param1-valJ>, <param2-valJ>, [...], <paramN-valJ>),
                         ])
def test_function(<param-name1>, <param-name2>, [...], <param-nameN>):
    ...
```

For example, let's take the following trivial test:

```python
def test_inequality_unparameterized():
    assert 1 < 2 < 3
    assert 4 < 5 < 6
    assert 7 < 8 < 9
    assert 10 < 11 < 12
```

and rewrite it in parameterized form. 
The decorator will have three distinct parameters, and each parameter, let's simply call them `a`, `b`, and `c`, will take on four values.

```python
# the parameterized form of `test_inequality_unparameterized`
@pytest.mark.parametrize("a, b, c", [(1, 2, 3), (4, 5, 6), (7, 8, 9), (10, 11, 12)])
def test_inequality(a, b, c):
    assert a < b < c
```
<!-- #endregion -->

<div class="alert alert-info">

**Exercise: Running a Parameterized Test**

Create the file `tests/test_parameterized.py`.
Add the parameterized tests `test_range_length` and `test_inequality`, which are defined above,
and run them.
</div>



<div class="alert alert-info">

**Exercise: Writing Parameterized Tests**

Rewrite `test_count_vowels_basic` as a parameterized test with the parameters: `input_string`, `include_y`, and `expected_count`.

Rewrite `test_merge_max_mappings` as a parameterized test with the parameters: `dict_a`, `dict_b`, and `expected_merged`.

Before rerunning the tests in `test_basic_functions.py` predict how many distinct test cases will be reported by pytest. 
</div>



<div class="alert alert-warning"> 

**Note**

The formatting for multi-parameter tests can quickly become unwieldy.
It isn't always obvious where one should introduce line breaks and indentations to improve readability.
This is a place where the ["black" auto-formatter](https://black.readthedocs.io/en/stable/) really shines!
Black will make all of these formatting decisions for us - we can write our parameterized tests as haphazardly as we like and simply run black to format our code. This is also a huge help with writing tests with Hypothesis, as you will see
</div>


<!-- #region -->
## Interlude: A Brief Intro to Hypothesis

It is often the case that the process of *describing our data* is by far the heaviest burden that we must bear when writing tests. This process of assessing "what variety of values should I test?", "have I thought of all the important edge-cases?", and "how much is 'enough'?" will crop up with nearly every test that we write.
Indeed, these are questions that you may have been asking yourself when writing `test_count_vowels_basic` and `test_merge_max_mappings` in the previous sections of this module.

[Hypothesis](https://hypothesis.readthedocs.io/) is a powerful Python library that empowers us to write a _description_ (specification, to be more precise) of the data that we want to use to exercise our test.
It will then *generate* test cases that satisfy this description and will run our test on these cases.
Let's witness this in its most basic form.

The following is the basic anatomy of a Hypothesis test:

```python
from hypothesis import given
import hypothesis.strategies as st

@given(x=st.integers())
def a_test_using_hypothesis(x):
    # x will be any integer
    # use `x` to test your function
    ...
```

The `@given` decorator is to be fed one or more *Hypothesis strategies* for describing data.
In this example, we specified a single strategy, which describes arbitrary integer values.
Executing `a_test_using_hypothesis()` will prompt Hypothesis to run the test's body _multiple times_ (100 times, by default); for run draws a new set of values from the strategies that we provided to `@given`.

Let's write a simple example to help us see this behavior clearly:

```python
saves_numbers = []

@given(x=st.integers())
def a_test_using_hypothesis(x):
    saves_numbers.append(x)
```

Now, we execute the function and inspect the contents of the list `saves_numbers`, which gets mutated (appended to) each time the body of the function is run

```python
# unlike a pytest-parameterized test, tests using hypothesis
# can be run outside of the pytest framework
>>> a_test_using_hypothesis()  # tells hypothesis to run the test body 100 times
>>> len(saves_numbers)
100

# Note that statistics will vary from run-to-run
>>> min(saves_numbers)
-147572478458337740506626060645758832445
>>> max(saves_numbers)
117191644382309356634160262916607663738
>>> sorted(saves_numbers)[50]  # median
50
```

There is a [whole suite of strategies](https://hypothesis.readthedocs.io/en/latest/data.html) available for describing various sorts of data with Hypothesis.
We will dive into the process of describing data in rich ways using these in the next section.
Prior to doing so, we will use our nascent understanding of Hypothesis to round out the taxonomy of tests, and study fuzz tests and property-based tests.
<!-- #endregion -->

### Hypothesis Performs Automated Test-Case Reduction

Before proceeding, there is an important feature that Hypothesis offers and that we should come to appreciate.
Try running the following test:

```python
from hypothesis import given 
import hypothesis.strategies as st

# using `given` with multiple parameters
# `x` is an integer drawn from [0, 10]
# `y` is an integer drawn from [20, 30]
@given(x=st.integers(0, 10), y=st.integers(20, 30))
def test_demonstrating_the_given_decorator(x, y):
    assert 0 <= x <= 10
    
    # `y` can be any value in [20, 30]
    # this is a bad assertion: it should fail!
    assert 20 <= y <= 25
```

```python
test_demonstrating_the_given_decorator()
```

Hypothesis should report:

```
Falsifying example: test_demonstrating_the_given_decorator(
    x=0, y=26,
)
```

It may seem lucky that it reported the smallest value for `y` that violates the bad inequality, but it is not luck at all!
This is a feature of Hypothesis known as **automated test-case reduction**.
That is, `given` decorator strives to report the "simplest" set of input values that produce a given error.
It does this through the process of **shrinking**.

Each of Hypothesis' strategies has its own prescribed shrinking behavior. For the integers strategy, this means identifying the integer closest to 0 that produces the error at hand.

When running the above test, Hypothesis could have encountered the following sequence of examples during its shrinking phase:

```
x=0   y=20 - PASSED
x=0   y=20 - PASSED
x=0   y=20 - PASSED
x=9   y=20 - PASSED
x=9   y=21 - PASSED
x=3   y=20 - PASSED
x=3   y=20 - PASSED
x=9   y=26 - FAILED
x=3   y=26 - FAILED
x=6   y=26 - FAILED
x=10  y=27 - FAILED
x=7   y=27 - FAILED
x=3   y=30 - FAILED
x=3   y=23 - PASSED
x=10  y=30 - FAILED
x=3   y=27 - FAILED
x=3   y=27 - FAILED
x=2   y=27 - FAILED
x=0   y=27 - FAILED
x=0   y=26 - FAILED
x=0   y=21 - PASSED
x=0   y=25 - PASSED
x=0   y=22 - PASSED
x=0   y=23 - PASSED
x=0   y=24 - PASSED
x=0   y=26 - FAILED
```

See that Hypothesis has to do a semi-random search to identify the boundaries of the fail case; it doesn't know if `x` is causing the error, or if `y` is the culprit, or if it is specific combinations of x and y that causes the failure!
Despite this complexity, the pairs of variables are successfully shrunk to the simplest fail case.


### Hypothesis will Save Falsifying Examples:

Albeit an advanced detail, it is important to note that Hypothesis does not have to search for falsifying examples from scratch every time we run a test function. Instead, Hypothesis will save a database of falsifying examples associated with each of your project's test functions. The database is saved under .hypothesis in whatever directory your test functions were run from.

This ensures that, once Hypothesis finds a falsifying example for a test, the falsifying example will be passed to your test function each time you run it, until it no longer raises an error in your code (e.g. you update your code to fix the bug that was causing the test failure).


<div class="alert alert-info">

**Exercise: Understanding How Hypothesis Works**

Create the file `tests/test_with_hypothesis.py`.

Copy the `test_demonstrating_the_given_decorator` function from above - complete with the failing assertion - and add a print statement to the body of the function, which prints out the value for `x` and `y`.

Run the test once and make note of the output that is printed. Consider copying and pasting the output to a notepad for reference. Next, rerun the test multiple times and make careful note of the printed output. What do you see? Is the output different from the first run? Does it differ between subsequent runs? Try to explain this behavior.

In your file browser, navigate to the directory from which you are running this test; if you are following along in a Jupyter notebook, this is simply the directory containing said notebook. You should see a `.hypothesis` directory. As noted above, this is the database that contains the falsifying examples that Hypothesis has identified. Delete the `.hypothesis` directory and try re-running your test? What do you notice about the output now? You should also see that the `.hypothesis` directory has reappeared. Explain what is going on here.
</div>






<div class="alert alert-info">

**Exercise: Fixing the Failing Test**

Update the body of test_demonstrating_the_given_decorator so that it no longer fails. Run the fixed test function. How many times is the test function actually be executed when you run it?
</div>





<!-- #region -->
**Now back to studying different styles of testing!** 

## Fuzz Testing

Fuzz testing is a simple, but often (embarrassingly) powerful approach to automated testing in which we feed a function a wide variety of randomly-generated inputs to see if it ever crashes.
For example, the following test "fuzzes" the `int` type with finite float inputs, to see if `int(<finite-float>)` ever causes a crash.

```python
@given(x=st.floats(allow_infinity=False, allow_nan=False))
def test_fuzz_in_with_finite_floats(x):
    int(x)  # no asserts needed!
```

while this test doesn't do much to assure us that `int` casts floats *correctly*, it is nonetheless a very simple and expressive test that gives us confidence that feeding a finite float will never cause `int` to crash.
We should appreciate just how trivial it is to write this test.

Fuzzing can be especially useful if we have our source code with internal internal `assert` statements.
Seeing that these assertions hold true even when our function is being fed truly bizarre and exotic (but valid!) input data helps close the aperture on where future bugs are coming from – we can at least be confident that they aren't coming from incorrect assertions.

([Seriously! Fuzzing can be very effective](https://github.com/google/oss-fuzz))
<!-- #endregion -->

<div class="alert alert-info">

**Exercise: Running a Parameterized Test**

Create the file `tests/test_fuzz.py`.
Use the Hypothesis strategies [text()](https://hypothesis.readthedocs.io/en/latest/data.html#hypothesis.strategies.text) and [booleans()](https://hypothesis.readthedocs.io/en/latest/data.html#hypothesis.strategies.booleans) to fuzz the `count_vowels` function.
    
Consider temporarily adding a print statement to your test to get a peek at the sort of data that you are fuzzing your function with.
    
The more inputs you feed a function in a fuzz test, the better. Take a glance at the documentation for [Hypothesis' settings](https://hypothesis.readthedocs.io/en/latest/settings.html) and increase the number of examples run in your fuzz test from 100 to 1,000.
</div>






Fuzzing is convenient and powerful because it enables us to run diverse inputs into our function without requiring us to figure out what the respective outputs of our function should be.
That being said, testing that your function simply doesn't crash doesn't tell us much about whether or not the function is actually doing its job.
We'll see that property-based testing can help us test the correctness of our code while maintaining much of the simplicity and verbosity of a fuzz-style test.


## Property-Based Tests

Property-based testing (PBT) also enables us to exercise our function with a diverse set of inputs and without knowing precisely what the corresponding outputs should be. But, unlike with fuzz testing, these tests will check that our code behaves correctly beyond not-crashing.
Here we will identify properties that should be satisfied by our function and we will test that each of these properties hold for a broad and diverse set of inputs to our function.

Just as Hypothesis' strategies enable us to fuzz-test our code with highly diverse inputs, they will serve to drive our property-based tests as well.

As an example, let's write some property-based tests for Python's `sorted` function and make sure that it properly sorts lists of integers & floats correctly along with lists of strings.

<!-- #region -->
```python
from collections import Counter

from hypothesis import given
import hypothesis.strategies as st


@given(
    arg=st.one_of(
        st.lists(st.integers() | st.floats(allow_nan=False)), # nans aren't orderable
        st.lists(st.text()),
    )
)
def test_sorted_property_based(arg):
    result = sorted(arg)
    
    # Property 1:
    # Check that entries of `result` are in ascending order.
    for a, b in zip(result, result[1:]):
        assert a <= b
    
    # Property 2:
    # Check that `result` and `arg` contain the same elements,
    # disregarding their order
    assert Counter(result) == Counter(arg)
```
<!-- #endregion -->

<!-- #region -->
This is a simple but powerful test!
Because we are using Hypothesis to generate the inputs to this test, we are exercising `sorted` with lists of varying lengths (including empty lists), of all redundant entries, containing positive and negative infinities, and so on.
Furthermore, we were able to identify two simple properties that, taken together, assure that `result` is indeed a sorted list.
Put another way, any manual test that we could write for `sorted` would be redundant with the assurances provided to us by `test_sorted_property_based`.
Lastly, consider how much more tedious and brittle it would be to write parameterized test that exercises a comparably-diverse set of inputs and desired outputs! 

It is important to note that property-based testing does not require you to identify a "complete" set of properties that fully guarantee correctness in our code.
Let's consider the following property-based test of our `count_vowels` function:

```python
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
```

Testing these properties alone shouldn't make us confident that `count_vowels` is behaving as expected; after all, we never actually verify that the vowel count is exactly correct.
But testing these properties *alongside some manual test cases* is a **very** powerful combination.

Consider the following smattering of manual tests:

```python
@pytest.mark.parametrize(
    "input_string, include_y, expected_count",
    [
        ("aA bB yY", False, 2),
        ("aA bB yY", True, 4),
        ("123bacediouyz", False, 5),
        ("b a c e d i o u y z", True, 6),
    ],
)
def test_count_vowels_parameterized(
    input_string: str, include_y: bool, expected_count: int
):
    assert count_vowels(input_string, include_y) == expected_count
```

These manual test cases are far from exhaustive, but when viewed in conjunction with the properties that we tested above, we suddenly realize that `count_vowels` is being tested quite thoroughly!
Take some time to reflect on how much more expressive each of these test cases become when we have the additional assurance that they also satisfy the properties tested above.
It should be clear that we aren't explicitly testing that the properties hold for these parameterized cases, but given that Hypothesis is generating *much* more diverse (and plentiful) examples in our PBT, we can be confident that the properties hold for our manual cases as well. 
<!-- #endregion -->

<!-- #region -->
<div class="alert alert-info">

**Exercise: Running a Hypothesis-Driven, Property-Based Test**

Create the file `tests/test_properties.py` and add the `test_count_vowels_property_based` test to it.
Are there any other properties that you might test?
Run your test suite and verify that this test is run and that it passes.
    
Revisit the parameterized tests that you wrote for `count_vowels` and consider adding some additional cases that, in conjunction with these property based tests, will help improve our confidence in `count_vowels`.


</div>




<!-- #endregion -->

<!-- #region -->
<div class="alert alert-info">

**Exercise: Writing Your Own Property-Based Test**

Add to `tests/test_properties.py` a property-based test for `merge_max_mappings`.

You can use the following strategy to generate dictionaries with strings as keys and numbers as values:
    
```python
st.dictionaries(keys=st.text(), values=st.integers() | st.floats(include_nan=False))
```
    
Can you identify a minimal and "complete" set of properties to test here? 

</div>

<!-- #endregion -->

<div class="alert alert-info">

**Exercise: Hypothesis, the automated CS tutor**

Suppose that you were responsible for writing tests for Python's all-important [`range()`](https://docs.python.org/3/library/functions.html#func-range).
Using Hypothesis, write a test that verifies the property that `len(range(size)) == size`, where `size` is any non-negative integer.

Go ahead and write/run the test...

.
    
.
    
.

You may be surprised to find that `len(range(size)) == size` does *not* pass for arbitrary non-negative integers.
Instead, this test reveals that the CPython implementation of the built-in `len` function is such that it can only handle non-negative integers smaller than $2^{63}$ (i.e. it will only allocate 64 bits to represent a signed integer - one bit is used to store the sign of the number).
Hypothesis should have revealed this by generating the failing test case `size=9223372036854775808`, which is exactly $2^{63}$.

Hypothesis has a knack for catching these sorts of unexpected edge cases!
In fact, this overflow behavior is now documented in the CPython source code because it was discovered while writing this material 😄.
Thus you can think of Hypothesis as your personal CS tutor.
It will tell you things about Python that you never knew that you wanted to know.
</div>


<!-- #region -->
## Extra: Test-Driven Development


We want to complete the following function:

```python
def leftpad(string: str, width: int, fillchar: str) -> str:
    """Left-pads `string` with `fillchar` until the resulting string
    has length `width`.
    
    Parameters
    ----------
    string : str
        The input string
    
    width : int
        A non-negative integer specifying the minimum guaranteed
        width of the left-padded output string.
    
    fillchar : str
        The character (length-1 string) used to pad the string.
    
    Examples
    --------
    The following is the intended behaviour of this function:
    
    >>> leftpad('cat', width=5, fillchar="Z")
    'ZZcat'
    >>> leftpad('Dog', width=2, fillchar="Z")
    'Dog'
    """
    assert isinstance(width, int) and width >= 0, width
    assert isinstance(fillchar, str) and len(fillchar) == 1, fillchar
    # YOUR CODE HERE
```

But let's use test-driven development to do so.
That is, include the above function stub in `pbt_tutorial/basic_function.py` (without completing the function) and then begin writing one or more property-based tests for it in `tests/test_properties.py`.
From the outset your test should fail, since the function hasn't been implemented.

Once you are satisfied with your property-based test for `leftpad`, proceed to complete your implementation of the function and use your test to drive your development (e.g. rely on it to tell you if you have gotten something wrong or have missed any edge cases). 
<!-- #endregion -->
