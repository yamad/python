"""Tests for spiral value problem:

Given an M x N matrix, return the values of the matrix in spiral order

Example: Spiral values
======================

Identify the domain
-------------------

From the problem statement, we know we are expecting a matrix--a 2-dimensional data structure of some form--defined by at least two key parameters:

* `m` -- number of rows
* `n` -- number of columns

These are counts, so they are non-negative integers: Z x Z.

From this, we already know a lot of stuff:

* We can reject non-2D data structures
* The domain is infinite (Z x Z)

Cover the domain
----------------

We'll start by choosing some simple example inputs. Then we notice that the relation between `m` and `n` is a nice way to decompose an infinite domain into a few basic cases. The only possible cases are that:

* m > n, a tall matrix
* m < n, a wide matrix
* m == n, a square matrix

This reduces an infinite space to just 3 important tests. This analysis tells us concretely that if we test a 3 x 5 (m < n) matrix, it probably doesn't do us much good to test a 3 x 6 (m < n + 1) matrix. On the other hand, it makes clear that if we test a 3 x 5 matrix, we are missing an important case if we don't also test a 5 x 3 matrix.

Similarly, we can start decomposing Z (non-negative integers) into a small set of relevant cases:

For each dimension, we may have:

* 0
* 1
* even
* odd

Thus, the combination gives 8 cases:

* m=0, n=?,
* m=?, n=0,
* m=1, n=?
* m=?, n=1
* m is even, n is even
* m is even, n is odd
* m is odd, n is even
* m is odd, n is odd

For good measure, we'll add two more special cases:

* m=0, n=0, an empty matrix
* m=1, n=1, single element matrix

Note that these are formally covered by the above, but are unique enough that they are worthy of checking separately.

We've ended up with this list:

* Simple cases:

  * choose basic examples, assert expected output
  * tall matrix            (m > n)
  * wide matrix            (m < n)
  * square matrix          (m == n)
  * even rows, even cols   (m is even, n is even)
  * even rows, odd cols    (m is even, n is odd)
  * odd rows, even cols    (m is odd, n is even)
  * odd rows, odd cols     (m is odd, n is odd)

* Edge cases

  * row vector             (m = 1)
  * column vector          (n = 1)
  * matrix with 1 value    (m = 1 and n = 1)
  * empty matrix           (m = 0 and n = 0)

* Error cases:

  * invalid matrix? something that can't spiralized. not a rectangular matrix in R^2.
    * every subarray is 1D and of the same length (assuming input type like: list[list[Any]]).
  * non-2D input ?? (decide if this is an assumption or not)

* Properties:

  * len(output) == m * n
  * given matrix from 1 to MxN values, when output in spiral order, then difference is either 1 or -1 or width or -w
  * same elements in input matrix are in output
"""
import hypothesis.extra.numpy as hyp_np
import numpy as np
import pytest
from hypothesis import given

import spiral_values

# add implementations of the spiral value function here
funcs = {
    "iterative layers, pure python": spiral_values.spiral_values_iterative_indexing,
    "recursive layers, numpy": spiral_values.spiral_values_numpy_recursive,
    "iterative layers, numpy": spiral_values.spiral_values_numpy_iter,
    "recursive rotation, numpy": spiral_values.spiral_values_numpy_rotate_recursive,
    "iterative rotation, numpy": spiral_values.spiral_values,
}


@pytest.fixture(
    scope="session",
    params=funcs.values(),
    ids=[f"{name} ({func.__name__})" for name, func in funcs.items()],
)
def spiral_values(request):
    """Spiral value implementations to test"""
    func = request.param
    return lambda x: list(func(x))


## Simple cases and edge cases
## ===========================

