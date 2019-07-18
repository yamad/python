import pytest
import warnings

from deprecate_defaults import deprecated_defaults

warnings.simplefilter("always")  # make sure DeprecationWarnings are issued


def test_deprecate_all_defaults():
    def undecorated(a, b=None, c=1, d="string"):
        return 1

    @deprecated_defaults()
    def decorated(a, b=None, c=1, d="string"):
        return 1

    assert undecorated("dummy") == 1
    with pytest.warns(DeprecationWarning, match=r"'b', 'c', 'd'"):
        assert decorated("dummy") == 1
    with pytest.warns(DeprecationWarning, match=r"'b', 'd'"):
        assert decorated("dummy", c=1) == 1
    with pytest.warns(DeprecationWarning, match=r"'c', 'd'"):
        assert decorated("dummy", b="something") == 1
    with pytest.warns(DeprecationWarning, match=r"'c'"):
        assert decorated("dummy", b="something", d="else") == 1


def test_deprecate_one():
    @deprecated_defaults("b")
    def foo(b=1, c=2):
        return 1

    with pytest.warns(DeprecationWarning, match=r"'b'"):
        assert foo() == 1
    assert foo(b=2) == 1
    assert foo(b=2, c=1) == 1


def test_deprecate_nonkw_is_noop():
    @deprecated_defaults("a")
    def foo(a, b=2):
        return 1

    assert foo(5) == 1
