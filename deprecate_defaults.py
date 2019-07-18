import functools
import inspect
import warnings


def default_parameters(callable_):
    """Return set of parameter names in callable that have default values"""
    sig = inspect.signature(callable_)
    default_names = []
    for param in sig.parameters.values():
        if param.default is not param.empty:
            default_names.append(param.name)
    return set(default_names)


def deprecated_defaults(*paramnames):
    """Decorator to deprecate default parameter values

    Default values to deprecate can be listed as arguments to the
    decorator (e.g. ``@deprecated_defaults("a")``). If no parameter
    names are provided, all parameters with default values are assumed
    deprecated (e.g. ``@deprecated_defaults()``).

    The intended use of the decorator is to signal to users that they
    should provide explicit values for parameters where they did not
    have to before. This allows an API to evolve, giving users warning
    of the eventual removal of confusing default behaviors. This
    decorator *does not* deprecate parameters themselves. In fact, it
    does somewhat the opposite: making previously optional parameters
    required.

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
            unprovided = default_parameters(func) - kwargs.keys()
            deprecations = unprovided  # default to all defaults being required
            if paramnames:  # filter by provided names
                deprecations = deprecations.intersection(paramnames)

            if deprecations:
                msg = (
                    f"Default values for parameters {sorted(deprecations)} "
                    "are deprecated. Please provide explicit arguments."
                )
                warnings.warn(msg, DeprecationWarning, stacklevel=2)

            result = func(*args, **kwargs)
            return result

        return deprecated

    return decorate
