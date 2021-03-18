
"""
The Composable class wraps a callable, providing methods for composition.
Composable instances take/return exactly one argument/value."""

from functools import update_wrapper


class Composable:
    """
    Provides methods for composition, both "wrapped" other(self(t))
    and "nested" self(other(t)). Docstrings and such are passed through
    via functools.update_wrapper().

    Shift operators are overridden such that the operator points to the outer
    function, i.e. f >> g is g(f) and f << g is f(g), in a manner analogous to
    shell redirection.

    A _strip() staticmethod is called to unwrap callables when embedding
    them into a new function. Subclasses may wish to override this be-
    havior. An additional hook is available one step higher with the
    _compose() class method."""

    def __init__(self, f):
        update_wrapper(self, f)
        self._f = f

    def __call__(self, t):
        return self._f(t)

    @property
    def func(self):
        return self._f

    @staticmethod
    def _strip(f):
        """If passed an instance, return the callable; otherwise, pass the
        argument through. A duck-typed approach is taken: any object
        with a "func" attribute will be stripped down to that attribute."""

        return f.func if hasattr(f, 'func') else f

    @classmethod
    def _compose(cls, f, g):
        """Returns a new instance wrapping the composition f(g(t)), after
        stripping the arguments."""

        f = cls._strip(f)
        g = cls._strip(g)

        return cls(lambda t: f(g(t)))

    def nest(self, other):
        """self(other(t))"""
        return self._compose(self, other)

    def wrap(self, other):
        """other(self(t))"""
        return self._compose(other, self)

    def __lshift__(self, other):
        """self << other"""
        return self._compose(self, other)

    def __rshift__(self, other):
        """self >> other"""
        return self._compose(other, self)

    def __rlshift__(self, other):
        """other << self"""
        return self._compose(other, self)

    def __rrshift__(self, other):
        """other >> self"""
        return self._compose(self, other)
