
Extensible Function Composition
===============================

Sample Session
--------------
::

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

Also available as a (silent) doctest_::

    >>> import doctest
    >>> import sfacomposable
    >>> doctest.testmod(sfacomposable.base)
    TestResults(failed=0, attempted=8)
    >>> if not _.failed: print('Success!')
    ...
    Success!

See Also
--------

toolz_: A functional standard library for Python

.. _doctest: https://docs.python.org/3/library/doctest.html
.. _toolz: https://github.com/pytoolz/toolz

