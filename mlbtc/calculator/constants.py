"""

"""

import decimal
from decimal import Decimal
import math
import typing

# Type definitions
Number = typing.Union[int, float, Decimal]


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
    """

    :param a:
    :param b:
    :param t:
    :param p:
    :param pi:
    :return:
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
def _maclaurin_approximation(
        clsmeth: typing.Callable[[type, int, Decimal], Decimal]
) -> typing.Callable:
    """

    :param clsmeth:
    :return:
    """

    def wrapper(cls: type, x: Decimal) -> Decimal:
        """

        :param cls:
        :param x:
        :return:
        """
        with decimal.localcontext() as ctx:
            ctx.prec = PRECISION + 2

            res: Decimal = Decimal()
            res_: Decimal

            n = 0
            while True:
                try:
                    res_ = res + clsmeth(cls, n, x)
                except decimal.Overflow:
                    return res

                if res == res_:
                    return res

                res = res_
                n += 1

    return wrapper


class _MaclaurinSeries:
    """

    """
    @classmethod
    @_maclaurin_approximation
    def sine(cls, n: int, x: Decimal) -> Decimal:
        """

        :param n:
        :param x:
        :return:
        """
        return (
                Decimal((-1) ** n)
                / Decimal(math.factorial(2 * n + 1))
                * (x ** (2 * n + 1))
        )

    @classmethod
    @_maclaurin_approximation
    def cosine(cls, n: int, x: Decimal) -> Decimal:
        """

        :param n:
        :param x:
        :return:
        """
        return (
                Decimal((-1) ** n)
                / Decimal(math.factorial(2 * n))
                * (x ** (2 * n))
        )

    @classmethod
    @_maclaurin_approximation
    def arcsine(cls, n: int, x: Decimal) -> Decimal:
        """

        :param n:
        :param x:
        :return:
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
    @_maclaurin_approximation
    def arctangent(cls, n: int, x: Decimal) -> Decimal:
        """

        :param n:
        :param x:
        :return:
        """
        return (
                Decimal((-1) ** n)
                / Decimal(2 * n + 1)
                * (x ** (2 * n + 1))
        )


# Trigonometric functions
def sine(x: Decimal) -> Decimal:
    """

    :param x:
    :return:
    """
    return _MaclaurinSeries.sine(x)


def cosine(x: Decimal) -> Decimal:
    """

    :param x:
    :return:
    """
    return _MaclaurinSeries.cosine(x)


def tangent(x: Decimal) -> Decimal:
    """

    :param x:
    :return:
    """
    try:
        return sine(x) / cosine(x)
    except ZeroDivisionError:
        return INF if sine(x) > 0 else NINF


def secant(x: Decimal) -> Decimal:
    """

    :param x:
    :return:
    """
    try:
        return 1 / cosine(x)
    except ZeroDivisionError:
        return INF if sine(x) > 0 else NINF


def cosecant(x: Decimal) -> Decimal:
    """

    :param x:
    :return:
    """
    try:
        return 1 / sine(x)
    except ZeroDivisionError:
        return INF if cosine(x) > 0 else NINF


def cotangent(x: Decimal) -> Decimal:
    """

    :param x:
    :return:
    """
    try:
        return cosine(x) / sine(x)
    except ZeroDivisionError:
        return INF if cosine(x) > 0 else NINF


# Inverse Trigonometric Functions
def arcsine(x: Decimal) -> Decimal:
    """

    :param x:
    :return:
    """
    if not abs(x) <= 1:
        raise ValueError(
            "Value of argument 'x' is outside the domain of arcsin(x): [-1, 1]"
        )
    if x == -1:
        return -PI / 2
    elif x == 1:
        return PI / 2
    else:
        return _MaclaurinSeries.arcsine(x)


def arccosine(x: Decimal) -> Decimal:
    """

    :param x:
    :return:
    """
    if not abs(x) <= 1:
        raise ValueError(
            "Value of argument 'x' is outside the domain of arccos(x): [-1, 1]"
        )
    if x == -1:
        return PI
    elif x == 1:
        return Decimal(0)
    else:
        return PI / 2 - arcsine(x)


def arctangent(x: Decimal) -> Decimal:
    """

    :param x:
    :return:
    """
    if x is INF:
        return PI / 2
    elif x is NINF:
        return -PI / 2
    elif -1 < x < 1:
        return _MaclaurinSeries.arctangent(x)
    else:
        return arcsine(x / (Decimal(1) + x ** 2).sqrt())


def arcsecant(x: Decimal) -> Decimal:
    """

    :param x:
    :return:
    """
    if not abs(x) >= 1:
        raise ValueError(
            "Value of argument 'x' is outside the domain of arcsec(x): (-inf, -1] U [1, inf)"
        )
    if x is INF:
        return PI / 2
    elif x is NINF:
        return -PI / 2
    else:
        return arccosine(1 / x)


def arccosecant(x: Decimal) -> Decimal:
    """

    :param x:
    :return:
    """
    if not abs(x) >= 1:
        raise ValueError(
            "Value of argument 'x' is outside the domain of arccsc(x): (-inf, -1] U [1, inf)"
        )
    if x is INF:
        return Decimal(0)
    elif x is NINF:
        return PI
    else:
        return arcsine(1 / x)


def arccotangent(x: Decimal) -> Decimal:
    """

    :param x:
    :return:
    """
    if x is INF:
        return Decimal(0)
    elif x is NINF:
        return PI
    else:
        return arctangent(1 / x)
