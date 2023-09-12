"""
.. py:data:: PROJECTILE

    Baseball dimension specifications, per the MLB Rulebook (Rule 3.01)

    :type: pd.DataFrame
"""

import pandas as pd

from ..coordinates import Vector3D


PROJECTILE = pd.DataFrame(
    {"weight": {"min": 5, "max": 5.25}, "circumference": {"min": 9, "max": 9.25}}
)


class Acceleration(Vector3D):
    """
    """


class Velocity(Vector3D):
    """
    """


class Position(Vector3D):
    """
    """
