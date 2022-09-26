"""
Tests for :py:mod:`mlbtc.calculator.environment`.
"""

import pytest

from mlbtc.calculator import environment


@pytest.mark.parametrize(
    "x, c, f, k", [
        (environment.Temperature(celsius=-40), -40, -40, 233.15),
        (environment.Temperature(fahrenheit=-40), -40, -40, 233.15),
        (environment.Temperature(kelvin=233.15), -40, -40, 233.15),

        (environment.Temperature(celsius=0), 0, 32, 273.15),
        (environment.Temperature(fahrenheit=32), 0, 32, 273.15),
        (environment.Temperature(kelvin=273.15), 0, 32, 273.15),

        (environment.Temperature(celsius=25), 25, 77, 298.15),
        (environment.Temperature(fahrenheit=77), 25, 77, 298.15),
        (environment.Temperature(kelvin=298.15), 25, 77, 298.15),

        (environment.Temperature(celsius=50), 50, 122, 323.15),
        (environment.Temperature(fahrenheit=122), 50, 122, 323.15),
        (environment.Temperature(kelvin=323.15), 50, 122, 323.15),

        (environment.Temperature(celsius=75), 75, 167, 348.15),
        (environment.Temperature(fahrenheit=167), 75, 167, 348.15),
        (environment.Temperature(kelvin=348.15), 75, 167, 348.15),

        (environment.Temperature(celsius=100), 100, 212, 373.15),
        (environment.Temperature(fahrenheit=212), 100, 212, 373.15),
        (environment.Temperature(kelvin=373.15), 100, 212, 373.15),
    ]
)
def test_temperature(x: environment.Temperature, c: float, f: float, k: float):
    """

    :param x:
    :param c:
    :param f:
    :param k:
    :return:
    """
    assert float(x.celsius) == c, x
    assert float(x.fahrenheit) == f, x
    assert float(x.kelvin) == k, x
