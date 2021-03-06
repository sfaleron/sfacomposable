
Extensible Function Composition
===============================

Sample Session
--------------
::

    >>> from sfacomposable import Composable, strip
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
    >>> class Foo(Composable):
    ...     pass
    ...
    >>> class Bar(Composable):
    ...     _new = Foo
    ...
    >>> hFoo=Foo(h)
    >>> hBar=Bar(h)
    >>> type(strip(h))
    <class 'function'>
    >>> type(strip(hFoo))
    <class 'function'>
    >>> 1|f|g|hFoo
    256
    >>> 1|f|g|hBar
    256
    >>> type(f|g|hFoo).__name__
    'Foo'
    >>> type(f|g|hBar).__name__
    'Foo'

Also available as a (silent) doctest_::

    >>> import doctest
    >>> import sfacomposable
    >>> doctest.testmod(sfacomposable.base)
    TestResults(failed=0, attempted=18)
    >>> if not _.failed: print('Success!')
    ...
    Success!

See Also
--------

toolz_: "A functional standard library for Python"

compose_: "The classic ``compose``, with all the Pythonic features"

.. _doctest: https://docs.python.org/3/library/doctest.html
.. _toolz: https://github.com/pytoolz/toolz
.. _compose: https://github.com/mentalisttraceur/python-compose
