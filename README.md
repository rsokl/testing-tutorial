# An Introduction to Methods for Doing Test-Driven Research
> Created by: Ryan Soklaski and Zac Dodds

This tutorial is designed to introduce attendees to (the wonderful world of) automated testing in Python 
– specifically for data science applications.

- [An Introduction to Methods for Doing Test-Driven Research](#an-introduction-to-methods-for-doing-test-driven-research)
  - [Introduction](#introduction)
  - [Syllabus](#syllabus)
    - [Property-Based Testing 101](#property-based-testing-101)
    - [Describe your Data](#describe-your-data)
    - [Common Tests](#common-tests)
    - [Putting it into Practice](#putting-it-into-practice)
  - [Prerequisites](#prerequisites)
  - [Creating a Python Environment for this Tutorial](#creating-a-python-environment-for-this-tutorial)
  - [For Instructors](#for-instructors)

## Introduction

This tutorial is designed to promote simple but powerful methods for bolstering your software-based work/research with 
property-based testing, and thereby help to close the aperture on “the things that could go wrong” because of your code.
It is structured as four blocks, each consisting of a short talk, live-coded demo, and extensive exercises for attendees:
1. Property-Based Testing 101: core concepts and the core of the Hypothesis library
2. Describe your Data: from numbers, to arrays, to recursive and more complicated things
3. Common Tests: from "does not crash" to "write+read == noop" to 'metamorphic relations'
4. Putting it into Practice: use what you've learned to find real bugs in a real project!

Each of these blocks runs for 40-60 minutes, consisting of a 5-15 minute presentation, around 5-10 minutes live-coding demo, and guided exercises.
Along with a short break in the middle, I find this pattern balances content, practice, and focus well for most classes.


## Syllabus
The material will be offered as a three-hour session. There will be a mixture of lectures with hands-on exercises. The following topics will be explored:

 ### Property-Based Testing 101
  - PLACEHOLDER

### Describe your Data
  - PLACEHOLDER

### Common Tests
  - PLACEHOLDER

### Putting it into Practice
  - PLACEHOLDER


## Prerequisites

Attendees are expected to have access to a computer with with Python 3.6+ installed on it and should know how to run Jupyter notebooks.
A complete description of how to do this is detailed in [Module 1 of Python Like You Meant It](https://www.pythonlikeyoumeanit.com/module_1.html).

It is also recommended that you prepare yourself to work in your IDE of choice for Python. If you do not have an IDE that you are comfortable with yet, [Visual Studio code and PyCharm are both highly recommended](https://www.pythonlikeyoumeanit.com/Module1_GettingStartedWithPython/Getting_Started_With_IDEs_and_Notebooks.html).


## Creating a Python Environment for this Tutorial

You will need the to install the following packages to complete this tutorial:

- numpy
- notebook
- pytest
- hypothesis

To create a mini-conda environment for this tutorial, in your terminal execute:

```shell
> conda create -n test-tutorial python=3.8
> conda activate test-tutorial
> conda install notebook numpy pytest hypothesis
> pip install mygrad
```

## For Instructors

The source material for this tutorial is written in [jupytext-markdown](https://jupytext.readthedocs.io/en/latest/formats.html#jupytext-markdown) in lieu of native Jupyter notebooks. 
These are markdown files that can be opened as Jupyter notebooks.
These markdown notebooks contain both the exercises and solutions.
To convert these files to Jupyter notebooks to be distributed to the students, with the solutions excised, we are using the [cogbooks](https://github.com/CogWorksBWSI/Cogbooks) tool, which can be installed with: `pip install cogbooks` 

