"""

"""

from decimal import Decimal
import inspect
import typing

from .constants import Number


class MetricPrefixes:
    """

    """
    yotta = Y = Decimal("1E+24")
    zetta = Z = Decimal("1E+21")
    exa = E = Decimal("1E+18")
    peta = P = Decimal("1E+15")
    tera = T = Decimal("1E+12")
    giga = G = Decimal("1E+9")
    mega = M = Decimal("1E+6")
    kilo = k = Decimal("1E+3")
    hecto = h = Decimal("1E+2")
    deka = da = Decimal("1E+1")

    deci = d = Decimal("1E-1")
    centi = c = Decimal("1E-2")
    milli = m = Decimal("1E-3")
    micro = mu = Decimal("1E-6")
    nano = n = Decimal("1E-9")
    pico = p = Decimal("1E-12")
    femto = f = Decimal("1E-15")
    atto = a = Decimal("1E-18")
    zepto = z = Decimal("1E-21")
    yocto = y = Decimal("1E-24")


class Unit:
    """

    """
    def __init__(self, **kwargs):
        """

        :param kwargs:
        """
        if [x is not None for x in kwargs.values()].count(True) != 1:
            raise ValueError(
                f"Exactly one of {', '.join(f'{x}' for x in kwargs)} must be non-null"
            )

        for name, value in kwargs.items():
            self.__setattr__(
                f"_{name}",
                None if value is None else Decimal(str(value))
            )

    def __repr__(self):
        attributes = (f"{k}={self[k]}" for k in vars(self))
        return f"{self.__name__}({', '.join(attributes)})"

    def __getitem__(self, item: str) -> Decimal:
        """

        :param item:
        :return:
        """
        return self.__getattribute__(item)


class Length(Unit):
    """

    """
    def __init__(
            self, *,
            inch: typing.Optional[Number] = None,
            foot: typing.Optional[Number] = None,
            meter: typing.Optional[Number] = None,
            mile: typing.Optional[Number] = None,
            yard: typing.Optional[Number] = None
    ):
        """

        :param inch:
        :param foot:
        :param meter:
        :param mile:
        :param yard:
        """
        local_vars = locals()
        kwargs = {k: local_vars[k] for k in inspect.signature(self.__init__).parameters}

        (
            self._inch, self._foot, self._meter, self._mile, self._yard
        ) = [Decimal() for _ in kwargs]

        super().__init__(**kwargs)

    @property
    def inch(self) -> Decimal:
        """

        :return:
        """
        if self._inch is not None:
            return self._inch
        elif self._foot is not None:
            return self.foot * Decimal("12")
        elif self._meter is not None:
            return self.meter / MetricPrefixes.c / Decimal("2.54")
        elif self._mile is not None:
            return self.mile * Decimal("5280") * Decimal("12")
        elif self._yard is not None:
            return self.yard * Decimal("3") * Decimal("12")

    @property
    def foot(self) -> Decimal:
        """

        :return:
        """
        if self._foot is not None:
            return self._foot
        else:
            return self.inch / Decimal("12")

    @property
    def meter(self) -> Decimal:
        """

        :return:
        """
        if self._meter is not None:
            return self._meter
        else:
            return self.inch * Decimal("2.54") * MetricPrefixes.c

    @property
    def mile(self) -> Decimal:
        """

        :return:
        """
        if self._mile is not None:
            return self._mile
        else:
            return self.inch / Decimal("12") / Decimal("5280")

    @property
    def yard(self) -> Decimal:
        """

        :return:
        """
        if self._yard is not None:
            return self._yard
        else:
            return self.inch / Decimal("12") / Decimal("3")


class Temperature(Unit):
    """

    """

    def __init__(
            self, *,
            celsius: typing.Optional[Number] = None,
            fahrenheit: typing.Optional[Number] = None,
            kelvin: typing.Optional[Number] = None,
    ):
        """

        :param celsius:
        :param fahrenheit:
        :param kelvin:
        """
        local_vars = locals()
        kwargs = {k: local_vars[k] for k in inspect.signature(self.__init__).parameters}

        (
            self._celsius, self._fahrenheit, self._kelvin
        ) = [Decimal() for _ in kwargs]

        super().__init__(**kwargs)

    @property
    def celsius(self) -> Decimal:
        """

        :return:
        """
        if self._celsius is not None:
            return self._celsius
        elif self._fahrenheit is not None:
            return Decimal("5") / Decimal("9") * (self.fahrenheit - Decimal("32"))
        elif self._kelvin is not None:
            return self.kelvin - Decimal("273.15")

    @property
    def fahrenheit(self) -> Decimal:
        """

        :return:
        """
        if self._fahrenheit is not None:
            return self._fahrenheit
        else:
            return Decimal("9") / Decimal("5") * self.celsius + Decimal("32")

    @property
    def kelvin(self) -> Decimal:
        """

        :return:
        """
        if self._kelvin is not None:
            return self._kelvin
        else:
            return self.celsius + Decimal("273.15")
