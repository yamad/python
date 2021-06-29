"""Spiral values

Given an M x N matrix, return the values of the matrix in spiral order

Examples

[1, 2, 3]
[4, 5, 6]
[7, 8, 9]

1 2 3 6 9 8 7 4 5

[1,  2,  3,  4],
[5,  6,  7,  8],
[9, 10, 11, 12],

1 2 3 4 8 12 11 10 9 5 6 7
"""
from typing import List, Any, Iterable, Tuple

import numpy as np


def spiral_values_iterative_indexing(matrix: List[List[Any]]) -> Iterable[Any]:
    """Return the values of matrix in spiral order"""
    validate_matrix(matrix)
    for i, j, _ in spiral_indices(matrix):
        yield matrix[i][j]


def validate_matrix(matrix):
    # all rows are the same length
    try:
        row_lengths = set(len(row) for row in matrix)
        if len(row_lengths) != 1:
            raise TypeError
    except TypeError:
        raise ValueError("must be a 2D list of lists")

    # all values are scalar
    if any(isinstance(x, Iterable) for row in matrix for x in row):
        raise ValueError("must be a 2D list of lists")


def spiral_indices(matrix: List[List[Any]]) -> Iterable[Tuple[int, int, str]]:
    """Return the indices (i, j, indicator) of the matrix in spiral order

    This implementation decomposes the matrix into layers from outside in, such that the outer
    border values are visited, then the values one layer in (starting at index 1,1) are visited,
    and so on.

    The 3rd element of each index is a debugging aid in the format: `{border indicator}{layer number}`

      * border indicator is one of [t, r, b, l], indicating the border is top, right, bottom, or left
      * layer number is the layer of the matrix the index arises from, starting from 0 as the outermost layer

    e.g. `t2` would mean that the index is from the top of the 3rd layer.
    """
    m = len(matrix)
    n = len(matrix[0])

    # define concentric rectangles to visit
    xstarts, xstops = range(0, n // 2 + 1), reversed(range(n // 2, n))
    ystarts, ystops = range(0, m // 2 + 1), reversed(range(m // 2, m))
    layers = zip(xstarts, xstops, ystarts, ystops)

    for i, (xstart, xstop, ystart, ystop) in enumerate(layers):
        for j in range(xstart, xstop + 1):  # top
            yield ystart, j, f"t{i}"

        for i in range(ystart + 1, ystop + 1):  # right
            yield i, xstop, f"r{i}"

        if xstart == xstop or ystart == ystop:  # handle single row or column
            break

        for j in reversed(range(xstart, xstop)):  # bottom
            yield ystop, j, f"b{i}"

        for i in reversed(range(ystart + 1, ystop)):  # left
            yield i, xstart, f"l{i}"


def spiral_values_numpy_recursive(matrix) -> Iterable[Any]:
    """Return the values of the matrix in spiral order

    This is a recursive numpy implementation that more directly encodes the layered logic of `spiral_values`.
    In particular, it directly shows that the spiral values can be recursively defined as:

      * values from the top, right, bottom, and left border
      * the spiral values of the matrix with the border removed

    The numpy array allows the use of slicing to more succinctly express the iteration through the border values

    This implementation is, in principle, tail recursive in the sense that the last function call (the call in tail
    position) is all the work left to do in this function.
    """
    if not isinstance(matrix, np.ndarray):
        matrix = np.array(matrix)
    if matrix.ndim != 2:
        raise ValueError("must be a 2D matrix")

    if matrix.size == 0:
        return

    # unroll outer layer
    yield from matrix[0, :]  # top
    yield from matrix[1:, -1]  # right
    if 1 in matrix.shape:  # done already if only 1 row or column
        return
    yield from matrix[-1, -2::-1]  # bottom
    yield from matrix[-2:0:-1, 0]  # left

    # strip outer layer and recurse
    yield from spiral_values_numpy_recursive(matrix[1:-1, 1:-1])


def spiral_values_numpy_iter(matrix):
    """Returns the values of the matrix in spiral order, iterative numpy version

    This re-expresses the algorithm from `spiral_values_numpy_recursive` as an iteration,
    which should protect it from stack overflow issues. Note that the logic and structure
    was worked out in the recursive version, and then ported into a while-loop formulation.

    In my opinion, analyzing the problem recursively makes it easier to see that the same
    operation is happening repeatedly to concentric layers of the matrix.
    """
    if not isinstance(matrix, np.ndarray):
        matrix = np.array(matrix)
    if matrix.ndim != 2:
        raise ValueError("must be a 2D matrix")

    while matrix.size > 0:
        yield from matrix[0, :]  # top
        yield from matrix[1:, -1]  # right

        if 1 in matrix.shape:
            return

        yield from matrix[-1, -2::-1]  # bottom
        yield from matrix[-2:0:-1, 0]  # left
        matrix = matrix[1:-1, 1:-1]  # strip outer layer


def spiral_values_numpy_rotate_recursive(matrix):
    """Returns the values of the matrix in spiral order, via recursive rotation

    A further simplification showing that the spiral values are:

      * the values from the top border
      * the spiral values from the rest of the matrix, rotated 90 degrees

    This function continually takes the top border of the matrix, rotates the
    matrix, and takes the top border again, until all values are exhausted.

    Note that the analysis and implementation is completely trivial, but only
    after translating the input matrix into a structure that lends itself to
    thinking in high-level operations on the matrix as a whole. The list of lists
    representation of the matrix does not have a rotate operation, and so leads
    one away from even thinking about this algorithm.

    Moreover, again, thinking recursively helps to find that the core operation at work.
    In a sense, this is the most straightforward expression of the spiral concept--spin
    the matrix around and shave off values as you go.
    """
    if not isinstance(matrix, np.ndarray):
        matrix = np.array(matrix)
    if matrix.ndim != 2:
        raise ValueError("must be a 2D matrix")

    if matrix.size == 0:
        return

    yield from matrix[0, :]  # top
    yield from spiral_values_numpy_rotate_recursive(np.rot90(matrix[1:, :]))


def spiral_values(matrix):
    """Returns the values of the matrix in spiral order, via iterative rotation

    Re-expression of the recursive version above into a while loop. This is the
    final version due to its simplicity. Only requiring that the input matrix be
    transformed into a numpy array.

    :see:`spiral_values_numpy_rotate_recursive` for discussion.
    """
    if not isinstance(matrix, np.ndarray):
        matrix = np.array(matrix)
    if matrix.ndim != 2:
        raise ValueError("must be a 2D matrix")

    while matrix.size > 0:
        yield from matrix[0]
        matrix = np.rot90(matrix[1:])
