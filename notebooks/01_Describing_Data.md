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

# Describing Your Data with Hypothesis


## Useful Links
- [Hypothesis' core strategies](https://hypothesis.readthedocs.io/en/latest/data.html)
- [The `.map` method](https://hypothesis.readthedocs.io/en/latest/data.html#mapping)
- [The `.filter` method](https://hypothesis.readthedocs.io/en/latest/data.html#filtering)
- [The `example` decorator](https://hypothesis.readthedocs.io/en/latest/reproducing.html#providing-explicit-examples)
- [Using `data()` to draw interactively in tests](https://hypothesis.readthedocs.io/en/latest/data.html#drawing-interactively-in-tests)

<!-- #region -->
## Hypothesis "Strategies"

As we learned in the previous section, Hypothesis provides us with so-called "strategies" for describing our data.
These are all located in the `hypothesis.strategies` module. The official documentation for the core strategies can be found [here](https://hypothesis.readthedocs.io/en/latest/data.html).

We will import this module under the alias `st` throughout this tutorial:

```python
import hypothesis.strategies as st
```

A strategy, once initialized, is an object that Hypothesis will use to generate data for our test. **The `given` decorator is responsible for drawing values from strategies and passing them as inputs to our test.**

For example, let's write a toy test for which `x` should be integers between 0 and 10, and `y` should be integers between 20 and 30:
<!-- #endregion -->

```python
import hypothesis.strategies as st
from hypothesis import given

# using `given` with multiple parameters
@given(x=st.integers(0, 10), y=st.integers(20, 30))
def demonstrating_the_given_decorator(x, y):
    assert 0 <= x <= 10
    assert 20 <= y <= 30
```

Running the test will prompt Hypothesis to draw 100 random pairs of values for `x` and `y`, according to their respective strategies, and the body of the test will be executed for each such pair:

```python
demonstrating_the_given_decorator()
```

Note that it is always advisable to specify the parameters of `given` as keyword arguments, so that the correspondence between our strategies with the function-signature's parameters are manifestly clear.


<div class="alert alert-info">

**Exercise: Describing data with `booleans()`**

Write a test that takes in a parameter `x`, that is a boolean value. Use the [`st.booleans()` strategy](https://hypothesis.readthedocs.io/en/latest/data.html#hypothesis.strategies.booleans) to describe the data. In the body of the test, assert that `x` is either `True` or `False`.

Run your test, and try mutating it to ensure that it can fail appropriately.

</div>


```python
# Write a test that uses the `st.booleans()` strategy
# <COGINST>
@given(x=st.booleans())
def testing_booleans(x):
    assert x is True or x is False

testing_booleans()
# </COGINST>
```

<!-- #region -->
### Viewing examples drawn from strategies

Hypothesis provides a useful mechanism for developing an intuition for the data produced by a strategy. A strategy, once initialized, has a `.example()` method that will randomly draw a representative value from the strategy. For example:

```python
# demonstrating usage of `<strategy>.example()`
>>> st.integers(-1, 1).example()
-1

>>> st.booleans()
True
```

**Note: the `.example()` mechanism is only meant to be used for pedagogical purposes. You should never use this in your test suite**
because (among other reasons) `.example()` biases towards smaller and simpler examples than `@given`, and lacks the features to ensure any test failures are reproducible.
<!-- #endregion -->

<div class="alert alert-info">

**Exercise: Write a `print_examples` function**

Write a function called `print_examples` that takes in two arguments:
 - an initialized hypothesis strategy (e.g. `st.integers(0, 10)`)
 - `n`: the number of examples to print
 
 Have it print the strategy (simply call `print` on the strategy) and `n` examples generated from the strategy. Use a for-loop.

</div>


```python
# Define the `print_examples` function
# <COGINST>
def print_examples(strategy, n):
    print(f"{n} examples drawn from {strategy}:\n")
    for _ in range(n):
        print(strategy.example())
# </COGINST>
```

Print five examples from the `st.integers(...)` strategy, with values ranging from -10 to 10. Then print 10 examples from the `st.booleans()` strategy.

```python
print_examples(st.integers(-10, 10), 5)  # <COGLINE>
```

```python
print_examples(st.booleans(), 5)  # <COGLINE>
```

<!-- #region -->
### The `.map` method

Hypothesis strategies have the `.map` method, which permits us to perform a mapping on the data being produced by a strategy. For example, if we want to draw only even-valued integers, we can simply use the following mapped strategy:

```python
# we can apply mappings to strategies
even_integers = st.integers().map(lambda x: 2 * x)
```
(`.map` can be passed any callable, it need not be a lambda)
<!-- #endregion -->

<div class="alert alert-info">

**Exercise: Understanding the `.map` method**

Write a test that uses the afore-defined `even_integers` strategy to generate data. The body of the test should assert that the input to the test is indeed an even-valued integer. 

Run your test (and try adding a bad assertion to make sure that the test can actually fail!)

</div>


```python
# write the test for `even_integers`

# <COGINST>
@given(st.integers().map(lambda x: 2 * x))
def test_even_ints(x):
    assert isinstance(x, int)
    assert x % 2 == 0


test_even_ints()
# </COGINST>
```

<div class="alert alert-info">

**Exercise: Getting creative with the `.map` method**

Construct a Hypothesis strategy that produces either the string `"cat"` or the string `"dog"`. Then write a test that checks the property of this strategy and run it

</div>



```python
# Write the cat-or-dog strategy
# <COGINST>
cat_dog = st.booleans().map(lambda x: "cat" if x else "dog")


@given(cat_dog)
def test_cat_dog(x):
    assert x in {"cat", "dog"}


test_cat_dog()
# </COGINST>
```

<!-- #region -->
### The `.filter` method

Hypothesis strategies can also have their data filtered via the `.filter` method. `.filter` takes a callable that accepts as input the data generated by the strategy, and returns:
 - `True` if the data should pass through the filter
 - `False` if the data should be rejected by the filter

Consider, for instance, that you want to generate all integers other than `0`. You can write the filtered strategy:

```python
non_zero_integers = st.integers().filter(lambda x: x != 0)
```
<!-- #endregion -->

<div class="alert alert-info">

**Exercise: Understanding the `.filter` method**

Write a test that uses the afore-defined `non_zero_integers` strategy to generate data. The body of the test should assert that the input to the test is indeed a nonzero integer. 

Run your test (and make sure that it can fail!)

</div>


```python
# Write the test for `non_zero_integers`
# <COGINST>
@given(st.integers().filter(lambda x: x != 0))
def test_nonzero_ints(x):
    assert isinstance(x, int)
    assert x != 0


test_nonzero_ints()
# </COGINST>
```

The `.filter` method is not magic. Hypothesis will raise an error if your strategy rejects too many values. 


<div class="alert alert-info">

**Exercise: The `.filter` method is not magic**

Write a strategy that applies a filter to `st.floats(allow_nan=False)` such that it only generates values on the domain `[10, 20]`.
Then write and run a test that that uses data from this strategy.

What is the name of the error that Hypothesis raises? How would you rewrite this strategy instead of using `.filter`?

</div>


```python
# <COGINST>
@given(st.floats(allow_nan=False).filter(lambda x: 10.0 <= x <= 20.0))
def test_aggressive_filter(x):
    assert isinstance(x, float)
    assert 10 <= x <= 20


test_aggressive_filter()
# </COGINST>
```

## The `example` Decorator

As mentioned before, Hypothesis strategies will draw values (pseudo)*randomly*.
Thus our test will potentially encounter different values every time it is run.
There are times where we want to be sure that, in addition the values produced by a strategy, specific values will tested. 
These might be known edge cases, critical use cases, or regression cases (i.e. values that were representative of passed bugs).
Hypothesis provides [the `example` decorator](https://hypothesis.readthedocs.io/en/latest/reproducing.html#providing-explicit-examples), which is to be used in conjunction with the `given` decorator, towards this end.

Let's suppose, for example, that we want to write a test whose data are pairs of perfect-squares (e.g. 4, 16, 25, ...), and that we want to be sure that the pairs `(100, 144)`, `(16, 25)`, and `(36, 36)` are tested *every* time the test is run. 
Let's use `example` to guarantee this.

```python
from hypothesis import example

perfect_squares = st.integers().map(lambda x: x ** 2)


def is_square(x):
    return int(x ** 0.5) == x ** 0.5


@example(a=36, b=36)
@example(a=16, b=25)
@example(a=100, b=144)
@given(a=perfect_squares, b=perfect_squares)
def test_pairs_of_squares(a, b):
    assert is_square(a)
    assert is_square(b)


test_pairs_of_squares()
```

Executing this test runs 103 cases: the three specified examples and one hundred pairs of values drawn via `given`.


## Exploring Strategies

There are a number critical Hypothesis strategies for us to become familiar with. It is worthwhile to peruse through all of Hypothesis' [core strategies](https://hypothesis.readthedocs.io/en/latest/data.html#core-strategies), but we will take time to highlight a few here.

### [`st.lists ()`](https://hypothesis.readthedocs.io/en/latest/data.html#hypothesis.strategies.lists)

[`st.lists`](https://hypothesis.readthedocs.io/en/latest/data.html#hypothesis.strategies.lists) accepts *another* strategy, which describes the elements of the lists being generated. You can also specify:
 - bounds on the length of the list
 - if we want the elements to be unique
 - a mechanism for defining "uniqueness"
 
**`st.lists(...)` is the strategy of choice anytime we want to generate sequences of varying lengths with elements that are, themselves, described by strategies**. Recall that we can always apply the `.map` method if we want a different type of collection (e.g. a `tuple`) other than a list.

Use `print_examples` to build an intuition for this strategy.


<div class="alert alert-info">

**Exercise: Describing data with `st.lists`**

Write a strategy that generates unique **tuples** of even-valued integers, ranging from length-5 to length-10. 

Write a test that checks these properties.

</div>


```python
# <COGINST>
even_integers = st.integers().map(lambda x: 2 * x)

strat = st.lists(even_integers, min_size=5, max_size=10, unique=True).map(tuple)

@given(x=strat)
def test_even_lists(x):
    assert isinstance(x, tuple)
    assert 5 <= len(x) <= 10
    assert len(set(x)) == len(x)
    assert all(isinstance(i, int) for i in x)
    assert all(i % 2 == 0 for i in x)


print_examples(strat, 3)
test_even_lists()
# </COGINST>
```

### [`st.floats()`](https://hypothesis.readthedocs.io/en/latest/data.html#hypothesis.strategies.floats)

[`st.floats`](https://hypothesis.readthedocs.io/en/latest/data.html#hypothesis.strategies.floats) is a powerful strategy that generates all variety of floats, including `math.inf` and `math.nan`. You can also specify:
 - whether `math.inf` and `math.nan`, respectively, should be included in the data description
 - bounds (either inclusive or exclusive) on the floats being generated; this will naturally preclude `math.nan` from being generated
 - the "width" of the floats; e.g. if you want to generate 16-bit or 32-bit floats vs 64-bit
   (while Python `float`s are always 64-bit, `width=32` ensures that the generated values can
   always be losslessly represented in 32 bits.  This is mostly useful for Numpy arrays.)


<div class="alert alert-info">

**Exercise: Using Hypothesis to learn about floats.. Part 1**

Use the `st.floats` strategy to identify which float(s) violate the identity: `x == x`

Then, revise your usage of `st.floats` such that it only describes values that satisfy the identity. 
</div>


```python
# using `st.floats` to find value(s) that violate `x == x`
# <COGINST>
@given(x=st.floats())
def test_broken_identity(x):
    assert x == x


test_broken_identity()
# </COGINST>
```

```python
# updating our usage of `st.floats` to generate only values that satisfy `x == x`
# <COGINST>
@given(x=st.floats(allow_nan=False))
def test_fixed_identity(x):
    assert x == x


test_fixed_identity()
# </COGINST>
```

<!-- #region -->
<div class="alert alert-info">

**Exercise: Using Hypothesis to learn about floats.. Part 2**

Use the `st.floats` strategy to identify which **positive** float(s) violate the inequality: `x < x + 1`.

To interpret your findings, it is useful to know that a double-precision (64-bit) binary floating-point number, which is representative of Pythons `float`, has a coefficient of 53 bits (including 1 implied bit), an exponent of 11 bits, and 1 sign bit. 


Then, revise your usage of `st.floats` such that it only describes values that satisfy the identity. **Use the `example` decorator to ensure that the identified boundary case is tested every time**.
</div>

<!-- #endregion -->

```python
# using `st.floats` to find value(s) that violate `x < x + 1`
# <COGINST>
@given(x=st.floats(min_value=0))
def test_broken_inequality(x):
    assert x < x + 1


test_broken_inequality()
# </COGINST>
```

```python
# updating our usage of `st.floats` to generate only values that satisfy `x < x + 1`
# <COGINST>
from hypothesis import example


@example(x=2.0 ** 53 - 1)  # ensures that maximum permissible value is tested
@given(x=st.floats(min_value=0, max_value=2.0 ** 53, exclude_max=True))
def test_fixed_inequality(x):
    assert x < x + 1


test_fixed_inequality()
# </COGINST>
```

### [`st.tuples()`](https://hypothesis.readthedocs.io/en/latest/data.html#hypothesis.strategies.tuples)

The [st.tuples](https://hypothesis.readthedocs.io/en/latest/data.html#hypothesis.strategies.tuples) strategy accepts $N$ Hypothesis strategies, and will generate length-$N$ tuples whose elements are drawn from the respective strategies that were specified as inputs.

For example, the following strategy will generate length-3 tuples whose entries are: even-valued integers, booleans, and odd-valued floats:

```python
my_tuples = st.tuples(
    st.integers().map(lambda x: 2 * x),
    st.booleans(),
    st.integers().map(lambda x: 2 * x + 1).map(float),
)
print_examples(my_tuples, 4)
```

[st.just](https://hypothesis.readthedocs.io/en/latest/data.html#hypothesis.strategies.just) is a strategy that "just" returns the value that you fed it. This is a convenient strategy that helps us to avoid abusing the use of `.map` to concoct particular strategies.


<div class="alert alert-info">

**Exercise: Describing the shape of an array of 2D vectors**

Write a strategy that describes the shape of an array (i.e. a tuple of integers) that contains 1-to-20 two-dimensional vectors.
E.g. `(5, 2)` is the shape of the array containing five two-dimensional vectors.
Avoid using `.map()` in your solution.    

Use `print_examples` to examine the outputs.
</div>


```python
# <COGINST>
shapes_2D = st.tuples(st.integers(1, 20), st.just(2))

print_examples(shapes_2D, 5)
# </COGINST>
```

<!-- #region -->
### [`st.one_of()`](https://hypothesis.readthedocs.io/en/latest/data.html#hypothesis.strategies.one_of)

The `st.one_of` allows us to specify a collection of strategies and any given datum will be drawn from "one of" them. E.g.

```python
# demonstrating st.one_of()
st.one_of(st.integers(), st.lists(st.integers()))
```

will draw values that are either integers or list of integers. 
<!-- #endregion -->

<!-- #region -->
Note that the "pipe" operator is overloaded by Hypothesis strategies as a shorthand for `one_of`; e.g.

```python
st.integers() | st.floats() | st.booleans()
```

is equivalent to:


```python
st.one_of(st.integers(), st.floats(), st.booleans())
```
<!-- #endregion -->

<div class="alert alert-info">

**Exercise: Stitching together strategies for rich behavior**

Write a strategy that draws a tuple of two perfect squares (integers) or three perfect cubes (integers)

Use `print_examples` to examine the behavior of your strategy.
</div>


```python
# <COGINST>
squares = st.integers().map(lambda x: x ** 2)
cubes = st.integers().map(lambda x: x ** 3)
squares_or_cubes = st.tuples(squares, squares) | st.tuples(cubes, cubes, cubes)

print_examples(squares_or_cubes, 5)
# </COGINST>
```

<!-- #region -->
### [`st.fixed_dictionaries()`](https://hypothesis.readthedocs.io/en/latest/data.html#hypothesis.strategies.fixed_dictionaries)

`st.fixed_dictionaries` takes a mapping of the form `key -> strategy` and returns a strategy according to that mapping. E.g.

```python
# demonstrating st.fixed_dictionaries()
>>> mapping = dict(age=st.integers(0, 89), height=st.floats(3, 7)
>>> st.fixed_dictionaries(mapping).example()
{'age': 7, 'height': 3.5}
```

will draw values that are either integers or list of integers. 
<!-- #endregion -->

### [`st.sampled_from`](https://hypothesis.readthedocs.io/en/latest/data.html#hypothesis.strategies.sampled_from)

Finally, [`st.sampled_from`](https://hypothesis.readthedocs.io/en/latest/data.html#hypothesis.strategies.sampled_from) accepts a collection of objects. The strategy will return values that are sampled from this collections.


<div class="alert alert-info">

**Exercise: Describing objects that evaluate to `False`**

Write a strategy that can return the boolean, integer, float, string, list, tuple, or dictionary that evaluates to `False` (when called on by `bool`)

Use `print_examples` to examine the behavior of your strategy.
</div>


```python
# <COGINST>
falsies = st.sampled_from([False, 0, 0.0, "", [], tuple(), {}])

print_examples(falsies, 10)
# </COGINST>
```

<!-- #region -->
### [`st.from_type()`](https://hypothesis.readthedocs.io/en/latest/data.html#hypothesis.strategies.from_type)

`st.from_type` looks up a strategy associated with a given type or type-annotation

```python
>>> st.from_type(int)
integers()

>>> from typing import List, Dict
>>> st.from_type(List[int])
lists(integers())

>>> st.from_type(Dict[str, float])
dictionaries(keys=text(), values=floats())
```

You can use `st.register_type_strategy` to add or override type -> strategy mappings used by `st.from_type`:

```python
import math

class ComplexUnitCircle(complex): 
    pass

st.register_type_strategy(
    ComplexUnitCircle,
    st.floats(0, 2 * math.pi).map(lambda x: math.cos(x) + 1j * math.sin(x)),
)
```

```python
>>> st.from_type(ComplexUnitCircle).example()
(0.7599735905063035-0.6499539535482165j)
```

`hypothesis.infer` can be used within `@given` to indicate that an argument's values should be inferred from the annotation from the test's signature.
For example:

```python
from hypothesis import infer

@given(x=infer) # uses `from_type(ComplexUnitCircle)`
def test_with_infer(x: ComplexUnitCircle):
    assert isinstance(x, complex)
    assert math.isclose(abs(x), 1)
```
<!-- #endregion -->

<!-- #region -->
### [`st.builds()`](https://hypothesis.readthedocs.io/en/latest/data.html#hypothesis.strategies.builds)

`st.builds` is will "build" (call/instantiate) some target callable. `builds` is capable of inferring strategies based on the target's annotated signature (it uses `st.from_type` to do so), otherwise we can explicitly specify arguments for it to use. 

```python
# Defining a target for `st.builds`
from dataclasses import dataclass

@dataclass
class C:
    x: int
    y: str
```

`builds` can either infer strategies to use, based on `C`'s type annotations:

```python
>>> st.builds(C).example()  # infers x->`st.integers()`, y->`st.text()`
C(x=57, y='\U00108b39W\U000a55f5ÈwC\U0009db0a')
```

or we can explicitly specify one or more of the strategies for describing the target's parameters

```python
>>> st.builds(C, x=st.just(-1111)).example()
C(x=-1111, y='A')
```
<!-- #endregion -->

<!-- #region -->
<div class="alert alert-info">

**Exercise: Registering a Strategy for a Type**

Given the following type
    
```python
from dataclasses import dataclass

@dataclass
class Student:
    age: int
    letter_grade: str
```

register a Hypothesis strategy in association with it (via `register_type_strategy`) that draws ages from the domain `[10, 18]` and letter grades from A-F (no pluses or minuses).
Next, write a test that draws a "class of students" (i.e. `List[Student]`), and use `hypothesis.infer` so that you don't have to write the strategy by-hand.
In the body of the test, simply print the values generated to describe the class of students.
</div>

<!-- #endregion -->

```python
# <COGINST>
from dataclasses import dataclass
from typing import List

from hypothesis import infer

@dataclass
class Student:
    age: int
    letter_grade: str


st.register_type_strategy(
    Student,
    st.builds(Student, age=st.integers(10, 18), letter_grade=st.sampled_from("ABCDEF")),
)

@given(class_of_students=infer)
def test_class(class_of_students: List[Student]):
    print(class_of_students)

test_class()
# </COGINST>
```

<div class="alert alert-info">

**Exercise: Exploring additional strategies**

Consult [Hypothesis' documentation](https://hypothesis.readthedocs.io/en/latest/data.html) 
</div>



## Drawing From Strategies Within a Test

We will often need to draw from a Hypothesis strategy in a context-dependent manner within our test. Suppose, for example, that we want to describe two lists of integers, but we want to be sure that the second list is longer than the first. [We can use the `st.data()` strategy to use strategies "interactively"](https://hypothesis.readthedocs.io/en/latest/data.html#drawing-interactively-in-tests) in this sort of way.

Let's see it in action:

```python
# We want two lists of integers, `x` and `y`, where we want `y` to be longer than `x`.

@given(x=st.lists(st.integers()), data=st.data())
def test_two_constrained_lists(x, data: st.DataObject):
    y = data.draw(st.lists(st.integers(), min_size=len(x) + 1), label="y")

    assert len(x) < len(y)


test_two_constrained_lists()
```

The `given` operator is told to pass two things to our test: 

 - `x`, which is a list of integers drawn from strategies
 - `data`, which is an instance of the `st.DataObject` class; this instance is what gets drawn from the `st.data()` strategy

The only thing that you need to know about `st.DataObject` is that it's `draw` method expects a hypothesis search strategy, and that it will immediately draw a value from said strategy during the test. You can also, optionally, pass a string to  `label` argument to the `draw` method. This simply permits you to provide a name for the item that was drawn, so that any stack-trace that your test produces is easy to interpret.


<div class="alert alert-info">

**Exercise: Drawing from a strategy interactively**

Write a test that is fed a list (of varying length) of non-negative integers. Then, draw a **set** (i.e. a unique collection) of non-negative integers whose sum is at least as large as the sum of the list.
The strategy [`st.sets`](https://hypothesis.readthedocs.io/en/latest/data.html#hypothesis.strategies.sets) will be useful for this.

</div>


```python
# <COGINST>
@given(the_list=st.lists(st.integers(min_value=0)), data=st.data())
def test_interactive_draw_skills(the_list, data):
    the_set = data.draw(
        st.sets(elements=st.integers(min_value=0)).filter(
            lambda x: sum(x) >= sum(the_list)
        )
    )
    assert sum(the_list) <= sum(the_set)


test_interactive_draw_skills()
# </COGINST>
```

```python
st.fixed_dictionaries(dict(age=st.integers(0, 89), height=st.floats(3, 7))).example()
```

```python

```

```python
- text
- dictionaries
- builds
- infer_type
- recipes
```
