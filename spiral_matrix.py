"""
1x1
[
    [ 1 ],
]

2x2
[
    [1, 2],
    [4, 3]
]

3x3
[
    [1, 2, 3],
    [8, 9, 4],
    [7, 6, 5],
]

4x4
[
   [ 1, 2, 3, 4],
   [12,13,14, 5],
   [11,16,15, 6],
   [10, 9, 8, 7],
]

[1, 1], [1, 2], [2, 2], [2, 1]
"""

from itertools import chain, repeat


def border_indices(n):
    if n == 1:
        return [tuple([0, 0])]

    # counters
    countup   = range(n-1)
    countdown = range(n-1, 0, -1)
    first     = repeat(0, n-1)
    last      = repeat(n-1, n-1)

    # edges
    top    = zip(first,     countup)
    right  = zip(countup,   last)
    bottom = zip(last,      countdown)
    left   = zip(countdown, first)
    return chain(top, right, bottom, left)

def spiral_matrix(n):
    """Fill n x n matrix with values from 1 to n^2 in spiral order
    """
    result = [[0]*n for _ in range(n)]
    val = 1
    for step, n_ in enumerate(range(n, 0, -2)):
        for row, col in border_indices(n_):
            result[row+step][col+step] = val
            val += 1
    return result

import numpy as np


def border_indices(n: int, offset: int = 0):
    """Generate (row, col) indices for clockwise border of an n x n matrix

    top    right  bottom  left
    |12 |  |  3|  |   |   |   |
    |   |  |  4|  |   |   |8  |
    |   |  |   |  | 65|   |7  |
    """
    if n < 1:
        raise ValueError
    if n == 1:
        return np.array([0]) + offset, np.array([0]) + offset

    countup = np.arange(0, n-1)
    countdown = np.arange(n-1, 0, -1)
    first = np.repeat(0, n-1)
    last = np.repeat(n-1, n-1)

    #           top      right    bottom     left
    col = np.r_[countup, last,    countdown, first    ]
    row = np.r_[first,   countup, last,      countdown]
    return row + offset, col + offset

def border_indices3(m: int, n: int, offset: int = 0):
    """Generate (row, col) indices for clockwise border of an m x n matrix
    """
    if n < 1 or m < 1:
        raise ValueError
    if n == 1 and m == 1:
        return np.array([0]) + offset, np.array([0]) + offset

    # top   = np.c_[np.arange(n),        np.repeat(0, n-1)]
    # right = np.c_[np.repeat(n-1, m-1), np.

    #           top           right           bottom                 left
    col = np.r_[np.arange(n-1),    np.repeat(n-1, m-1), np.arange(n-1, 0, -1), np.repeat(0, m-1)]
    row = np.r_[np.repeat(0, n-1), np.arange(m-1),      np.repeat(m-1, n-1),     np.arange(m-1, 0, -1)]
    return row + offset, col + offset


def spiral_indices_recursive(m: int, n: int, offset: int = 0):
    """Generate (row, col) indices for clockwise border of an m x n matrix

    top    right  bottom  left
    |12 |  |  3|  |   |   |   |
    |   |  |  4|  |   |   |8  |
    |   |  |   |  | 65|   |7  |
    """
    if n < 1 or m < 1:
        return np.array([]), np.array([])
    if n == 1 and m == 1:
        return np.array([0]) + offset, np.array([0]) + offset

    #           top                right                bottom                 left
    row = np.r_[np.repeat(0, n-1), np.arange(m-1),      np.repeat(m-1, n-1),   np.arange(m-1, 0, -1)]
    col = np.r_[np.arange(n-1),    np.repeat(n-1, m-1), np.arange(n-1, 0, -1), np.repeat(0, m-1)]

    row += offset
    col += offset

    row_recurse, col_recurse = spiral_indices_recursive(m-2, n-2, offset+1)

    row = np.r_[row, row_recurse]
    col = np.r_[col, col_recurse]
    return row, col

def spiral_indices2(n: int):
    edge_lengths = range(n, 0, -2)

    row = []
    col = []
    for step, edge_length in enumerate(edge_lengths):
        r, c = border_indices(edge_length, step)
        row.append(r)
        col.append(c)

    return np.concatenate(row), np.concatenate(col)

def spiral_matrix2(n):
    mat = np.empty(((n, n)))
    mat[spiral_indices2(n)] = np.arange(n*n) + 1
    return mat

from typing import Any, Iterable, List

def inclusive_range(start=None, stop=None, step=None):
    if start is None and stop is None:
        raise ValueError("must provide at least one of start and stop")

    if start is None:
        start = 0

    if stop is None:
        stop = start

    if step is None:
        step = 1

    return range(start, stop+1, step)


def spiral_values(matrix: List[List[Any]]) -> Iterable[Any]:
    for _, j, i in spiral_indices(matrix):
        yield matrix[j][i]


def spiral_indices(matrix: List[List[Any]]) -> Iterable[Any]:
    m = len(matrix)
    if m == 0:
        return

    n = len(matrix[0])

    # define concentric rectangles to visit
    xstarts, xstops = range(0, n//2 + 1), reversed(range(n//2, n))
    ystarts, ystops = range(0, m//2 + 1), reversed(range(m//2, m))
    layers = zip(xstarts, xstops, ystarts, ystops)

    for i, (xstart, xstop, ystart, ystop) in enumerate(layers):
        for i in range(xstart, xstop+1): # top
            yield f"t{i}", ystart, i

        for j in range(ystart+1, ystop+1): # right
            yield f"r{i}", j, xstop

        if xstart == xstop or ystart == ystop: # handle single row or column
            break

        for i in reversed(range(xstart, xstop)): # bottom
            yield f"b{i}", ystop, i

        for j in reversed(range(ystart+1, ystop)): # left
            yield f"l{i}", j, xstart


def spiral_values_numpy(matrix):
    if not isinstance(matrix, np.ndarray):
        matrix = np.array(matrix)

    if matrix.size == 0:
        return

    if 1 in matrix.shape:
        yield from matrix.flat
        return

    # unroll outer layer
    yield from matrix[0,:-1]    # top
    yield from matrix[:-1,-1]   # right
    yield from matrix[-1,:0:-1] # bottom
    yield from matrix[:0:-1, 0] # left

    # strip outer layer and recurse
    yield from spiral_values_numpy(matrix[1:-1, 1:-1])


def spiral_values_numpy_iter(matrix):
    if not isinstance(matrix, np.ndarray):
        matrix = np.array(matrix)

    while matrix.size > 0:
        # handle cases where 0 and -1 index the same elements
        if 1 in matrix.shape:
            yield from matrix.flat
            return

        yield from matrix[0,:]        # top
        yield from matrix[1:,-1]      # right
        yield from matrix[-1, -2::-1] # bottom
        yield from matrix[-2:0:-1, 0] # left
        matrix = matrix[1:-1, 1:-1]   # strip outer layer

def spiral_values_numpy_gen1(matrix):
    if not isinstance(matrix, np.ndarray):
        matrix = np.array(matrix)

    if matrix.size == 0:
        return

    yield from matrix[0,:] # top
    yield from spiral_values_numpy_gen1(np.rot90(matrix[1:,:]))



def spiral_values_numpy_gen(matrix):
    if not isinstance(matrix, np.ndarray):
        matrix = np.array(matrix)

    while matrix.size > 0:
        yield from matrix[0, :]
        matrix = np.rot90(matrix[1:])
