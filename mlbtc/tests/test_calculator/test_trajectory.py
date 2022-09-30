"""
Tests for :py:mod:`mlbtc.calculator.trajectory`.
"""

from decimal import Decimal
import inspect

from mlbtc.calculator import trajectory
from mlbtc.calculator import constants
from mlbtc.calculator.constants import PI
from mlbtc.calculator.constants import Number

import pytest


@pytest.mark.parametrize(
    "r, x, y, z, theta, rho, phi", [
        (
                Decimal(2).sqrt(), Decimal(1), Decimal(1), Decimal(1), PI / Decimal(4),
                Decimal(3).sqrt(), constants.arctangent(Decimal(2).sqrt())
        ),
        (
                Decimal(5), Decimal(3), Decimal(4), Decimal(12),
                constants.arctangent(Decimal(4) / Decimal(3)), Decimal(13),
                constants.arctangent(Decimal(5) / Decimal(12))
        ),
        (
                Decimal(20), Decimal(12), Decimal(16), Decimal(21),
                constants.arctangent(Decimal(4) / Decimal(3)), Decimal(29),
                constants.arctangent(Decimal(20) / Decimal(21))
        )
    ]
)
def test_vector_3d(
        r: Number, x: Number, y: Number, z: Number, theta: Number, rho: Number, phi: Number
):
    """
    Unit tests for :py:class:`mlbtc.calculator.trajectory.Vector3D`.
    """
    arguments = {k: Decimal(v) for k, v in locals().items()}
    for system in trajectory.Vector3D.systems:
        vector = trajectory.Vector3D(
            system(
                **{k: arguments[k] for k in inspect.signature(system).parameters}
            )
        )

        for key in arguments:
            assert float(vector[key]) == pytest.approx(
                float(arguments[key])
            ), (system, key, vector)
