---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.9.1
  kernelspec:
    display_name: Python [conda env:.conda-testing-tutorial]
    language: python
    name: conda-env-.conda-testing-tutorial-py
---

# Traversing the Taxonomy of Testing


We expect your to write your to write pytest-style tests, which is exemplified by `test_count_vowels`, which can be found below.
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
from pbt_tutorial import count_vowels

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

<!-- #region -->
## Fuzzing

Fuzz testing is a simple, but often (embarrassingly) powerful approach to automated testing in which we feed a function a wide variety of randomly-generated inputs to see if it ever crashes.
For example, the following test "fuzzes" the `int` type with finite float inputs, to see if `int(<finite-float>)` ever causes a crash.

```python
@given(x=st.floats(allow_infinity=False, allow_nan=False))
def test_fuzz_in_with_finite_floats(x):
    int(x)  # no asserts needed!
```

while this test doesn't do much to assure us that `int` casts floats _correctly_, it is nonetheless a very simple and expressive test that gives us confidence that feeding a finite float will never cause `int` to crash.
We should appreciate just how trivial it is to write this test.

Fuzzing can be especially useful if we have our source code with internal internal `assert` statements.
Seeing that these assertions hold true even when our function is being fed truly bizarre and exotic (but valid!) input data helps close the aperture on where future bugs are coming from – we can at least be confident that they aren't coming from incorrect assertions.

([Seriously! Fuzzing can be very effective](https://github.com/google/oss-fuzz))
<!-- #endregion -->

<div class="alert alert-info">

**Exercise: Running a Parameterized Test**

Create the file `tests/test_fuzz.py`.
Use the Hypothesis strategies [text(](https://hypothesis.readthedocs.io/en/latest/data.html#hypothesis.strategies.text) and [booleans()](https://hypothesis.readthedocs.io/en/latest/data.html#hypothesis.strategies.booleans) to fuzz the `count_vowels` function.
    
Consider temporarily adding a print statement to your test to get a peek at the sort of data that you are fuzzing your function with.
    
The more inputs you feed a function in a fuzz test, the better. Take a glance at the documentation for [Hypothesis' settings](https://hypothesis.readthedocs.io/en/latest/settings.html) and increase the number of examples run in your fuzz test from 100 to 1,000.
</div>






## Property-Based Tests

<!-- #region -->
## Extra: Test-Driven Development


Using Hypothesis' [`text()` strategy](https://hypothesis.readthedocs.io/en/latest/data.html#hypothesis.strategies.text)
<!-- #endregion -->



```python

```
