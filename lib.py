
from functools import reduce

from .base import Composable

# for friendlier introspection
_notDefined = type('NotDefined', (object,), {})()


def pam_reduce(op, fxns, *, initializer=_notDefined, cls=Composable):
    """Reduce on the inverse of a map: a single value applied to many functions.

    Example: pam_reduce(op, [f, g]) returns a new Composable wrapping
    lambda t: reduce(op, [f(t), g(t)])"""

    # reify any iterator (and strip)
    fxns = tuple(map(cls._strip, fxns))

    if initializer is _notDefined:
        return cls(lambda t: reduce(
            op, (f(t) for f in fxns)))
    else:
        return cls(lambda t: reduce(
            op, (f(t) for f in fxns), initializer))
