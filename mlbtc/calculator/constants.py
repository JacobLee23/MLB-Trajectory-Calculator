r"""
Contains mathematical constants and functions.

.. py:data:: PRECISION

    The number of decimal points to which :py:class:`decimal.Decimal` objects should by accurate.

.. py:data:: PI

    The Gauss-Legendre Algorithm approximation of :math:`\pi`, accurate to :py:data:`PRECISION`
    points of precision.

.. py:data:: INF

    The :py:class:`decimal.Decimal` representaiton of :math:`\infty`.

.. py:data:: NINF

    The :py:class:`decimal.Decimal` representation of :math:`-\infty`.
"""

import decimal
from decimal import Decimal
import math
import typing


# Precision
PRECISION: int = 100
decimal.getcontext().prec = PRECISION


# Numerical Constants
def gauss_legendre(
        a: Decimal = Decimal(1),
        b: Decimal = 1 / Decimal(2).sqrt(),
        t: Decimal = 1 / Decimal(4),
        p: int = 1,
        pi: Decimal = Decimal()
):
    r"""
    Approximates the value of :math:`\pi` using the Gauss-Legendre Algorithm. Computes the
    :math:`nth` iteration using the values of the :math:`(n-1)th` iteration.

    From Wikipedia (`source`_):

        1. Inital value setting:

            :math:`a_{0} = 1`,

            :math:`b_{0} = \frac{1}{\sqrt{2}}`,

            :math:`t_{0} = \frac{1}{4}`,

            :math:`p_{0} = 1`.

        2. Repeat the following instructions until the difference of :math:`a_{n}` and
        :math:`b_{n}` is within the desired accuracy:

            :math:`a_{n+1} = \frac{a_{n} + b_{n}}{2}`,

            :math:`b_{n+1} = \sqrt{a_{n}b_{n}}`,

            :math:`t_{n+1} = t_{n} - p_{n}(a_{n} - a_{n+1}) ^ {2}`,

            :math:`p_{n+1} = 2 p_{n}`.

        3. :math:`\pi` is then approximated as:

            :math:`\pi \approx \frac{(a_{n+1} + b_{n+1}) ^ {2}}{4 t_{n+1}}`.

    The default parameters ``a``, ``b``, ``t``, and ``p``correspond to the initial values
    :math:`a`, :math:`b`, :math:`t`, and :math:`p`, respectively.

    The value of :math:`\pi` is recursively calculated until the desired accuracy is obtained. (The
    desired accuracy is determined by :py:data:`PRECISION`.) In other words, :py:data:`PI` is
    accurate to :py:data:`PRECISION` decimal places.

    .. _source: https://en.wikipedia.org/wiki/Gauss%E2%80%93Legendre_algorithm

    :param a: The value of :math:`a` from the previous iteration (or the initial value)
    :param b: The value of :math:`b` from the previous iteration (or the initial value)
    :param t: The value of :math:`t` from the previous iteration (or the initial value)
    :param p: The value of :math:`p` from the previous iteration (or the initial value)
    :param pi:  The value of :math:`\pi` from the previous iteration (or the initial value)
    :return: The approximated value of :math:`\pi`
    """
    with decimal.localcontext() as ctx:
        ctx.prec = PRECISION + 2

        a_: Decimal = (a + b) / 2
        b_: Decimal = (a * b).sqrt()
        t_: Decimal = t - p * (a - a_) ** 2
        p_: int = 2 * p
        pi_: Decimal = (a_ + b_) ** 2 / (4 * t_)

        if pi == pi_:
            return pi

        return gauss_legendre(a_, b_, t_, p_, pi_)


PI = gauss_legendre()
INF = Decimal("Infinity")
NINF = Decimal("-Infinity")


# Maclaurin approximations
def _maclaurin_expansion(
        clsmeth: typing.Callable[[type, int, Decimal], Decimal]
) -> typing.Callable:
    """

    :param clsmeth:
    :return:
    """

    def wrapper(cls: type, x: Decimal) -> typing.Generator[Decimal, None, None]:
        """

        :param cls:
        :param x:
        :return:
        """
        with decimal.localcontext() as ctx:
            ctx.prec = PRECISION + 2

            n = 0
            while True:
                try:
                    term = clsmeth(cls, n, x)
                except decimal.Overflow:
                    return

                # Test for "convergence"
                if term + Decimal(1) == Decimal(1):
                    return

                yield term

                n += 1

    return wrapper


