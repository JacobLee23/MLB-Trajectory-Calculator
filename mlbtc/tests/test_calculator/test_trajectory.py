"""
Tests for :py:mod:`mlbtc.calculator.trajectory`.
"""

from decimal import Decimal

from mlbtc.calculator import trajectory
from mlbtc.calculator import constants
from mlbtc.calculator.constants import PI
from mlbtc.calculator.constants import Number

import pytest


@pytest.mark.parametrize(
    "r, x, y, z, theta, rho, phi", [
        (
                Decimal(2).sqrt(), 1, 1, 1, PI / Decimal(4), Decimal(3).sqrt(),
                constants.arctangent(Decimal(2).sqrt())
        ),
        (
                5, 3, 4, 12, constants.arctangent(Decimal(4) / Decimal(3)), 13,
                constants.arctangent(Decimal(5) / Decimal(12))
        ),
        (
                20, 12, 16, 21, constants.arctangent(Decimal(4) / Decimal(3)), 29,
                constants.arctangent(Decimal(20) / Decimal(21))
        )
    ]
)
def test_vector(
        r: Number, x: Number, y: Number, z: Number, theta: Number, rho: Number, phi: Number
):
    """
    Unit tests for :py:class:`mlbtc.calculator.trajectory.Vector`.
    """
    arguments = {k: Decimal(v) for k, v in locals().items()}
    for system, triplet in trajectory.Vector.triplets.items():
        vector = trajectory.Vector(**{k: v for k, v in arguments.items() if k in triplet})

        for key in arguments:
            assert float(vector[key]) == pytest.approx(
                float(arguments[key])
            ), (system, key, vector)
