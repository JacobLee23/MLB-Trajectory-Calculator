"""
"""

import typing

import numpy as np

from ..coordinates import Coordinates2D
from ..coordinates import Vector2D


class Temperature:
    """
    Converts between temperature scales.
    """
    def __init__(self, value: float, unit: typing.Literal["celsius", "fahrenheit", "kelvin"]):
        self._value, self._unit = value, unit

    @property
    def celsius(self) -> float:
        r"""
        Converts to the Celsius scale (:math:`^\degree C`).
        """
        if self._unit == "celsius":
            return self._value
        elif self._unit == "fahrenheit":
            return 5 / 9 * (self._value - 32)
        elif self._unit == "kelvin":
            return self._value + 273.15
        
    @property
    def fahrenheit(self) -> float:
        r"""
        Converts to the Fahrenheit scale (:math:`^\degree F`).
        """
        if self._unit == "celsius":
            return 9 / 5 * self._value + 32
        elif self._unit == "fahrenheit":
            return self._value
        elif self._unit == "kelvin":
            return 9 / 5 * (self._value + 273.15) + 32
        
    @property
    def kelvin(self) -> float:
        r"""
        Converts to the Kelvin scale (:math:`K`).
        """
        if self._unit == "celsius":
            return self._value + 273.15
        elif self._unit == "fahrenheit":
            return 5 / 9 * (self._value - 32) + 273.15
        elif self._unit == "kelvin":
            return self._value
        else:
            return np.nan


class Wind(Vector2D):
    r"""
    Handles wind velocity.

    .. note::

        Wind direction is expressed as an angular displacement from straightaway centerfield.

    :param v_w: wind speed, :math:`{v}_{w}` (:math:`\frac{m}{s}`)
    :param phi_w: wind direction, :math:`{\phi}_{w}` (:math:`rad`)
    """
    def __init__(self, v_w: float, phi_w: float):
        super().__init__(Coordinates2D(np.array([v_w, phi_w]), "polar").cartesian)


class AirDensity:
    r"""
    .. py:attribute:: r

        Molar gas constant, :math:`R` (:math:`J * {mol}^{-1} * {K}^{-1}`).

        :type: float
    
    .. py:attribute:: m_d

        Molar mass of dry air, :math:`{M}_{d}` (:math:`\frac{kg}{mol}`).

        :type: float

    .. py:attribute:: m_v

        Molar mass of water vapor, :math:`{M}_{v}` (:math:`\frac{kg}{mol}`).

        :type: float
    """
    r = 8.31446261815324

    m_d = 0.0289652
    m_v = 0.018016

    @classmethod
    def dry_air(cls, p: float, t: float) -> float:
        r"""
        :param p: absolute pressure, :math:`p` (:math:`Pa`)
        :param t: absolute temperature, :math:`T` (:math:`K`)
        :return: air density, :math:`\rho` (:math:`\frac{kg}{{m}^{3}}`)
        """
        return p / (cls.r * t)
    
    @classmethod
    def humid_air(cls, p_d: float, p_v: float, t: float) -> float:
        """
        :param p_d: partial pressure of dry air, :math:`{p}_{d}` (:math:`Pa`)
        :param p_v: pressure of water vapor, :math:`{p}_{v}` (:math:`Pa`)
        :param t: temperature, :math:`T` (:math:`K`)
        :return:
        """
        return (p_d * cls.m_d + p_v * cls.m_v) / (cls.r * t)
    
    @classmethod
    def vapor_pressure(cls, p_sat: float, phi: float) -> float:
        """
        :param p_sat: saturation vapor pressure, :math:`{p}_{sat}`
        :param phi: relative humidity, :math:`\phi` (:math:`[0.0, 1.0]`)
        :return: vapor pressure of water, :math:`{p}_{v}`
        """
        return phi * p_sat
    
    @classmethod
    def saturation_vapor_pressure(cls, t: float) -> float:
        """
        :param t: temperature, :math:`T` (:math:`\degree C`)
        :return: saturation vapor pressure, :math:`{p}_{sat}` (:math:`hPa`)
        """
        return 6.1078 * pow(10, 7.5 * t / (t + 237.3))
