"""

"""

from decimal import Decimal
import inspect
import typing

from . import constants
from .constants import Number


class Vector:
    """

    """
    triplets = {
        "rectangular": ("x", "y", "z"),
        "cylindrical": ("r", "theta", "z"),
        "spherical": ("rho", "phi", "theta")
    }

    class _Rectangular(typing.NamedTuple):
        x: Decimal
        y: Decimal
        z: Decimal

    class _Cylindrical(typing.NamedTuple):
        r: Decimal
        theta: Decimal
        z: Decimal

    class _Spherical(typing.NamedTuple):
        rho: Decimal
        phi: Decimal
        theta: Decimal

    def __init__(
            self, *,
            r: typing.Optional[Number] = None,
            x: typing.Optional[Number] = None,
            y: typing.Optional[Number] = None,
            z: typing.Optional[Number] = None,
            theta: typing.Optional[Number] = None,
            rho: typing.Optional[Number] = None,
            phi: typing.Optional[Number] = None,
    ):
        """

        :param r:
        :param x:
        :param y:
        :param z:
        :param theta:
        :param rho:
        :param phi:
        """
        local_vars = locals()
        kwargs = {k: local_vars[k] for k in inspect.signature(self.__init__).parameters}

        if [
            all(
                (v is not None) if k in t else (v is None) for k, v in kwargs.items()
            ) for t in self.triplets.values()
        ].count(True) != 1:
            params = ", ".join(map(str, self.triplets.values()))
            raise ValueError(
                f"Exactly one of {params} must be a triplet of non-null values: {kwargs}"
            )

        (
            self._r, self._x, self._y, self._z, self._theta, self._rho, self._phi
        ) = [Decimal() for _ in kwargs]

        for name, value in kwargs.items():
            self.__setattr__(
                f"_{name}", None if value is None else Decimal(str(value))
            )

    def __repr__(self):
        attributes = (f"{k.strip('_')}={self[k.strip('_')]}" for k in vars(self))
        return f"{type(self).__name__}({', '.join(attributes)})"

    def __getitem__(self, item: str) -> Decimal:
        """

        :param item:
        :return:
        """
        return self.__getattribute__(item)

    @property
    def r(self) -> Decimal:
        """

        :return:
        """
        if self._r is not None:
            return self._r
        elif None not in (self._x, self._y, self._z):
            return (self.x ** 2 + self.y ** 2).sqrt()
        elif None not in (self._rho, self._phi, self._theta):
            return self.rho * constants.sine(self.phi)

    @property
    def x(self) -> Decimal:
        """

        :return:
        """
        if self._x is not None:
            return self._x
        return self.r * constants.cosine(self.theta)

    @property
    def y(self) -> Decimal:
        """

        :return:
        """
        if self._y is not None:
            return self._y
        return self.r * constants.sine(self.theta)

    @property
    def z(self) -> Decimal:
        """

        :return:
        """
        if self._z is not None:
            return self._z
        return self.rho * constants.cosine(self.phi)

    @property
    def theta(self) -> Decimal:
        """

        :return:
        """
        if self._theta is not None:
            return self._theta
        return constants.arctangent(self.y / self.x)

    @property
    def rho(self) -> Decimal:
        """

        :return:
        """
        if self._rho is not None:
            return self._rho
        elif None not in (self._x, self._y, self._z):
            return (self.x ** 2 + self.y ** 2 + self.z ** 2).sqrt()
        elif None not in (self._r, self._theta, self._z):
            return (self.r ** 2 + self.z ** 2).sqrt()

    @property
    def phi(self) -> Decimal:
        """

        :return:
        """
        if self._phi is not None:
            return self._phi
        return constants.arctangent(self.r / self.z)

    @property
    def rectangular(self) -> _Rectangular:
        """

        :return:
        """
        return self._Rectangular(x=self.x, y=self.y, z=self.z)

    @property
    def cylindrical(self) -> _Cylindrical:
        """

        :return:
        """
        return self._Cylindrical(r=self.r, theta=self.theta, z=self.z)

    @property
    def spherical(self) -> _Spherical:
        """

        :return:
        """
        return self._Spherical(rho=self.rho, phi=self.phi, theta=self.theta)
