
# composition updates an internal list at either end depending on nest/wrap
# simplify will go through the list and collapse any that may be combined
# reduce/condense/umm will replace the list with one function, or maybe not.
# could be just as well to keep the list?

# it seems necessary to have a method that will flag when simplification is defined
# for nest and/or wrap. It should be a two argument classmethod. Same method for
# either direction. If nest matches, go with it, if not check wrap.

# test:
# both must be Functions or a subtype

#   invocation      if True
# a.simplify(a,b)  a.nest(b)
# b.simplify(b,a)  b.wrap(a)

# simplification
# set i=0
# if elements i,i+1 simplify, replace them with the simplification
# in either case, increment i by 1
# iterate until ith element is the last element.

# it's been crazy trying to wrap my head around how to implement this. the trouble
# is actually pretty straightforward. The Function instance is trying to manage other
# instances in a sibling sort of relationship. Nutty! There needs to be a list type
# that contains the siblings and has distinct wrap/nest handling but has the same
# high-level API. The reduce/condense/umm methos will be its, and it returns a
# Function instance.

# Rename current type to "_Function"?
# Nope. List type is named "Functional"

# reduce/condense/umm should be available as a property and a method?
# something short would be nice, but also something not too terse.. uhhhh

"""
The Function class wraps a callable, providing methods for composition,
in either "wrapped" or "nested" senses. Also a function-oriented reduce(),
as a class method. It is also accessable as a standalone function.

Function instances take/return exactly one argument/value."""

from functools import reduce, update_wrapper


notDefined = object()

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

    @classmethod
    def freduce(cls, op, fxns, initializer=notDefined):
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

freduce = Function.freduce
