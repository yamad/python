import functools
import inspect
import warnings

def default_parameters(callable_):
    """Return set of parameter names with default values for callable"""
    sig = inspect.signature(callable_)
    default_names = []
    for param in sig.parameters.values():
        if param.default is not param.empty:
            default_names.append(param.name)
    return set(default_names)


def deprecated_defaults(*paramnames):
    """Decorator to deprecate default values for parameters

    Defaults to deprecate are listed as strings as arguments to the
    decorator (e.g. ``@deprecated_defaults("a")``). If no parameter
    names are provided, all parameters with default values are assumed
    deprecated (e.g. ``@deprecated_defaults()``).

    The intended use of the decorator is to signal to users that they
    should provide explicit values for parameters where they did not
    necessarily have to before. Thus, an API can evolve, users are
    warned, and confusing default behaviors are ultimately
    removed. This decorator *does not* deprecate parameters,

    For example, to require arguments for ``b``, ``c``, and
    ``d`` in ``foo``::

        @deprecated_defaults()
        def foo(a, b=None, c=None, d=None):
            return 1

    Alternatively, you can specify subsets::

        @deprecated_defaults("b")
        def foo...

        @deprecated_defaults("b", "c")
        def foo...

    After one or more releases with the deprecation in place, the
    signature can eventually become::

        def foo(a, b, c, d):
            return 1

    or::

        def foo(a, *, b, c, d):
            return 1

    """
    def decorate(func):
        @functools.wraps(func)
        def deprecated(*args, **kwargs):
            defaults = default_parameters(func)
            unprovided = default_parameters(func) - kwargs.keys()
            deprecations = unprovided  # default to all defaults being required
            if paramnames:             # filter by provided names
                deprecations = deprecations.intersection(paramnames)

            if deprecations:
                names = list(deprecations)
                names.sort()
                msg = (f"Default values for parameters {names} are deprecated. "
                       "Please provide explicit arguments.")
                warnings.warn(msg, DeprecationWarning, stacklevel=2)

            result = func(*args, **kwargs)
            return result
        return deprecated
    return decorate
