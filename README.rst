
**Extensible Function Composition**

Sample session::

    >>> from sfacomposable import Composable
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

Also available as a (silent) doctest_ on the `command line`_::

    $ python -m sfacomposable.tests
    Testing..
    Success!

.. _doctest: https://docs.python.org/3/library/doctest.html
.. _command line: https://docs.python.org/3/using/cmdline.html#cmdoption-m


See also packages Polynomial and Wavegen.
