"""
Tests for :py:mod:`mlbtc.calculator.base_units`.
"""

import pytest

from mlbtc.calculator import base_units


@pytest.mark.parametrize(
    "x, c, f, k", [
        (base_units.Temperature(celsius=-40), -40, -40, 233.15),
        (base_units.Temperature(fahrenheit=-40), -40, -40, 233.15),
        (base_units.Temperature(kelvin=233.15), -40, -40, 233.15),

        (base_units.Temperature(celsius=0), 0, 32, 273.15),
        (base_units.Temperature(fahrenheit=32), 0, 32, 273.15),
        (base_units.Temperature(kelvin=273.15), 0, 32, 273.15),

        (base_units.Temperature(celsius=25), 25, 77, 298.15),
        (base_units.Temperature(fahrenheit=77), 25, 77, 298.15),
        (base_units.Temperature(kelvin=298.15), 25, 77, 298.15),

        (base_units.Temperature(celsius=50), 50, 122, 323.15),
        (base_units.Temperature(fahrenheit=122), 50, 122, 323.15),
        (base_units.Temperature(kelvin=323.15), 50, 122, 323.15),

        (base_units.Temperature(celsius=75), 75, 167, 348.15),
        (base_units.Temperature(fahrenheit=167), 75, 167, 348.15),
        (base_units.Temperature(kelvin=348.15), 75, 167, 348.15),

        (base_units.Temperature(celsius=100), 100, 212, 373.15),
        (base_units.Temperature(fahrenheit=212), 100, 212, 373.15),
        (base_units.Temperature(kelvin=373.15), 100, 212, 373.15),
    ]
)
def test_temperature(x: base_units.Temperature, c: float, f: float, k: float):
    """
    Unit tests for :py:class:`mlbtc.calculator.base_units.Temperature`.
    """
    assert float(x.celsius) == c, x
    assert float(x.fahrenheit) == f, x
    assert float(x.kelvin) == k, x
