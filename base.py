
"""
The Composable class wraps a callable, providing methods for composition.
Composable instances take/return exactly one argument/value."""

from functools import update_wrapper


def strip(f):
    """
    Extract the function wrapped by the Composable instance. Can be
    overridden, see the Composable docstring for details."""

    if hasattr(f, '_stripped'):
        return f._stripped
    else:
        return f


def compose_base(*f):
    """Composition without processing. Bare functions in, bare function out.
    """

    def builder(seq):
        if len(seq) == 1:
            return 'f[{:d}](t)'.format(seq[0])
        else:
            return 'f[{:d}]({})'.format(seq[0], builder(seq[1:]))

    if   len(f) == 0:
        return lambda t: t
    elif len(f) == 1:
        return f[0]
    else:
        return eval('lambda t: ' + builder(range(len(f))), dict(f=f), {})


def compose(*f):
    """Returns a new Composable instance wrapping the composition, after
    stripping (as needed) the arguments."""

    return Composable(compose_base(*map(strip, f)))


# Could mixin with a class with callable instances
class ComposableBase:
    """
    Provides methods for composition, both "wrapped" other(self(t))
    and "nested" self(other(t)). Docstrings and such are passed through
    via functools.update_wrapper().

    Composition can be customized by overloading the method _compose(). The
    default behavior is to use the module-level compose() function

    The or operator is overloaded to implement "piping" in the manner familiar
    to shell users. Non-callable arguments at the front of the pipeline are
    passed to the function and evaluated in the expected manner."""

    @staticmethod
    def _compose(f, g):
        return compose(f, g)

    def nest(self, other):
        """self(other(t))"""
        return self._compose(self, other)

    def wrap(self, other):
        """other(self(t))"""
        return self._compose(other, self)

    def __or__(self, other):
        """other(self(t))"""
        return self._compose(other, self)

    def __ror__(self, other):
        """self(other(t))"""
        if callable(other):
            return self._compose(self, other)
        else:
            return self(other)



class Composable(ComposableBase):
    """
    If the constructor is not passed a callable, the identity function is
    used.

    TypeError is raised if the object passed is not callable. Ability to
    accept a single argument is not validated.

    >>> from composable import Composable
    >>> f=Composable(lambda x:x+1)
    >>> g=Composable(lambda x:4*x)
    >>> @Composable
    ... def h(x):
    ...     return 2**x
    ...
    >>> h(g(f(1)))
    256
    >>> f(g(h(1)))
    9
    >>> (f|g|h)(1)
    256
    >>> 1|f|g|h
    256
    """

    @property
    def _stripped(self):
        """Fixed attributes are allowed. Conserves space moreso than computation,
        however. To disable, delete or assign self to the attribute."""

        return self.__wrapped__

    def __init__(self, f=None):
        if f is None:
            f = lambda x: x

        if not callable(f):
            raise TypeError('Pass a callable (that can be invoked as f(arg)), or pass nothing for the identity function.')

        update_wrapper(self, f)

    def __call__(self, t):
        return self.__wrapped__(t)
