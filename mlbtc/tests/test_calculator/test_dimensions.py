"""
Tests for :py:mod:`mlbtc.calculator.dimensions`.
"""

from decimal import Decimal

import pytest

from mlbtc.calculator import dimensions
from mlbtc.calculator.constants import Number
from mlbtc.calculator.constants import PI


@pytest.mark.parametrize(
    "degree, radian, revolution", [
        (0, 0, 0),
        (Decimal(90), PI / Decimal(2), Decimal(1) / Decimal(4)),
        (Decimal(180), PI, Decimal(1) / Decimal(2)),
        (Decimal(270), Decimal(3) * PI / Decimal(2), Decimal(3) / Decimal(4)),
        (Decimal(360), Decimal(2) * PI, Decimal(1))
    ]
)
def test_angle(
        degree: Number, radian: Number, revolution: Number
):
    """
    Unit tests for :py:class:`mlbtc.calculator.dimensions.Angle`.
    """
    arguments = {k: Decimal(v) for k, v in locals().items()}
    units = {k.name: k for k in dimensions.Angle.units}
    for unit, value in arguments.items():
        x = dimensions.Angle(value, units[unit])

        for key in arguments:
            assert float(x[key]) == float(arguments[key]), (unit, key, x)


@pytest.mark.parametrize(
    "foot, inch, meter, mile, yard", [
        (0, 0, 0, 0, 0),
        (
                1,
                12,
                # ft * (in / ft) * (cm / in) / (cm / m)
                Decimal(1) * Decimal(12) * Decimal("2.54") / Decimal(100),
                # ft / (ft / mi)
                Decimal(1) / Decimal(5280),
                # ft / (ft / yd)
                Decimal(1) / Decimal(3)
        ),
        (
                # in / (in / ft)
                Decimal(1) / Decimal(12),
                1,
                # in * (cm / in) / (cm / m)
                Decimal("2.54") / Decimal(100),
                # in / (in / mi)
                Decimal(1) / Decimal(63360),
                # in / (in / yd)
                Decimal(1) / Decimal(36)
        ),
        (
                # m * (cm / m) / (cm / in) / (in / ft)
                Decimal(1) * Decimal(100) / Decimal("2.54") / Decimal(12),
                # m * (cm / m) / (cm / in)
                Decimal(1) * Decimal(100) / Decimal("2.54"),
                1,
                # m * (cm / m) / (cm / in) / (in / mi)
                Decimal(1) * Decimal(100) / Decimal("2.54") / Decimal(63360),
                # m * (cm / m) / (cm / in) / (in / yd)
                Decimal(1) * Decimal(100) / Decimal("2.54") / Decimal(36)
        ),
        (
                5280,
                63360,
                # mi * (in / mi) * (cm / in) / (cm / m)
                Decimal(1) * Decimal(63360) * Decimal("2.54") / Decimal(100),
                1,
                1760
        ),
        (
                3,
                36,
                Decimal(36) * Decimal("2.54") / Decimal(100),
                Decimal(1) / Decimal(1760),
                1
        )
    ]
)
def test_length(
        foot: Number, inch: Number, meter: Number, mile: Number, yard: Number
):
    """
    Unit tests for :py:class:`mlbtc.calculator.dimensions.Length`.
    """
    arguments = {k: Decimal(v) for k, v in locals().items()}
    units = {k.name: k for k in dimensions.Length.units}
    for unit, value in arguments.items():
        x = dimensions.Length(value, units[unit])

        for key in arguments:
            assert float(x[key]) == float(arguments[key]), (unit, key, x)


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
    Unit tests for :py:class:`mlbtc.calculator.dimensions.Temperature`.
    """
    arguments = {k: Decimal(v) for k, v in locals().items()}
    units = {k.name: k for k in dimensions.Temperature.units}
    for unit, value in arguments.items():
        x = dimensions.Temperature(value, units[unit])

        for key in arguments:
            assert float(x[key]) == float(arguments[key]), (unit, key, x)


@pytest.mark.parametrize(
    "gram, ounce, pound, ton_uk, ton_us", [
        (0, 0, 0, 0, 0),
        (
                Decimal("28.349523125"),
                1,
                Decimal(1) / Decimal(16),
                Decimal(1) / Decimal(35840),
                Decimal(1) / Decimal(32000)
        ),
        (
                Decimal("28.349523125") * 16,
                16,
                1,
                Decimal(1) / Decimal(2240),
                Decimal(1) / Decimal(2000)
        )
    ]
)
def test_mass(
        gram: Number, ounce: Number, pound: Number, ton_uk: Number, ton_us: Number
):
    """
    Unit tests for :py:class:`mlbtc.calculator.dimensions.Mass`.
    """
    arguments = {k: Decimal(v) for k, v in locals().items()}
    units = {v.name: v for v in dimensions.Mass.units}
    for unit, value in arguments.items():
        x = dimensions.Mass(value, units[unit])

        for key in arguments:
            assert float(x[key]) == float(arguments[key]), (unit, key, x)


@pytest.mark.parametrize(
    "foot_per_second, kilometer_per_hour, meter_per_second, mile_per_hour", [
        (Decimal(0), Decimal(0), Decimal(0), Decimal(0)),
        (
                Decimal(1),
                # (ft / s) * (in / ft) * (cm / in) / (cm / km) * (s / h)
                Decimal(1) * Decimal(12) * Decimal("2.54") / Decimal(100000) * Decimal(3600),
                # (ft / s) * (in / ft) * (cm / in) / (cm / m)
                Decimal(1) * Decimal(12) * Decimal("2.54") / Decimal(100),
                # (ft / s) * (s / h) / (ft / mi)
                Decimal(1) * Decimal(3600) / Decimal(5280)
        ),
        (
                # (km / h) * (cm / km) / (cm / in) / (in / ft) / (s / h)
                Decimal(1) * Decimal(100000) / Decimal("2.54") / Decimal(12) / Decimal(3600),
                Decimal(1),
                # (km / h) * (m / km) / (s / h)
                Decimal(1) * Decimal(1000) / Decimal(3600),
                # (km / h) * (cm / km) / (cm / in) / (in / ft) * (ft / mi)
                Decimal(1) * Decimal(100000) / Decimal("2.54") / Decimal(12) / Decimal(5280)
        ),
        (
                # (m / s) / (cm / in) / (ft / in)
                Decimal(1) * Decimal(100) / Decimal("2.54") / Decimal(12),
                # (m / s) / (m / km) * (s / h)
                Decimal(1) / Decimal(1000) * Decimal(3600),
                Decimal(1),
                # (m / s) * (s / h) * (cm / m) / (in / m) / (in / ft) / (ft / mi)
                Decimal(1) * Decimal(3600) * Decimal(100) / Decimal("2.54") / Decimal(12) / Decimal(5280)
        ),
        (
                # (mi / h) * (ft / mi) / (s / h)
                Decimal(1) * Decimal(5280) / Decimal(3600),
                # (mi / h) * (ft / mi) * (in / ft) * (cm / in) / (cm / km)
                Decimal(1) * Decimal(5280) * Decimal(12) * Decimal("2.54") / Decimal(100000),
                # (mi / h) * (ft / mi) * (in / ft) * (cm / in) / (cm / m) / (c / h)
                Decimal(1) * Decimal(5280) * Decimal(12) * Decimal("2.54") / Decimal(100) / Decimal(3600),
                Decimal(1)
        )
    ]
)
def test_velocity(
        foot_per_second: Number, kilometer_per_hour: Number, meter_per_second: Number,
        mile_per_hour: Number
):
    """
    Unit tests for :py:class:`mlbtc.calculator.dimensions.Velocity`.
    """
    arguments = {k: Decimal(v) for k, v in locals().items()}
    units = {v.name: v for v in dimensions.Velocity.units}
    for unit, value in arguments.items():
        x = dimensions.Velocity(value, units[unit])

        for key in arguments:
            assert float(x[key]) == float(arguments[key]), (unit, key, x)


@pytest.mark.parametrize(
    """foot_per_second_per_second,
    kilometer_per_hour_per_second,
    meter_per_second_per_second,
    mile_per_hour_per_second""", [
        (Decimal(0), Decimal(0), Decimal(0), Decimal(0)),
        (
                Decimal(1),
                # (ft / (s ^ 2)) * (in / ft) * (cm / in) / (cm / km) * (s / h)
                Decimal(1) * Decimal(12) * Decimal("2.54") / Decimal(100000) * Decimal(3600),
                # (ft / (s ^ 2)) * (in / ft) * (cm / in) / (cm / m)
                Decimal(1) * Decimal(12) * Decimal("2.54") / Decimal(100),
                # (ft / (s ^ 2)) * (s / h) / (ft / mi)
                Decimal(1) * Decimal(3600) / Decimal(5280)
        ),
        (
                # (km / h / s) * (cm / km) / (cm / in) / (in / ft) / (s / h)
                Decimal(1) * Decimal(100000) / Decimal("2.54") / Decimal(12) / Decimal(3600),
                Decimal(1),
                # (km / h / s) * (m / km) / (s / h)
                Decimal(1) * Decimal(1000) / Decimal(3600),
                # (km / h / s) * (cm / km) / (cm / in) / (in / ft) * (ft / mi)
                Decimal(1) * Decimal(100000) / Decimal("2.54") / Decimal(12) / Decimal(5280)
        ),
        (
                # (m / (s ^ 2)) / (cm / in) / (ft / in)
                Decimal(1) * Decimal(100) / Decimal("2.54") / Decimal(12),
                # (m / (s ^ 2)) / (m / km) * (s / h)
                Decimal(1) / Decimal(1000) * Decimal(3600),
                Decimal(1),
                # (m / (s ^ 2)) * (s / h) * (cm / m) / (in / m) / (in / ft) / (ft / mi)
                Decimal(1) * Decimal(3600) * Decimal(100) / Decimal("2.54") / Decimal(12) / Decimal(5280)
        ),
        (
                # (mi / h / s) * (ft / mi) / (s / h)
                Decimal(1) * Decimal(5280) / Decimal(3600),
                # (mi / h / s) * (ft / mi) * (in / ft) * (cm / in) / (cm / km)
                Decimal(1) * Decimal(5280) * Decimal(12) * Decimal("2.54") / Decimal(100000),
                # (mi / h / s) * (ft / mi) * (in / ft) * (cm / in) / (cm / m) / (c / h)
                Decimal(1) * Decimal(5280) * Decimal(12) * Decimal("2.54") / Decimal(100) / Decimal(3600),
                Decimal(1)
        )
    ]
)
def test_velocity(
        foot_per_second_per_second: Number, kilometer_per_hour_per_second: Number,
        meter_per_second_per_second: Number, mile_per_hour_per_second: Number
):
    """
    Unit tests for :py:class:`mlbtc.calculator.dimensions.Acceleration`.
    """
    arguments = {k: Decimal(v) for k, v in locals().items()}
    units = {v.name: v for v in dimensions.Acceleration.units}
    for unit, value in arguments.items():
        x = dimensions.Acceleration(value, units[unit])

        for key in arguments:
            print(key)
            assert float(x[key]) == float(arguments[key]), (unit, key, x)
