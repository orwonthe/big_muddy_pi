from signal_exception import SignalException


class ClockingChecker:
    """
    Ensure clock signals travel through the entire hardware daisy chain.

    The two clock signals, shift and load, are each on a GPIO output pin.
    Those travel through the daisy chain (for robustness in opposite direction as data travels).
    They each return to a pair of GPIO input pins.
    If the daisy chain is intact, without disconnect cables or other hardware faults,
    then the value on the input pin should match the value just placed on the output pin.
    In normal operations a failure of clock integrity should raise an exception.
    However, when debugging the hardware it is very useful to ignore the integrity
    and keep the clock pulses running. The ClockingChecker is a singleton object
    that does the integrity check normally, but can be turned off.

    """
    # Default for whether to raise clocking exceptions.
    # Normally true for actual operations.
    # Sometimes handy to set to false when debugging hardware.
    __raise_exception = True

    @staticmethod
    def set_raise_clock_exceptions(raise_clock_exception):
        ClockingChecker.__raise_exception = raise_clock_exception

    @staticmethod
    def does_raise_exceptions():
        """ Whether exception is raised when expectation fails """
        return ClockingChecker.__raise_exception

    @staticmethod
    def expect_false(value):
        """ Raise exception if value is not False """
        """ Throw an exception if expectationis False and exceptioning is on """
        if value and ClockingChecker.__raise_exception:
            raise SignalException("Clock stuck high")
        return not value

    @staticmethod
    def expect_true(value):
        """ Raise exception if value is not True """
        if not value and ClockingChecker.__raise_exception:
            raise SignalException("Clock stuck low")
        return value
