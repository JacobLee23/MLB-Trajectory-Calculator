"""

"""

from decimal import Decimal
import typing


class SIPrefixes:
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


class Unit:
    """

    """
    def __init__(self, name: str, abbreviation: str):
        """

        :param name:
        :param abbreviation:
        """
        self._name = name.lower()
        self._abbreviation = abbreviation

    def __repr__(self) -> str:
        return f"{type(self).__name__}(name='{self.name}', abbr='{self.abbr}')"

    @property
    def name(self) -> str:
        """

        :return:
        """
        return self._name

    @property
    def abbreviation(self) -> str:
        """

        :return:
        """
        return self._abbreviation

    abbr = abbreviation


class Dimension(SIPrefixes):
    """

    """
    units: typing.Tuple[Unit]

    def __init__(self, x: Decimal, unit: Unit):
        """

        :param x:
        :param unit:
        """
        if unit not in self.units:
            raise ValueError(
                f"Unknown unit: {unit}"
            )

        self._x = x
        self._unit = unit

    def __repr__(self):
        return f"{type(self).__name__}(x={self._x}, quantity='{self._unit.name}')"

    def __getitem__(self, item: str) -> Decimal:
        """

        :param item:
        :return:
        """
        return self.__getattribute__(item)


# Derived Dimensions


class Length(Dimension):
    """

    """
    # Imperial Units
    Inch = Unit("inch", "in")
    Foot = Unit("foot", "ft")
    Yard = Unit("yard", "yd")
    Mile = Unit("mile", "mi")

    # SI Units
    Meter = Unit("meter", "m")

    units = (
        Foot, Inch, Meter, Mile, Yard
    )

    @property
    def foot(self) -> Decimal:
        """

        :return:
        """
        if self._unit is self.Foot:
            return self._x
        # in / (in / ft)
        return self.inch / Decimal(12)

    @property
    def inch(self) -> Decimal:
        """

        :return:
        """
        if self._unit is self.Inch:
            return self._x
        elif self._unit is self.Foot:
            # ft * (in / ft)
            return self._x * Decimal(12)
        elif self._unit is self.Meter:
            # m / (m / cm) / (cm / in)
            return self._x / self.centi / Decimal("2.54")
        elif self._unit is self.Mile:
            # mi * (ft / mi) * (in / ft)
            return self._x * Decimal(5280) * Decimal(12)
        elif self._unit is self.Yard:
            # yd * (ft / yd) * (in / ft)
            return self._x * Decimal(3) * Decimal(12)

    @property
    def meter(self) -> Decimal:
        """

        :return:
        """
        if self._unit is self.Meter:
            return self._x
        # in * (cm / in) * (m / cm)
        return self.inch * Decimal("2.54") * self.centi

    @property
    def mile(self) -> Decimal:
        """

        :return:
        """
        if self._unit is self.Mile:
            return self._x
        # in / (in / ft) / (ft / mi)
        return self.inch / Decimal(12) / Decimal(5280)

    @property
    def yard(self) -> Decimal:
        """

        :return:
        """
        if self._unit is self.Yard:
            return self._x
        # in / (in / ft) / (ft / yd)
        return self.inch / Decimal(12) / Decimal(3)


class Temperature(Dimension):
    """

    """
    # Imperial Units
    Fahrenheit = Unit("fahrenheit", "degF")

    # SI Units
    Celsius = Unit("celsius", "degC")
    Kelvin = Unit("kelvin", "K")

    units = (
        Celsius, Fahrenheit, Kelvin
    )

    @property
    def celsius(self) -> Decimal:
        """

        :return:
        """
        if self._unit is self.Celsius:
            return self._x
        elif self._unit is self.Fahrenheit:
            return Decimal(5) / Decimal(9) * (self.fahrenheit - Decimal(32))
        elif self._unit is self.Kelvin:
            return self.kelvin - Decimal("273.15")

    @property
    def fahrenheit(self) -> Decimal:
        """

        :return:
        """
        if self._unit is self.Fahrenheit:
            return self._x
        return Decimal(9) / Decimal(5) * self.celsius + Decimal(32)

    @property
    def kelvin(self) -> Decimal:
        """

        :return:
        """
        if self._unit is self.Kelvin:
            return self._x
        return self.celsius + Decimal("273.15")


class Mass(Dimension):
    """

    """
    # Imperial Units
    Ounce = Unit("ounce", "oz")
    Pound = Unit("pound", "lb")
    TonUK = Unit("ton_uk", "t")
    TonUS = Unit("ton_us", "t")

    # SI Units
    Gram = Unit("gram", "g")

    units = (
        Gram, Ounce, Pound, TonUK, TonUS
    )

    @property
    def gram(self) -> Decimal:
        """

        :return:
        """
        if self._unit is self.Gram:
            return self._x
        return self.ounce * Decimal("28.349523125")

    @property
    def ounce(self) -> Decimal:
        """

        :return:
        """
        if self._unit is self.Gram:
            return self._x / Decimal("28.349523125")
        elif self._unit is self.Ounce:
            return self._x
        elif self._unit is self.Pound:
            return self._x * Decimal(16)
        elif self._unit is self.TonUK:
            return self._x * Decimal(35840)
        elif self._unit is self.TonUS:
            return self._x * Decimal(32000)

    @property
    def pound(self) -> Decimal:
        """

        :return:
        """
        if self._unit is self.Pound:
            return self._x
        return self.ounce / Decimal(16)

    @property
    def ton_uk(self) -> Decimal:
        """

        :return:
        """
        if self._unit is self.TonUK:
            return self._x
        return self.ounce / Decimal(35840)

    @property
    def ton_us(self) -> Decimal:
        if self._unit is self.TonUS:
            return self._x
        return self.ounce / Decimal(32000)


# Derived Dimensions


class Velocity(Dimension):
    """

    """
    # Imperial Units
    FootPerSecond = Unit("foot_per_second", "ft/s")
    MilePerHour = Unit("mile_per_hour", "mi/h")

    # SI Units
    MeterPerSecond = Unit("meter_per_second", "m/s")
    KilometerPerHour = Unit("kilometer_per_hour", "km/h")

    units = (
        FootPerSecond, KilometerPerHour, MeterPerSecond, MilePerHour
    )

    @property
    def foot_per_second(self) -> Decimal:
        """

        :return:
        """
        if self._unit is self.FootPerSecond:
            return self._x
        return Length(self.meter_per_second, Length.Meter).foot

    @property
    def kilometer_per_hour(self) -> Decimal:
        """

        :return:
        """
        if self._unit is self.KilometerPerHour:
            return self._x
        return self.meter_per_second / self.kilo * Decimal(3600)

    @property
    def meter_per_second(self) -> Decimal:
        """

        :return:
        """
        if self._unit is self.FootPerSecond:
            return Length(self._x, Length.Foot).meter
        elif self._unit is self.KilometerPerHour:
            return self._x * self.kilo / Decimal(3600)
        elif self._unit is self.MeterPerSecond:
            return self._x
        elif self._unit is self.MilePerHour:
            return Length(self._x, Length.Mile).meter / Decimal(3600)

    @property
    def mile_per_hour(self) -> Decimal:
        """

        :return:
        """
        if self._unit is self.MilePerHour:
            return self._x
        return Length(self.meter_per_second, Length.Meter).mile * Decimal(3600)