class _MaclaurinSeries:
    """

    """
    @classmethod
    @_maclaurin_expansion
    def sine(cls, n: int, x: Decimal) -> Decimal:
        r"""
        Calculates the :math:`nth` term of the Maclaurin series expansion of :math:`sin(x)`.

        :math:`a_{n} = \frac{(-1)^{n}}{(2n+1)!} x^{2n+1}`

        :param n: The number of the term within the Maclaurin series expansion
        :param x: The point at which to evaluate the Maclaurin series expansion
        :return: The value of the :math:`nth` term of the Maclaurin series expansion
        """
        return (
                Decimal((-1) ** n)
                / Decimal(math.factorial(2 * n + 1))
                * (x ** (2 * n + 1))
        )

    @classmethod
    @_maclaurin_expansion
    def cosine(cls, n: int, x: Decimal) -> Decimal:
        r"""
        Calculates the :math:`nth` term of the Maclaurin series expansion of :math:`cos(x)`.

        :math:`a_{n} = \frac{(-1)^{n}}{(2n)!} x^{2n}`

        :param n: The number of the term within the Maclaurin series expansion
        :param x: The point at which to evaluate the Maclaurin series expansion
        :return: The value of the :math:`nth` term of the Maclaurin series expansion
        """
        return (
                Decimal((-1) ** n)
                / Decimal(math.factorial(2 * n))
                * (x ** (2 * n))
        )

    @classmethod
    @_maclaurin_expansion
    def arcsine(cls, n: int, x: Decimal) -> Decimal:
        r"""
        Calculates the :math:`nth` term of the Maclaurin series expansion of :math:`arcsin(x)`.

        :math:`a_{n} = \frac{(2n)!}{4^{n}(n!)^{2}(2n+1)} x^{2n+1}`

        :param n: The number of the term within the Maclaurin series expansion
        :param x: The point at which to evaluate the Maclaurin series expansion
        :return: The value of the :math:`nth` term of the Maclaurin series expansion
        """
        return (
                Decimal(math.factorial(2 * n))
                / (
                        Decimal(4 ** n)
                        * Decimal(math.factorial(n)) ** 2
                        * Decimal(2 * n + 1)
                )
                * (x ** (2 * n + 1))
        )

    @classmethod
    @_maclaurin_expansion
    def arctangent(cls, n: int, x: Decimal) -> Decimal:
        r"""
        Calculates the :math:`nth` term of the Maclaurin series expansion of :math:`arctan(x)`.

        :math:`a_{n} = \frac{(-1)^n}{2n+1} x^{2n+1}`

        :param n: The number of the term within the Maclaurin series expansion
        :param x: The point at which to evaluate the Maclaurin series expansion
        :return: The value of the :math:`nth` term of the Maclaurin series expansion
        """
        return (
                Decimal((-1) ** n)
                / Decimal(2 * n + 1)
                * (x ** (2 * n + 1))
        )


# Trigonometric functions
def sine(x: Decimal) -> Decimal:
    r"""
    Approximates the value of :math:`sin(x)` using the Maclaurin series expansion.

    :math:`sin(x) \approx \sum_{0}^{\infty} \frac{(-1)^{n}}{(2n+1)!} x^{2n+1}`.

    .. note::

        Domain: :math:`(-\infty, +\infty)`

        Range: :math:`[-1, 1]`

    :param x:
    :return:
    """
    return sum(_MaclaurinSeries.sine(x))


def cosine(x: Decimal) -> Decimal:
    r"""
    Approximates the value of :math:`cos(x)` using the Maclaurin series expansion.

    :math:`cos(x) \approx \sum{0}^{\infty} \frac{(-1)^{n}}{(2n)!} x^{2n}`.

    .. note::

        Domain: :math:`(-\infty, +\infty)`

        Range: :math:`[1, 1]`

    :param x:
    :return:
    """
    return sum(_MaclaurinSeries.cosine(x))


