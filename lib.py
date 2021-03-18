
from functools import reduce

from .base import Composable

# for friendlier introspection
notDefined = type('NotDefined', (object,), {})()


def freduce(op, fxns, initializer=notDefined, cls=Composable):
    """Like reduce(), but for functions.

    Example: freduce(op, [f, g]) returns a new instance wrapping
    lambda t: reduce(op, [f(t), g(t)])"""

    # reify any iterator (and strip)
    fxns = tuple(map(cls._strip, fxns))

    if initializer is notDefined:
        return cls(lambda t: reduce(
            op, (f(t) for f in fxns)))
    else:
        return cls(lambda t: reduce(
            op, (f(t) for f in fxns), initializer))
