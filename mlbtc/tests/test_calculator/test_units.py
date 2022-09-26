"""
Tests for :py:mod:`mlbtc.calculator.base_units`.
"""

from decimal import Decimal

import pytest

from mlbtc.calculator import units
from mlbtc.calculator.constants import Number


@pytest.mark.parametrize(
    "inch, foot, meter, mile, yard", [
        (0, 0, 0, 0, 0),
        (
                1, Decimal("1") / Decimal("12"), Decimal("2.54") / Decimal("100"),
                Decimal("1") / Decimal("63360"), Decimal("1") / Decimal("36")
        ),
        (
                10, Decimal("5") / Decimal("6"), Decimal("25.4") / Decimal("100"),
                Decimal("1") / Decimal("6336"), Decimal("5") / Decimal("18")
        )
    ]
)
def test_length(
        inch: Number, foot: Number, meter: Number, mile: Number, yard: Number
):
    """
    Unit tests for :py:class:`mlbtc.calculator.base_units.Length`.
    """
    arguments = {k: Decimal(v) for k, v in locals().items()}
    for unit, value in arguments.items():
        x = units.Length(**{unit: value})

        for key in arguments:
            assert float(x[key]) == float(arguments[key]), x


@pytest.mark.parametrize(
    "celsius, fahrenheit, kelvin", [
        (-40, -40, Decimal("233.15")),
        (0, 32, Decimal("273.15")),
        (25, 77, Decimal("298.15")),
        (50, 122, Decimal("323.15")),
        (75, 167, Decimal("348.15")),
        (100, 212, Decimal("373.15")),
    ]
)
def test_temperature(
        celsius: Number, fahrenheit: Number, kelvin: Number
):
    """
    Unit tests for :py:class:`mlbtc.calculator.base_units.Temperature`.
    """
    arguments = {k: Decimal(v) for k, v in locals().items()}
    for unit, value in arguments.items():
        x = units.Temperature(**{unit: value})

        for key in arguments:
            assert float(x[key]) == float(arguments[key]), x


@pytest.mark.parametrize(
    "gram, ounce, pound, ton_uk, ton_us", [
        (
                Decimal("28.349523125"), 1, Decimal("1") / Decimal("16"),
                Decimal("1") / Decimal("35840"), Decimal("1") / Decimal("32000")
        ),
        (
                Decimal("28.349523125") * 16, 16, 1,
                Decimal("1") / Decimal("2240"), Decimal("1") / Decimal("2000")
        )
    ]
)
def test_mass(
        gram: Number, ounce: Number, pound: Number, ton_uk: Number, ton_us: Number
):
    """
    Unit tests for :py:class:`mlbtc.calculator.base_units.Mass`.
    """
    arguments = {k: Decimal(v) for k, v in locals().items()}
    for unit, value in arguments.items():
        x = units.Mass(**{unit: value})

        for key in arguments:
            assert float(x[key]) == float(arguments[key]), x