def tangent(x: Decimal) -> Decimal:
    r"""
    Approximates the value of :math:`tan(x)` using the Maclaurin series expansion.

    :math:`tan(x) = \frac{sin(x)}{cos(x)}`.

    Thus, :math:`tan(x)` is computed by dividing the Maclaurin approximation of :math:`sin(x)` by
    the Maclaurin approximation of :math:`cos(x)`.

    .. note::

        Domain: :math:`\{x | x \neq \frac{\pi}{2} + \pi n\}, n \in \mathbb{Z}`

        Range: :math:`(-\infty, +\infty)`

    :param x:
    :return:
    """
    try:
        return sine(x) / cosine(x)
    except ZeroDivisionError:
        return INF if sine(x) > 0 else NINF


def secant(x: Decimal) -> Decimal:
    r"""
    Approximates the value of :math:`sec(x)` using the Maclaurin series expansion.

    :math:`sec(x) = \frac{1}{cos(x)}`.

    Thus, :math:`sec(x)` is computed by calculating the reciprocal of the Maclaurin approximation
    of :math:`cos(x)`.

    .. note::

        Domain: :math:`\{x | x \neq \frac{\pi}{2} + \pi n\}, n \in \mathbb{Z}`

        Range: :math:`(-\infty, -1] \bigcup [1, +\infty)`

    :param x:
    :return:
    """
    try:
        return 1 / cosine(x)
    except ZeroDivisionError:
        return INF if sine(x) > 0 else NINF


def cosecant(x: Decimal) -> Decimal:
    r"""
    Approximates the value of :math:`sec(x)` using the Maclaurin series expansion.

    :math:`csc(x) = \frac{1}{sin(x)}`.

    Thus, :math:`csc(x)` is computed by calculating the reciprocal of the Maclaurin approximation
    of :math:`sin(x)`.

    .. note::

        Domain: :math:`\{x | x \neq \pi n\}, n \in \mathbb{Z}`

        Range: :math:`(-\infty, -1] \bigcup [1, +\infty)`

    :param x:
    :return:
    """
    try:
        return 1 / sine(x)
    except ZeroDivisionError:
        return INF if cosine(x) > 0 else NINF


def cotangent(x: Decimal) -> Decimal:
    r"""
    Approximates the value of :math:`cot(x)` using the Maclaurin series expansion.

    :math:`tan(x) = \frac{cos(x)}{sin(x)}`.

    Thus, :math:`tan(x)` is computed by dividing the Maclaurin approximation of :math:`cos(x)` by
    the Maclaurin approximation of :math:`sin(x)`.

    .. note::

        Domain: :math:`\{x | x \neq \pi n\}, n \in \mathbb{Z}`

        Range: :math:`(-\infty, +\infty)`

    :param x:
    :return:
    """
    try:
        return cosine(x) / sine(x)
    except ZeroDivisionError:
        return INF if cosine(x) > 0 else NINF


# Inverse Trigonometric Functions
def arcsine(x: Decimal) -> Decimal:
    r"""
    Approximates the value of :math:`arcsin(x)` using the Maclaurin series expansion.

    :math:`arcsin(x) \approx \sum{0}^{\infty} \frac{(2n)!}{4^{n}(n!)^{2}(2n+1)} x^{2n+1}`.

    .. note::

        Domain: :math:`[-1, 1]`

        Range: :math:`[-\frac{\pi}{2}, \frac{\pi}{2}]`

    :param x:
    :return:
    """
    if not abs(x) <= 1:
        raise ValueError(
            "Value of argument 'x' is outside the domain of arcsin(x)"
        )
    if x == -1:
        return -PI / 2
    elif x == 1:
        return PI / 2
    else:
        return sum(_MaclaurinSeries.arcsine(x))


