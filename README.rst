Function instances take/return exactly one argument/value.

Composition is tricky to define otherwise. Something like "functions take/return exactly one tuple", which isn't really an improvement.

Arbitrary args and kwargs can be used at every level, but they will only apply to the innermost function.

Arbitrary positional arguments can work throughout, if all functions comply with the convention, but it's equivalent to tuples. Keyword arguments might be added by having a unit of exchange that was a tuple of (args,kwargs)

::

    >>> from composable import Composable
    >>> f=Composable(lambda x:x+1)
    >>> g=Composable(lambda x:4*x)
    >>> h=Composable(lambda x:2**x)
    >>> h(g(f(1)))
    256
    >>> f(g(h(1)))
    9
    >>> (f|g|h)(1)
    256
    >>> 1|f|g|h
    256
