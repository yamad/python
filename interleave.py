
from itertools import zip_longest

def interleave2(*iterables):
    iters = [iter(x) for x in iterables]
    while iters:
        for it in list(iters):
            try:
                yield next(it)
            except StopIteration:
                iters.remove(it)

def interleave(*iterables):
    dummy = object()
    for items in zip_longest(*iterables, fillvalue=dummy):
        for item in items:
            if item is not dummy:
                yield item

def test_numbers_basic():
    numbers = [1, 2, 3, 4]
    res = interleave(numbers, range(5, 9))
    assert list(res) == [1, 5, 2, 6, 3, 7, 4, 8]

def test_numbers_basic2():
    numbers = [1, 2, 3, 4]
    res = interleave(numbers, (n**2 for n in numbers))
    assert list(res) == [1, 1, 2, 4, 3, 9, 4, 16]


def test_numbers_iterator():
    i = interleave([1,2,3,4], [5,6,7,8])
    assert next(i) == 1
    assert list(i) == [5, 2, 6, 3, 7, 4, 8]

def test_three_args():
    expected = [1, 4, 7, 2, 5, 8, 3, 6, 9]
    actual = interleave([1,2,3], [4,5,6], [7,8,9])
    assert list(actual) == expected

def test_unequal_lengths():
    actual = interleave([1, 2, 3], [4, 5, 6, 7, 8])
    expected = [1, 4, 2, 5, 3, 6, 7, 8]
    assert list(actual) == expected

def test_different_length_lists():
    in1 = [1, 2, 3]
    in2 = [4, 5, 6, 7, 8]
    in3 = [9]
    out1 = [1, 4, 9, 2, 5, 3, 6, 7, 8]
    assert list(interleave(in1, in2, in3)) == out1


def test_different_length_lists2():
    actual = interleave([1, 2], [3], [4, 5, 6], [7, 8], [9])
    expected = [1, 3, 4, 7, 9, 2, 5, 8, 6]
    assert list(actual) == expected
