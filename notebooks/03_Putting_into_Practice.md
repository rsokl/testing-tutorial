---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.11.2
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

# Putting it all into Practice

In this final section we'll practice the practical configuration tips that will help you apply property-based testing in the real world.

Now that we know how to write property-based tests, in this final section we will cover practical tips for using them as part of a larger project.  Test-suite design patterns, use of performance and determinism settings, reproducing test failures from a CI server, etc; they're all practical topics and typically left out of shorter introductions!


### The joy of `--hypothesis-show-statistics`

Hypothesis has [great support for showing test statistics](https://hypothesis.readthedocs.io/en/latest/details.html#test-statistics), including better-than-`print()` debugging with `note()`, custom `event()`s you can add to the summary, and a variety of performance details.

Let's explore those now: run `pytest --hypothesis-show-statistics test_statistics.py`.  You should see

- a lot of output from `printing`... if you actually want to see every example Hypothesis generates, use the `verbosity` setting instead!  You can even set it from the command-line with `--hypothesis-verbosity=verbose`.
- **one** line of output from `note()`
- statistics on the generate phase for both tests, and the shrink phase for the failing test.  If you re-run the tests, you'll see a `reuse` phase where notable examples from previous runs are replayed.

Useful, isn't it!


### Settings for Performance

Hypothesis is designed to behave sensibly by default, but sometimes you have something
more specific in mind.  At those times, [`hypothesis.settings`](https://hypothesis.readthedocs.io/en/latest/settings.html)
is here to help.

The main performance-related settings to know are:

- `max_examples` - the number of valid examples Hypothesis will run.  Defaults to 100; turning it up or down makes your testing proportionally more or less rigorous... and also proportionally slower or faster, respectively!
- `deadline` - if an input takes longer than this to run, we'll treat that as an error.  Useful to detect weird performance issues; but can be flaky if VM performance gets weird.

```python
from time import sleep
from hypothesis import given, settings, strategies as st

# TODO: add a settings decorator which reduces max_examples (for speed)
#       and increases or disables the deadline so the test passes.

@given(st.floats(min_value=0.1, max_value=0.3))
def test_really_slow(delay):
    sleep(delay)

test_really_slow()
```

### The `phases` setting

The phases setting allows you to individually enable or disable [Hypothesis' six phases](https://hypothesis.readthedocs.io/en/latest/settings.html#controlling-what-runs), and has two main uses:

- Disabling all but the `explicit` phase, reducing Hypothesis to parametrized tests ([e.g. here](https://github.com/python/cpython/pull/22863))
- Enabling the `explain` phase, accepting some overhead to report additional feedback on failures

Other use-cases tend to be esoteric, but are supported if you think of one.

```python
# See `tests/test_settings.py` for this exercise.
```

### Dealing with a PRNG

If you have test behaviour that depends on a psudeo-random number generator, and it's not being seeded between inputs, you're going to have some flaky tests.  [`hypothesis.register_random()` to the rescue!](https://hypothesis.readthedocs.io/en/latest/details.html#making-random-code-deterministic)

Try running this test a few times - you'll see the `Flaky` error - and then un-comment `hypothesis.register_random(r)`.  Instant determinism!

```python
import random
import hypothesis
from hypothesis.strategies import integers

r = random.Random()

# hypothesis.register_random(r)

@hypothesis.given(integers(0, 100))
def test_sometimes_flaky(x):
    y = r.randint(0, 100)
    assert x <= y

test_flaky()
```

### `target()`ed property-based testing

Random search works well... but [guided search with `hypothesis.target()`](https://hypothesis.readthedocs.io/en/latest/details.html#targeted-example-generation)
is even better.  Targeted search can help

- find rare bugs ([e.g.](https://github.com/astropy/astropy/pull/10373))
- understand bugs, by mitigating [the "threshold problem"](https://hypothesis.works/articles/threshold-problem/) (where shrinking makes severe bugs look marginal)

```python
# See `tests/test_settings.py` for this exercise.
```

### Hooks for external fuzzers

If you're on Linux or OSX, you may want to [experiment with external fuzzers](https://hypothesis.readthedocs.io/en/latest/details.html#use-with-external-fuzzers).
For example, [here's a fuzz-test for the Black autoformatter](https://github.com/psf/black/blob/3ef339b2e75468a09d617e6aa74bc920c317bce6/fuzz.py#L75-L85)
using Atheris as the fuzzing engine.

We can mock this up with our own very simple fuzzer:

```python
from secrets import token_bytes as get_bytes_from_fuzzer
from hypothesis import given, strategies as st


@given(st.nothing())
def test(_):
    pass 


# And now for the fuzzer:
for _ in range(1000):
    payload = get_bytes_from_fuzzer(1000)
    test.hypothesis.fuzz_one_input(payload)
```
