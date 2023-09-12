"""
"""

import typing

import numpy as np


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
