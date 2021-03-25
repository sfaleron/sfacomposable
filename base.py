# Copyright 2021 Christopher Fuller
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
    and "nested" self(other(t)).

    Composition can be customized by overloading the method _compose(). The
    default behavior is to use the module-level compose() function.

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
    """Wraps a callable passed to the constructor, or the identity function,
    if none is provided. Docstrings and such are passed through via
    functools.update_wrapper().

    The provided callable can be accessed via the strip() function. Customi-
    zation of how instances are stripped can be done by overloading the
    attribute "_stripped".

    TypeError is raised if the object passed is not callable. Ability to
    accept a single argument is not validated.

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
