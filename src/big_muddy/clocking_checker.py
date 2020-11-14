from big_muddy.signal_exception import SignalException

class ClockingChecker:
    # Default for whether to raise clocking exceptions.
    # Normally true for actual operations.
    # Sometimes handy to set to false when debugging hardware.
    __raise_exception = True

    @staticmethod
    def set_raise_clock_exceptions(raise_clock_exception):
        ClockingChecker.__raise_exception = raise_clock_exception

    @staticmethod
    def expect_false(value):
        if value and ClockingChecker.__raise_exception:
            raise SignalException("Clock stuck high")    \

    @staticmethod
    def expect_true(value):
        if not value and ClockingChecker.__raise_exception:
            raise SignalException("Clock stuck low")