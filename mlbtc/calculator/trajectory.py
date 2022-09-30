"""

"""

from decimal import Decimal
import typing

from . import constants


class _Vector:
    """

    """
    systems: list[typing.NamedTuple, ...]

    def __init__(
            self,
            coordinates: typing.NamedTuple,
    ):
        """

        :param coordinates:
        """
        if any(v is None for v in coordinates._asdict().values()):
            raise ValueError(
                f"Argument 'coordinates' must be a sequence of non-null values: {coordinates}"
            )

        self._coordinates = self._coord = coordinates

    def __repr__(self):
        return f"{type(self).__name__}(coordinates={self._coordinates})"

    def __getitem__(self, item: str) -> Decimal:
        """

        :param item:
        :return:
        """
        return self.__getattribute__(item)


class Vector2D(_Vector):
    """

    """
    class Rectangular(typing.NamedTuple):
        x: Decimal
        y: Decimal

    class Polar(typing.NamedTuple):
        r: Decimal
        theta: Decimal

    systems = [Rectangular, Polar]

    @property
    def r(self) -> Decimal:
        if isinstance(self._coord, self.Rectangular):
            return (self._coord.x ** 2 + self._coord.y ** 2).sqrt()
        elif isinstance(self._coord, self.Polar):
            return self._coord.r

    @property
    def x(self) -> Decimal:
        """

        :return:
        """
        if isinstance(self._coord, self.Rectangular):
            return self._coord.x
        elif isinstance(self._coord, self.Polar):
            return self._coord.r * constants.cosine(self._coord.theta)

    @property
    def y(self) -> Decimal:
        """

        :return:
        """
        if isinstance(self._coord, self.Rectangular):
            return self._coord.y
        elif isinstance(self._coord, self.Polar):
            return self._coord.r * constants.sine(self._coord.theta)

    @property
    def theta(self) -> Decimal:
        """

        :return:
        """
        if isinstance(self._coord, self.Rectangular):
            return constants.arctangent(self._coord.y / self._coord.x)
        elif isinstance(self._coord, self.Polar):
            return self._coord.theta


class Vector3D(_Vector):
    """

    """
    class Rectangular(typing.NamedTuple):
        x: Decimal
        y: Decimal
        z: Decimal

    class Cylindrical(typing.NamedTuple):
        r: Decimal
        theta: Decimal
        z: Decimal

    class Spherical(typing.NamedTuple):
        rho: Decimal
        phi: Decimal
        theta: Decimal

    systems = [Rectangular, Cylindrical, Spherical]

    @property
    def r(self) -> Decimal:
        """

        :return:
        """
        if isinstance(self._coord, self.Rectangular):
            return (self.x ** 2 + self.y ** 2).sqrt()
        elif isinstance(self._coord, self.Cylindrical):
            return self._coord.r
        elif isinstance(self._coord, self.Spherical):
            return self.rho * constants.sine(self.phi)

    @property
    def x(self) -> Decimal:
        """

        :return:
        """
        if isinstance(self._coord, self.Rectangular):
            return self._coord.x
        elif isinstance(self._coord, (self.Cylindrical, self.Spherical)):
            return self.r * constants.cosine(self.theta)

    @property
    def y(self) -> Decimal:
        """

        :return:
        """
        if isinstance(self._coord, self.Rectangular):
            return self._coord.y
        elif isinstance(self._coord, (self.Cylindrical, self.Spherical)):
            return self.r * constants.sine(self.theta)

    @property
    def z(self) -> Decimal:
        """

        :return:
        """
        if isinstance(self._coord, (self.Rectangular, self.Cylindrical)):
            return self._coord.z
        elif isinstance(self._coord, self.Spherical):
            return self.rho * constants.cosine(self.phi)

    @property
    def phi(self) -> Decimal:
        """

        :return:
        """
        if isinstance(self._coord, self.Rectangular):
            return constants.arctangent((self.x ** 2 + self.y ** 2).sqrt() / self.z)
        elif isinstance(self._coord, self.Cylindrical):
            return constants.arctangent(self.r / self.z)
        elif isinstance(self._coord, self.Spherical):
            return self._coord.phi

    @property
    def rho(self) -> Decimal:
        """

        :return:
        """
        if isinstance(self._coord, self.Rectangular):
            return (self.x ** 2 + self.y ** 2 + self.z ** 2).sqrt()
        elif isinstance(self._coord, self.Cylindrical):
            return (self.r ** 2 + self.z ** 2).sqrt()
        elif isinstance(self._coord, self.Spherical):
            return self._coord.rho

    @property
    def theta(self) -> Decimal:
        """

        :return:
        """
        if isinstance(self._coord, self.Rectangular):
            return constants.arctangent(self.y / self.x)
        elif isinstance(self._coord, (self.Cylindrical, self.Spherical)):
            return self._coord.theta

    @property
    def rectangular(self) -> Rectangular:
        """

        :return:
        """
        return self.Rectangular(x=self.x, y=self.y, z=self.z)

    @property
    def cylindrical(self) -> Cylindrical:
        """

        :return:
        """
        return self.Cylindrical(r=self.r, theta=self.theta, z=self.z)

    @property
    def spherical(self) -> Spherical:
        """

        :return:
        """
        return self.Spherical(rho=self.rho, phi=self.phi, theta=self.theta)
