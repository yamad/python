"""Decorator for deprecating default parameter values

License (BSD3):

 Copyright (c) 2019, Jason Yamada-Hanff

 All rights reserved.

 Redistribution and use in source and binary forms, with or without modification,
 are permitted provided that the following conditions are met:

     * Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer.
     * Redistributions in binary form must reproduce the above copyright notice,
       this list of conditions and the following disclaimer in the documentation
       and/or other materials provided with the distribution.
     * Neither the name of src nor the names of its contributors
       may be used to endorse or promote products derived from this software
       without specific prior written permission.

 THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
 CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
 NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

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
        def wrapped(*args, **kwargs):
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

            return func(*args, **kwargs)

        return wrapped

    return decorate
