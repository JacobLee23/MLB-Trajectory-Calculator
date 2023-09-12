"""
"""

import datetime
import json
import re

import bs4
import pandas as pd
import requests

from ..coordinates import Vector3D


class DragCoefficient:
    """
    Baseball drag coefficient data by season (<source `https://baseballsavant.mlb.com/drag-dashboard`>).
    """
    _url = "https://baseballsavant.mlb.com/drag-dashboard"
    _regex = re.compile(r"^const serverVals = (.*);$")

    def __init__(self):
        with requests.get(self._url, timeout=100) as response:
            soup = bs4.BeautifulSoup(response.text, features="lxml")
        self._data = json.loads(
            self._regex.search(
                str(soup.select_one("div.article-template > script").text.strip())
            ).group(1)
        )

    @property
    def binned_data(self) -> pd.DataFrame:
        """
        """
        dataframe = pd.DataFrame(self._data["binnedData"])
        dataframe.columns = ["Year", "CD", "TotalPitches", "n", "freq"]
        return dataframe
    
    @property
    def scatter_data(self) -> pd.DataFrame:
        """
        """
        dataframe = pd.DataFrame(self._data["scatterData"])
        dataframe.columns=["Date", "n", "Games", "MeanCD"]
        dataframe.loc[:, "Date"] = dataframe.loc[:, "Date"].apply(
            lambda x: datetime.datetime.strptime(x["value"], "%Y-%m-%d")
        )
        return dataframe


class DragForce(Vector3D):
    r"""
    :param rho: density of the fluid, :math:`\rho`
    :param v: velocity of the projectile relative to the fluid, :math:`v`
    :param a: cross-sectional area of the projectile, :math:`A`
    :param c_d: the drag coefficient of the projectile in the fluid, :math:`{C}_{d}`
    """
    def __init__(self, rho: float, v: Vector3D, a: float, c_d: float):
        super().__init__(rho * v ** 2 * c_d * a / 2)
