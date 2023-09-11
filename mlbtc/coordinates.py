"""
"""

import typing

import numpy as np


class Coordinates3D:
    r"""
    +-------------------+-----------------------+-----------------------+-----------------------+
    | Coordinate System | ``coordinates[0]``    | ``coordinates[1]``    | ``coordinates[2]``    |
    +===================+=======================+=======================+=======================+
    | Cartesian         | :math:`x`             | :math:`y`             | :math:`z`             |
    +-------------------+-----------------------+-----------------------+-----------------------+
    | Cylindrical       | :math:`\rho`          | :math:`\phi`          | :math:`z`             |
    +-------------------+-----------------------+-----------------------+-----------------------+
    | Spherical         | :math:`\r`            | :math:`\theta`        | :math:`\phi`          |
    +-------------------+-----------------------+-----------------------+-----------------------+

    :param coordinates:
    :param system:
    """
    def __init__(self, coordinates: np.ndarray, system: typing.Literal["cartesian", "cylindrical", "spherical"]):
        if coordinates.shape != (3,):
            raise ValueError
        
        self._coordinates, self._system = coordinates, system

    def __repr__(self) -> str:
        arguments = ", ".join(
            f"{k}={self.__getattribute__(k)}" for k in ["cartesian", "cylindrical", "spherical"]
        )
        return f"{type(self).__name__}({arguments})"

    @property
    def cartesian(self) -> np.ndarray:
        """
        Converts to the Cartesian coordinate system (:math:`x`, :math:`y`, :math:`z`).
        """
        # (x, y, z)
        if self._system == "cartesian":
            return self._coordinates
        # (rho, phi, z)
        elif self._system == "cylindrical":
            return np.array(
                [
                    # x = rho * cos(phi)
                    self._coordinates[0] * np.cos(self._coordinates[1]),
                    # y = rho * sin(phi)
                    self._coordinates[0] * np.sin(self._coordinates[1]),
                    # z = z
                    self._coordinates[2]
                ]
            )
        # (r, theta, phi)
        elif self._system == "spherical":
            return np.array(
                [
                    # x = r * sin(theta) * cos(phi)
                    self._coordinates[0] * np.sin(self._coordinates[1]) * np.cos(self._coordinates[2]),
                    # y = r * sin(theta) * sin(phi)
                    self._coordinates[0] * np.sin(self._coordinates[1]) * np.sin(self._coordinates[2]),
                    # z = r * cos(theta)
                    self._coordinates[0] * np.cos(self._coordinates[1])
                ]
            )
        else:
            return np.array([np.nan, np.nan, np.nan])
        
    @property
    def cylindrical(self) -> np.ndarray:
        r"""
        Converts to the cylindrical coordinate system (axial radius :math:`\rho`, azimuth
        :math:`\phi`, elevation :math:`z`).
        """
        # (x, y, z)
        if self._system == "cartesian":
            return np.array(
                [
                    # rho = sqrt(x ** 2 + y ** 2)
                    np.sqrt(self._coordinates[0] ** 2 + self._coordinates[1] ** 2),
                    # phi = arctan(y / x)
                    np.arctan(self._coordinates[1] / self._coordinates[0]),
                    # z = z
                    self._coordinates[2]
                ]
            )
        # (rho, phi, z)
        elif self._system == "cylindrical":
            return self._coordinates
        # (r, theta, phi)
        elif self._system == "spherical":
            return np.array(
                [
                    # rho = r * sin(theta)
                    self._coordinates[0] * np.sin(self._coordinates[1]),
                    # phi = phi
                    self._coordinates[2],
                    # z = r * cos(theta)
                    self._coordinates[0] * np.cos(self._coordinates[1])
                ]
            )
        else:
            return np.array([np.nan, np.nan, np.nan])
        
    @property
    def spherical(self) -> np.ndarray:
        r"""
        Converts to the spherical coordinate system (central radius :math:`r`, inclination
        :math:`\theta`, azimuth :math:`\phi`).
        """
        # (x, y, z)
        if self._system == "cartesian":
            return np.array(
                [
                    # r = sqrt(x ** 2 + y ** 2 + z ** 2)
                    np.sqrt((self._coordinates ** 2).sum()),
                    # theta = arccos(z / sqrt(x ** 2 + y ** 2 + z ** 2))
                    np.arccos(
                        self._coordinates[2] / np.sqrt((self._coordinates ** 2).sum())
                    ),
                    # phi = sign(y) * arccos(x / sqrt(x ** 2 + y ** 2))
                    np.sign(self._coordinates[1]) * np.arccos(
                        self._coordinates[0] / np.sqrt(
                            self._coordinates[0] ** 2 + self._coordinates[1] ** 2
                        )
                    )
                ]
            )
        # (rho, phi, z)
        elif self._system == "cylindrical":
            return np.array(
                [
                    # r = sqrt(rho ** 2 + z ** 2)
                    np.sqrt(self._coordinates[0] * 2 + self._coordinates[2] ** 2),
                    # theta = arctan(rho / z)
                    np.arctan(self._coordinates[0] / self._coordinates[2]),
                    # phi = phi
                    self._coordinates[1]
                ]
            )
        # (r, theta, phi)
        elif self._system == "spherical":
            return self._coordinates
        else:
            return np.array([np.nan, np.nan, np.nan])
