"""
.. py:data:: PROJECTILE

    Baseball dimension specifications, per the MLB Rulebook (Rule 3.01)

    :type: pd.Series
"""

import pandas as pd


PROJECTILE = pd.Series(
    {"WeightMin": 5, "WeightMax": 5.25, "CircumferenceMin": 9, "CircumferenceMax": 9.25}
)
