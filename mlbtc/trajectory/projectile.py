"""
.. py:data:: PROJECTILE

    Baseball dimension specifications, per the MLB Rulebook (Rule 3.01)

    :type: pd.Series
"""

import pandas as pd


PROJECTILE = pd.DataFrame(
    {"weight": {"min": 5, "max": 5.25}, "circumference": {"min": 9, "max": 9.25}}
)
