
"""
Wraps a callable, providing methods for composition, in either "wrapped"
or "nested" senses. Also a function-oriented reduce(), as a class method,
or a standalone function.

Functions take/return exactly one argument/value. Composition is tricky
to define otherwise. Something like "functions take/return exactly one
tuple", which isn't really an improvement.
"""


from functools import reduce as _reduce, update_wrapper as _update

_notDefined = object()


class Function(object):
    """
    Provides methods for composition, both "wrapped" other(self(t))
    and "nested" self(other(t)). Docstrings and such are passed through
    via functools.update_wrapper().

    A _strip() staticmethod is called to unwrap callables when embedding
    them into a new function. Subclasses may wish to override this be-
    havior. An additional hook is available one step higher with the
    _compose() class method."""

    def __init__(self, f):
        _update(self, f)
        self._f = f

    def __call__(self, t):
        return self._f(t)

    @property
    def func(self):
        return self._f

    @staticmethod
    def _strip(f):
        """If passed an instance, return the callable; otherwise, pass the
        argument through. A duck-typed approach is taken; any object
        with a "func" attribute will be unwrapped."""

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

    @classmethod
    def freduce(cls, op, fxns, initializer=_notDefined):
        """Like reduce(), but for functions.

        Example: freduce(op, [f, g]) returns a new instance wrapping
        lambda t: reduce(op, [f(t), g(t)])
        """

        # reify any iterator (and strip)
        fxns = tuple(map(cls._strip, fxns))

        if initializer is _notDefined:
            return cls(lambda t: _reduce(
                op, [f(t) for f in fxns]))
        else:
            return cls(lambda t: _reduce(
                op, [f(t) for f in fxns], initializer))

freduce = Function.freduce
