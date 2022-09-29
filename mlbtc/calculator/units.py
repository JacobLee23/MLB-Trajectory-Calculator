"""

"""

from decimal import Decimal
import inspect
import typing

from .constants import Number


class MetricPrefixes:
    """

    """
    yotta = Decimal("1E+24")
    zetta = Decimal("1E+21")
    exa = Decimal("1E+18")
    peta = Decimal("1E+15")
    tera = Decimal("1E+12")
    giga = Decimal("1E+9")
    mega = Decimal("1E+6")
    kilo = Decimal("1E+3")
    hecto = Decimal("1E+2")
    deka = Decimal("1E+1")

    deci = Decimal("1E-1")
    centi = Decimal("1E-2")
    milli = Decimal("1E-3")
    micro = Decimal("1E-6")
    nano = Decimal("1E-9")
    pico = Decimal("1E-12")
    femto = Decimal("1E-15")
    atto = Decimal("1E-18")
    zepto = Decimal("1E-21")
    yoct = Decimal("1E-24")


# Basic Units


class Unit(MetricPrefixes):
    """

    """
    def __init__(self, **kwargs):
        """

        :param kwargs:
        """
        if [x is not None for x in kwargs.values()].count(True) != 1:
            params = ", ".join(kwargs)
            raise ValueError(
                f"Exactly one of {params} must be a non-null value: {kwargs}"
            )

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
            # ft * (in / ft)
            return self.foot * Decimal(12)
        elif self._meter is not None:
            # m / (m / cm) / (cm / in)
            return self.meter / self.centi / Decimal("2.54")
        elif self._mile is not None:
            # mi * (ft / mi) * (in / ft)
            return self.mile * Decimal(5280) * Decimal(12)
        elif self._yard is not None:
            # yd * (ft / yd) * (in / ft)
            return self.yard * Decimal(3) * Decimal(12)

    @property
    def foot(self) -> Decimal:
        """

        :return:
        """
        if self._foot is not None:
            return self._foot
        # in / (in / ft)
        return self.inch / Decimal(12)

    @property
    def meter(self) -> Decimal:
        """

        :return:
        """
        if self._meter is not None:
            return self._meter
        # in * (cm / in) * (m / cm)
        return self.inch * Decimal("2.54") * self.centi

    @property
    def mile(self) -> Decimal:
        """

        :return:
        """
        if self._mile is not None:
            return self._mile
        # in / (in / ft) / (ft / mi)
        return self.inch / Decimal(12) / Decimal(5280)

    @property
    def yard(self) -> Decimal:
        """

        :return:
        """
        if self._yard is not None:
            return self._yard
        # in / (in / ft) / (ft / yd)
        return self.inch / Decimal(12) / Decimal(3)


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
            return Decimal(5) / Decimal(9) * (self.fahrenheit - Decimal(32))
        elif self._kelvin is not None:
            return self.kelvin - Decimal("273.15")

    @property
    def fahrenheit(self) -> Decimal:
        """

        :return:
        """
        if self._fahrenheit is not None:
            return self._fahrenheit
        return Decimal(9) / Decimal(5) * self.celsius + Decimal(32)

    @property
    def kelvin(self) -> Decimal:
        """

        :return:
        """
        if self._kelvin is not None:
            return self._kelvin
        return self.celsius + Decimal("273.15")


class Mass(Unit):
    """

    """
    def __init__(
            self, *,
            gram: typing.Optional[Number] = None,
            ounce: typing.Optional[Number] = None,
            pound: typing.Optional[Number] = None,
            ton_uk: typing.Optional[Number] = None,
            ton_us: typing.Optional[Number] = None
    ):
        """

        :param gram:
        :param ounce:
        :param pound:
        :param ton_uk:
        :param ton_us:
        """
        local_vars = locals()
        kwargs = {k: local_vars[k] for k in inspect.signature(self.__init__).parameters}

        (
            self._gram, self._ounce, self._pound, self._ton_uk, self._ton_us
        ) = [Decimal() for _ in kwargs]

        super().__init__(**kwargs)

    @property
    def gram(self) -> Decimal:
        """

        :return:
        """
        if self._gram is not None:
            return self._gram
        return self.ounce * Decimal("28.349523125")

    @property
    def ounce(self) -> Decimal:
        """

        :return:
        """
        if self._gram is not None:
            return self.gram / Decimal("28.349523125")
        elif self._ounce is not None:
            return self._ounce
        elif self._pound is not None:
            return self.pound * Decimal(16)
        elif self._ton_uk is not None:
            return self.ton_uk * Decimal(35840)
        elif self._ton_us is not None:
            return self.ton_us * Decimal(32000)

    @property
    def pound(self) -> Decimal:
        """

        :return:
        """
        if self._pound is not None:
            return self._pound
        return self.ounce / Decimal(16)

    @property
    def ton_uk(self) -> Decimal:
        """

        :return:
        """
        if self._ton_uk is not None:
            return self._ton_uk
        return self.ounce / Decimal(35840)

    @property
    def ton_us(self) -> Decimal:
        if self._ton_us is not None:
            return self._ton_us
        return self.ounce / Decimal(32000)


# Derived Units


class Velocity(Unit):
    """

    """
    def __init__(
            self, *,
            foot_per_second: typing.Optional[Number] = None,
            meter_per_second: typing.Optional[Number] = None,
            mile_per_hour: typing.Optional[Number] = None
    ):
        """

        :param foot_per_second:
        :param meter_per_second:
        :param mile_per_hour:
        """
        local_vars = locals()
        kwargs = {k: local_vars[k] for k in inspect.signature(self.__init__).parameters}

        (
            self._foot_per_second, self._meter_per_second, self._mile_per_hour
        ) = [Decimal() for _ in kwargs]

        super().__init__(**kwargs)

    @property
    def foot_per_second(self) -> Decimal:
        """

        :return:
        """
        if self._foot_per_second is not None:
            return self._foot_per_second
        return Length(meter=self.meter_per_second).foot

    @property
    def meter_per_second(self) -> Decimal:
        """

        :return:
        """
        if self._foot_per_second is not None:
            return Length(foot=self.foot_per_second).meter
        elif self._meter_per_second is not None:
            return self._meter_per_second
        elif self._mile_per_hour is not None:
            return Length(mile=self.mile_per_hour).meter / Decimal(3600)

    @property
    def mile_per_hour(self) -> Decimal:
        """

        :return:
        """
        if self._mile_per_hour is not None:
            return self._mile_per_hour
        return Length(meter=self.meter_per_second).mile * Decimal(3600)
