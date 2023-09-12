"""
This module contains classes for handling mathematical coordinates.
"""

import typing

import numpy as np


class Coordinates2D:
    r"""
    Converts ordered pairs between 2-dimensional coordinate systems.

    +-------------------+-----------------------+-----------------------+
    | Coordinate System | ``coordinates[0]``    | ``coordinates[1]``    |
    +===================+=======================+=======================+
    | Cartesian         | :math:`x`             | :math:`y`             |
    +-------------------+-----------------------+-----------------------+
    | Polar             | :math:`r`             | :math:`\theta`        |
    +-------------------+-----------------------+-----------------------+

    :param coordinates: An ordered pair of real numbers
    :param system: The corresponding coordinate system name
    """
    def __init__(self, coordinates: np.ndarray, system: typing.Literal["cartesian", "polar"]):
        if coordinates.shape != (2,):
            raise ValueError

        self._coordinates, self._system = coordinates, system

    def __repr__(self) -> str:
        arguments = ", ".join(
            f"{k}={self.__getattribute__(k)}" for k in ["cartesian", "polar"]
        )
        return f"{type(self).__name__}({arguments})"

    @property
    def cartesian(self) -> np.ndarray:
        """
        Converts to the Cartesian coordinate system (:math:`x`, :math:`y`).
        """
        # (x, y)
        if self._system == "cartesian":
            return self._coordinates
        # (r, theta)
        elif self._system == "polar":
            return np.array(
                [
                    # x = r * cos(theta)
                    self._coordinates[0] * np.cos(self._coordinates[1]),
                    # y = r * sin(theta)
                    self._coordinates[0] * np.sin(self._coordinates[1])
                ]
            )
        else:
            return np.array([np.nan, np.nan])

    @property
    def polar(self) -> np.ndarray:
        r"""
        Converts to the polar coordinate system (radius :math:`r`, azimuth :math:`\phi`).
        """
        # (x, y)
        if self._system == "cartesian":
            return np.array(
                [
                    # r = sqrt(x ** 2 + y ** 2)
                    np.sqrt((self._coordinates ** 2).sum()),
                    # theta = arctan(y / x),
                    np.arctan(self._coordinates[1] / self._coordinates[0])
                ]
            )
        elif self._system == "polar":
            return self._coordinates
        else:
            return np.array([np.nan, np.nan])


class Vector2D:
    """
    Handles computations involving 2-dimensional vectors.
    """
    def __init__(self, vector: np.ndarray):
        if vector.shape != (2,):
            raise ValueError
        self._vector = vector

    def __repr__(self) -> str:
        arguments = ", ".join(f"{a}={b}" for a, b in zip(["x", "y"], self.vector))
        return f"{type(self).__name__}({arguments})"
    
    def __str__(self) -> str:
        return "<{}, {}>".format(*self.vector)

    @property
    def vector(self) -> np.ndarray:
        """
        """
        return self._vector
    
    @property
    def coordinates(self) -> Coordinates2D:
        """
        """
        return Coordinates3D(self.vector, "cartesian")
    
    @property
    def radius(self) -> float:
        """
        """
        return self.coordinates.polar[0]
    
    @property
    def azimuth(self) -> float:
        """
        """
        return self.coordinates.polar[1]


class Coordinates3D:
    r"""
    Converts ordered triplets between 3-dimensional coordinate systems.

    +-------------------+-----------------------+-----------------------+-----------------------+
    | Coordinate System | ``coordinates[0]``    | ``coordinates[1]``    | ``coordinates[2]``    |
    +===================+=======================+=======================+=======================+
    | Cartesian         | :math:`x`             | :math:`y`             | :math:`z`             |
    +-------------------+-----------------------+-----------------------+-----------------------+
    | Cylindrical       | :math:`\rho`          | :math:`\phi`          | :math:`z`             |
    +-------------------+-----------------------+-----------------------+-----------------------+
    | Spherical         | :math:`\r`            | :math:`\theta`        | :math:`\phi`          |
    +-------------------+-----------------------+-----------------------+-----------------------+

    :param coordinates: An ordered triplet of real numbers
    :param system: The corresponding coordinate system name
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
                    np.arccos(self._coordinates[2] / np.sqrt((self._coordinates ** 2).sum())),
                    # phi = sign(y) * arccos(x / sqrt(x ** 2 + y ** 2))
                    np.sign(self._coordinates[1]) * np.arccos(self._coordinates[0] / np.sqrt(self._coordinates[0] ** 2 + self._coordinates[1] ** 2))
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


class Vector3D:
    """
    Handles computations involving 3-dimensional vectors.
    """
    def __init__(self, vector: np.ndarray):
        if vector.shape != (3,):
            raise ValueError
        self._vector = vector

    def __repr__(self) -> str:
        arguments = ", ".join(f"{a}={b}" for a, b in zip(["x", "y", "z"], self.vector))
        return f"{type(self).__name__}({arguments})"
    
    def __str__(self) -> str:
        return "<{}, {}, {}>".format(*self.vector)

    @property
    def vector(self) -> np.ndarray:
        """
        """
        return self._vector
    
    @property
    def coordinates(self) -> Coordinates3D:
        """
        """
        return Coordinates3D(self.vector, "cartesian")
    
    @property
    def central_radius(self) -> float:
        """
        """
        return self.coordinates.spherical[0]
    
    @property
    def axial_radius(self) -> float:
        """
        """
        return self.coordinates.cylindrical[0]
    
    @property
    def azimuth(self) -> float:
        """
        """
        return self.coordinates.spherical[2]
    
    @property
    def elevation(self) -> float:
        """
        """
        return self.coordinates.cylindrical[1]
