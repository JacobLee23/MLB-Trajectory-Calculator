"""

"""

from decimal import Decimal
import typing


class Temperature:
    """

    """

    def __init__(
            self, *,
            celsius: typing.Optional[float] = None,
            fahrenheit: typing.Optional[float] = None,
            kelvin: typing.Optional[float] = None,
    ):
        """

        :param celsius:
        :param fahrenheit:
        :param kelvin:
        """
        if [x is not None for x in (celsius, fahrenheit, kelvin)].count(True) != 1:
            raise ValueError(
                "Exactly one of 'celsius', 'fahrenheit', 'kelvin' must be non-null"
            )

        self._c, self._f, self._k = None, None, None

        if celsius is not None:
            self._c = Decimal(str(celsius))
        if fahrenheit is not None:
            self._f = Decimal(str(fahrenheit))
        if kelvin is not None:
            self._k = Decimal(str(kelvin))

    def __repr__(self) -> str:
        args = [
            f"celsius={float(self.celsius)}",
            f"fahrenheit={float(self.fahrenheit)}",
            f"kelvin={float(self.kelvin)}"
        ]
        return f"Temperature({', '.join(args)})"

    @property
    def celsius(self) -> Decimal:
        """

        :return:
        """
        if self._c is not None:
            return self._c
        elif self._f is not None:
            return Decimal("5") / Decimal("9") * (self._f - Decimal("32"))
        elif self._k is not None:
            return self._k - Decimal("273.15")
        else:
            raise ValueError

    @property
    def fahrenheit(self) -> Decimal:
        """

        :return:
        """
        if self._c is not None:
            return Decimal("9") / Decimal("5") * self._c + Decimal("32")
        elif self._f is not None:
            return self._f
        elif self._k is not None:
            return Decimal("9") / Decimal("5") * (self._k - Decimal("273.15")) + Decimal("32")
        else:
            raise ValueError

    @property
    def kelvin(self) -> Decimal:
        """

        :return:
        """
        if self._c is not None:
            return self._c + Decimal("273.15")
        elif self._f is not None:
            return Decimal("5") / Decimal("9") * (self._f - Decimal("32")) + Decimal("273.15")
        elif self._k is not None:
            return self._k
        else:
            raise ValueError

    @property
    def si(self) -> Decimal:
        """

        :return:
        """
        return self.celsius
