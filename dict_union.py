from collections import abc
from functools import reduce
from itertools import chain

class DictUnion(abc.Mapping):
    """Union of dictionaries, lazily combining values using binary function `fn`

    >>> import collections
    >>> import functools
    >>> import operator
    >>> dict_a = {'a': 1, 'b': 2, 'c': 3}
    >>> dict_b = {'a': 1,         'c': 3}
    >>> dict_c = {        'b': 4,         'd': 5}

    >>> a = DictUnion(dict_a, dict_b, dict_c, fn=operator.add)
    >>> a['b']
    6
    >>> a
    DictUnion({'a': 2, 'b': 6, 'c': 6, 'd': 5})

    __getitem__ follows its contract and raises a KeyError for missing keys

    >>> a['z']
    Traceback (most recent call last):
       ...
    KeyError: 'z'


    >>> DictUnion(dict_a, dict_b, dict_c, fn=operator.mul)
    DictUnion({'a': 1, 'b': 8, 'c': 9, 'd': 5})


    Implementing the abstract base class Mapping gives us nice stuff
    for free:

    >>> isinstance(a, collections.abc.Mapping)
    True
    >>> list(a.items())
    [('a', 2), ('b', 6), ('c', 6), ('d', 5)]
    >>> list(a.values())
    [2, 6, 6, 5]

    Particularly cute is automatic conversion to a normal dict or
    other collection type. This gets used in the __repr__
    implementation:

    >>> da = dict(a)
    >>> da
    {'a': 2, 'b': 6, 'c': 6, 'd': 5}
    >>> da.__class__
    <class 'dict'>

    Because the values are dynamically calculated, the values in
    DictUnion are obviously not mutable:

    >>> isinstance(a, collections.abc.MutableMapping)
    False
    >>> a['d'] = 10  # doctest: +ELLIPSIS
    Traceback (most recent call last):
       ...
    TypeError: ... does not support item assignment

    But saving out the result as a (mutable) dict is easy:

    >>> mut_a = dict(a)
    >>> mut_a['d']
    5
    >>> mut_a['d'] = 10
    >>> mut_a['d']
    10

    The `fn` argument comes last to support use of `functools.partial`::

    >>> dua = functools.partial(DictUnion, fn=operator.add)
    >>> a == dua(dict_a, dict_b, dict_c)
    True


    The `default` parameter provides an initial empty value for each
    value, if needed:

    >>> list_concat = lambda acc, y: acc + [y]
    >>> DictUnion(dict_a, dict_b, dict_c, fn=list_concat, default=[])
    DictUnion({'a': [1, 1], 'b': [2, 4], 'c': [3, 3], 'd': [5]})

    """
    def __init__(self, *dicts, fn, default=None):
        self._dicts = dicts
        self._fn = fn
        self._default = default

    def keys(self):
        return sorted(set(chain.from_iterable(self._dicts)))

    def __repr__(self):
        return f'{self.__class__.__name__}({dict(self)})'

    def __getitem__(self, key):
        vals = [d[key] for d in self._dicts if key in d]
        if len(vals) == 0:
            raise KeyError(key)

        if not self._default is None:
            return reduce(self._fn, vals, self._default)
        else:
            return reduce(self._fn, vals)

    def __iter__(self):
        return iter(self.keys())

    def __len__(self):
        return len(self.keys())