# add simple test cases with expected output here:
# test name: (input, expected output)
test_cases = {
    "2 x 2": ([[1, 2], [3, 4]], [1, 2, 4, 3]),
    "3 x 3": ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [1, 2, 3, 6, 9, 8, 7, 4, 5]),
    "3 x 4": (
        [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],
        [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7],
    ),
    "4 x 3": (
        [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]],
        [1, 2, 3, 6, 9, 12, 11, 10, 7, 4, 5, 8],
    ),
    "tall, m > n": (
        [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15]],
        [1, 2, 3, 6, 9, 12, 15, 14, 13, 10, 7, 4, 5, 8, 11],
    ),
    "wide, m < n": (
        [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]],
        [1, 2, 3, 4, 5, 10, 9, 8, 7, 6],
    ),
    "row vector": ([[1, 2, 3, 4]], [1, 2, 3, 4]),
    "column vector": ([[1], [2], [3], [4]], [1, 2, 3, 4]),
    "point": ([[0]], [0]),
    "empty": ([[]], []),
}


@pytest.mark.parametrize("matrix, expected", test_cases.values(), ids=test_cases.keys())
def test_case(matrix, expected, spiral_values):
    assert spiral_values(matrix) == expected


@given(
    matrix=hyp_np.arrays(
        shape=hyp_np.array_shapes(), dtype=hyp_np.integer_dtypes()
    ).filter(lambda x: x.ndim != 2)
)
def test_wrong_dimensions(matrix, spiral_values):
    with pytest.raises(ValueError):
        spiral_values(matrix)

def test_uneven_rows(spiral_values):
    matrix = [[1, 2], [3], [4, 5, 6]]
    with pytest.raises(ValueError):
        spiral_values(matrix)

## Properties
## ===========

st_matrix_shape = hyp_np.array_shapes(min_dims=2, max_dims=2)
st_matrix = hyp_np.arrays(shape=st_matrix_shape, dtype=hyp_np.integer_dtypes())


@given(matrix=st_matrix)
def test_output_length(matrix, spiral_values):
    assert matrix.size == len(spiral_values(matrix.tolist()))


@given(matrix=st_matrix)
def test_same_elements(matrix, spiral_values):
    assert sorted(matrix.flat) == sorted(spiral_values(matrix))


@given(matrix_shape=hyp_np.array_shapes(min_dims=2, max_dims=2, min_side=2))
def test_differences(matrix_shape, spiral_values):
    """Given a matrix of values in sequential order, adjacent values in spiral result will be:

      - 1 in x direction
      - width in y direction
    """
    matrix = np.arange(np.prod(matrix_shape)).reshape(matrix_shape)
    res = spiral_values(matrix)
    absolute_diffs = set(np.abs(np.diff(res)))
    width = matrix.shape[1]
    assert {1, width} == absolute_diffs


@given(
    matrix=hyp_np.arrays(
        shape=hyp_np.array_shapes(min_dims=2, max_dims=2, min_side=2),
        dtype=hyp_np.integer_dtypes(),
    )
)
def test_bottom_left_corner_value(matrix, spiral_values):
    values = spiral_values(matrix)
    height, width = matrix.shape
    last_index = width * 2 + (height - 2) - 1
    assert values[last_index] == matrix[-1, 0]


@given(matrix=st_matrix)
def test_bottom_right_corner_value(matrix, spiral_values):
    values = spiral_values(matrix)
    bottom_right_index = sum(matrix.shape) - 2
    assert values[bottom_right_index] == matrix[-1, -1]


def next_layer_index(matrix):
    height, width = matrix.shape
    if height == 1:
        return width
    elif width == 1:
        return height
    else:
        return width * 2 + (height - 2) * 2


@given(
    matrix=hyp_np.arrays(
        shape=hyp_np.array_shapes(min_dims=2, max_dims=2, min_side=2),
        dtype=hyp_np.integer_dtypes(),
    )
)
def test_last_outer_layer_value(matrix, spiral_values):
    values = spiral_values(matrix)
    last_index = next_layer_index(matrix) - 1
    assert values[last_index] == matrix[1, 0]


@given(matrix=hyp_np.arrays(
        shape=hyp_np.array_shapes(min_dims=2, max_dims=2, min_side=3),
        dtype=hyp_np.integer_dtypes(),
    ))
def test_inner_layer_is_equivalent(matrix, spiral_values):
    outer_values = spiral_values(matrix)
    inner_values = spiral_values(matrix[1:-1, 1:-1])
    assert outer_values[next_layer_index(matrix) :] == inner_values
