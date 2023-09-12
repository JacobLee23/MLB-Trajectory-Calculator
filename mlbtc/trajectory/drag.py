"""
.. py:data:: DRAG_COEFFICIENT

    Estimated mean baseball drag coefficient by season
    (<source `https://baseballsavant.mlb.com/drag-dashboard`>).

    :type: pd.Series
"""

import numpy as np
import pandas as pd


DRAG_COEFFICIENT = pd.Series(
    {
        2016: 0.3461, 2017: 0.3346, 2018: 0.3374, 2019: 0.3279, 2020: 0.3410, 2021: 0.3410,
        2022: 0.3467, 2023: 0.3406
    }
)
