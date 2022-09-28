"""

"""

import decimal
from decimal import Decimal
import typing


Number = typing.Union[int, float, Decimal]


def gauss_legendre(precision: int = 100) -> Decimal:
    """

    :param precision:
    :return:
    """
    with decimal.localcontext() as ctx:
        ctx.prec = precision + 1

        # Initial value setting
        a: Decimal = Decimal(1)
        b: Decimal = 1 / Decimal(2).sqrt(ctx)
        t: Decimal = 1 / Decimal(4)
        p: int = 1
        pi: Decimal = Decimal()

        # (n + 1)th values
        a_: Decimal
        b_: Decimal
        t_: Decimal
        p_: int
        pi_: Decimal

        while True:
            a_ = (a + b) / 2
            b_ = (a * b).sqrt(ctx)
            t_ = t - p * (a - a_) ** 2
            p_ = 2 * p
            pi_ = (a_ + b_) ** 2 / (4 * t_)

            if pi == pi_:
                return pi

            a, b, t, p, pi = a_, b_, t_, p_, pi_


PI = gauss_legendre()