def arccosine(x: Decimal) -> Decimal:
    r"""
    Approximates the value of :math:`arccos(x)` using the Maclaurin series expansion.

    :math:`arccos(x) = \frac{\pi}{2} - arcsin(x)`.

    Thus, :math:`arccos(x)` is computed by subtracting the Maclaurin approximation of
    :math:`arcsin(x)` from :math:`\frac{\pi}{2}`.

    .. note::

        Domain: :math:`[-1, 1]`

        Range: :math:`[0, \pi]`

    :param x:
    :return:
    """
    if not abs(x) <= 1:
        raise ValueError(
            "Value of argument 'x' is outside the domain of arccos(x)"
        )
    if x == -1:
        return PI
    elif x == 1:
        return Decimal(0)
    else:
        return PI / 2 - arcsine(x)


def arctangent(x: Decimal) -> Decimal:
    r"""
    Approximates the value of :math:`arctan(x)` using the Maclaurin series expansion.

    :math:`arcsin(x) \approx \sum{0}^{\infty} \frac{(-1)^n}{2n+1} x^{2n+1}`.

    However, for :math:`x \in (-\infty, -1] \bigcup [1, \infty)`, :math:`arctan(x)` converges very
    slowly. Furthermore, :math:`arctan(x) = arcsin(\frac{x}{\sqrt{1+x^{2}}})`. Thus, for
    :math:`x \in (-\infty, -1] \bigcup [1, \infty)`, :math:`arctan(x)` is computed by calculating
    the Maclaurin approximation of :math:`arcsin(\frac{x}{\sqrt{1+x^{2}}})`

    .. note::

        Domain: :math:`(-\infty, +\infty)`

        Range: :math:`(-\frac{\pi}{2}, \frac{\pi}{2})`

    :param x:
    :return:
    """
    if x is INF:
        return PI / 2
    elif x is NINF:
        return -PI / 2
    elif -1 < x < 1:
        return sum(_MaclaurinSeries.arctangent(x))
    else:
        return arcsine(x / (Decimal(1) + x ** 2).sqrt())


def arcsecant(x: Decimal) -> Decimal:
    r"""
    Approximates the value of :math:`arcsec(x)` using the Maclaurin series expansion.

    :math:`arcsec(x) = arccos(\frac{1}{x}) = \frac{\pi}{2} - arcsin(\frac{1}{x})`.

    Thus, :math:`arcsec(x)` is computed by subtracting the Maclaurin approximation of
    :math:`arcsin(\frac{1}{x})` from :math:`\frac{\pi}{2}`.

    .. note::

        Domain: :math:`(-\infty, +\infty)`

        Range: :math:`(-\frac{\pi}{2}, \frac{\pi}{2})`

    :param x:
    :return:
    """
    if not abs(x) >= 1:
        raise ValueError(
            "Value of argument 'x' is outside the domain of arcsec(x)"
        )
    if x is INF:
        return PI / 2
    elif x is NINF:
        return -PI / 2
    else:
        return arccosine(1 / x)


def arccosecant(x: Decimal) -> Decimal:
    r"""
    Approximates the value of :math:`arccsc(x)` using the Maclaurin series expansion.

    :math:`arccsc(x) = arcsin(\frac{1}{x})`.

    Thus, :math:`arccsc(x)` is computed by calculating the Maclaurin approximation of
    :math:`arcsin(\frac{1}{x})`.

    .. note::

        Domain: :math:`(-\infty, +\infty)`

        Range: :math:`(0, \pi)`

    :param x:
    :return:
    """
    if not abs(x) >= 1:
        raise ValueError(
            "Value of argument 'x' is outside the domain of arccsc(x)"
        )
    if x is INF:
        return Decimal(0)
    elif x is NINF:
        return PI
    else:
        return arcsine(1 / x)


def arccotangent(x: Decimal) -> Decimal:
    r"""
    Approximates the value of :math:`arccot(x)` using the Maclaurin series expansion.

    :math:`arccot(x) = arcsin(\frac{1}{\sqrt{x^{2}+1}}) = arctan(\frac{1}{x})`.

    Thus, :math:`arccot(x)` is computed by calculating the Maclaurin approximation of
    :math:`arctan(\frac{1}{x})`.

    .. note::

        Domain: :math:`(-\infty, +\infty)`

        Range: :math:`(0, \pi)`

    :param x:
    :return:
    """
    if x is INF:
        return Decimal(0)
    elif x is NINF:
        return PI
    else:
        return arctangent(1 / x)
