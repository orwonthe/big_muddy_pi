import time

from clocking_checker import ClockingChecker
from signal_exception import SignalException

try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    from big_muddy import mock_gpio as GPIO

JUST_TESTING = True
# Inverse of clocking frequency, default value.
GOOD_TEST_FREQUENCY = 500.0  # hz
GOOD_LIVE_FREQUENCY = 50 * 1000.0  # hz
DEFAULT_CLOCKING_CYCLE_SECONDS = (1.0 / GOOD_TEST_FREQUENCY) if JUST_TESTING else (1.0 / GOOD_LIVE_FREQUENCY)


def set_modes_and_warnings(gpio):
    """
    Sets the GPIO system for normal operation.
    :param gpio: GPIO system, unless mocking
    """
    gpio.setmode(GPIO.BOARD)
    gpio.setwarnings(False)


class SignalList:
    """ Base class implements setup method for signal list """

    def __init__(self, signals):
        self.signals = signals

    def setup(self):
        for signal in self.signals:
            signal.setup()


class GpioPin:
    """ base class for Named and numbered GPIO pin """

    def __init__(self, signal_name, pin_number, gpio=None):
        if gpio is None:
            gpio = GPIO
        self.gpio = gpio
        self.signal_name = signal_name
        self.pin_number = pin_number
        self.inverted = False


class GpioInputPin(GpioPin):
    """ GPIO input pin can be read """

    def setup(self):
        self.gpio.setup(self.pin_number, self.gpio.IN)

    def read(self):
        """
        Reads current state of GPIO input pin.
        :return: 0 or 1
        """
        if self.inverted:
            return 1 - self.gpio.input(self.pin_number)
        else:
            return self.gpio.input(self.pin_number)


class GpioOutputPin(GpioPin):
    """ GPIO output pin can be written """

    def setup(self):
        self.gpio.setup(self.pin_number, self.gpio.OUT)

    def write(self, state):
        """
        Writes 0 or 1 to GPIO output pin.
        :param state: 0 or 1
        """
        if self.inverted:
            self.gpio.output(self.pin_number, 1 - state)
        else:
            self.gpio.output(self.pin_number, state)


class GpioLinkedPins(SignalList):
    """ Pair of GPIO pins, one in, one out. """

    def __init__(self,
                 signal_prefix,
                 in_pin_number,
                 out_pin_number,
                 gpio=None):
        """
        :param signal_prefix: common prefix used for both in and out pins
        :param in_pin_number: pin number for the input pin
        :param out_pin_number: pin number for the output pin
        :param gpio: GPIO system either real or mocked
        """
        self.signal_name = signal_prefix
        self.input = GpioInputPin(
            signal_name=signal_prefix + "_in",
            pin_number=in_pin_number,
            gpio=gpio
        )
        self.output = GpioOutputPin(
            signal_name=signal_prefix + "_out",
            pin_number=out_pin_number,
            gpio=gpio
        )
        super().__init__([
            self.output,
            self.input,
        ])

    def read(self):
        return self.input.read()

    def write(self, state):
        self.output.write(state)


class ClockingPins(GpioLinkedPins):
    """ Pair of gpio pins used for daisy chained clocking signal. """

    def __init__(self,
                 in_pin_number,
                 out_pin_number,
                 signal_prefix="clock",
                 gpio=None,
                 cycle=DEFAULT_CLOCKING_CYCLE_SECONDS,
                 ):
        """
        :param in_pin_number: pin number for returning clock signal
        :param out_pin_number: pin number for sending clock signal
        :param signal_prefix: name of clock signal ("shift", "load" etc.)
        :param gpio: real or mocked GPIO system
        :param cycle: clock period (reciprocal of frequency)
        """
        self.half_cycle = cycle / 2
        super().__init__(
            signal_prefix=signal_prefix,
            in_pin_number=in_pin_number,
            out_pin_number=out_pin_number,
            gpio=gpio
        )

    def pulse(self, count=1):
        """
        Trasnmit clock pulses
        :param count: how many (default is just one)
        """
        for _ in range(count):
            self.output.write(1)
            time.sleep(self.half_cycle)
            ClockingChecker.expect_true(self.read())
            self.output.write(0)
            time.sleep(self.half_cycle)
            ClockingChecker.expect_false(self.read())


class LoadingPins(ClockingPins):
    """
    Clock pins used for parallel load signal
    """

    def __init__(self,
                 in_pin_number,
                 out_pin_number,
                 signal_prefix="load",
                 gpio=None):
        super().__init__(
            signal_prefix=signal_prefix,
            in_pin_number=in_pin_number,
            out_pin_number=out_pin_number,
            gpio=gpio,
        )


class ShiftingPins(ClockingPins):
    """ Clock pins used for data shifting """

    def __init__(self,
                 in_pin_number,
                 out_pin_number,
                 signal_prefix="shift",
                 gpio=None):
        super().__init__(
            signal_prefix=signal_prefix,
            in_pin_number=in_pin_number,
            out_pin_number=out_pin_number,
            gpio=gpio,
        )


class DataPins(GpioLinkedPins):
    """ Pair of gpio pins used for serialized data """

    def __init__(self,
                 in_pin_number,
                 out_pin_number,
                 signal_prefix,
                 gpio=None):
        self.duration = None
        self._duration = 0
        super().__init__(
            signal_prefix=signal_prefix,
            in_pin_number=in_pin_number,
            out_pin_number=out_pin_number,
            gpio=gpio
        )

    def check_cleared(self):
        """ Used as part of daisy chain length self measurement """
        return self.read()

    def start_duration_measurement(self):
        """ Called at start of duration measurement """
        self.duration = None
        self._duration = 0

    def check_duration(self):
        """ Called at each cycle of duration measurement """
        if self.duration is None:
            if self.read():
                self.duration = self._duration
            else:
                self._duration += 1
        elif not self.read():
            raise SignalException("broken data chain at " + self.signal_name)


class SerialDataSystem(SignalList):
    """
    Class for managing a serial data source
    """

    def __init__(self,
                 loading,
                 shifting,
                 data_signals=None,
                 max_test_duration=540,
                 ):
        """
        :param loading: ClockingPins for parallel load of data
        :param shifting: ClockingPins for data shifting
        :param data_signals: list of data signals driven by loading and shifting
        :param max_test_duration: maximum expected length of serial data
        """
        if data_signals is None:
            data_signals = []
        self.data_signals = data_signals
        self.loading = loading
        self.shifting = shifting
        self.max_test_duration = max_test_duration
        self.duration = None
        self._max_duration = None
        super().__init__(
            [self.loading, self.shifting] + data_signals
        )

    def shift(self, state_list):
        """
        Read current data, then push new data into the serial stream.

        Uses one clock cycle.
        :param state_list: List of signal values, one per data signal line
        :return: current data
        """
        result = self.read_data()
        self.write_data(state_list)
        self.shifting.pulse()
        return result

    def write_data(self, state_list):
        """
        Push data to the output pins of the data signals.

        No clock cycles.
        :param state_list: list of values for the data signals.
        """
        for data_signal, state in zip(self.data_signals, state_list):
            data_signal.write(state)

    def read_data(self):
        """
        Read the data from the data signal input pins, no clock cycle

        :return: list of values from the data signals.
        """
        return [data_signal.read() for data_signal in self.data_signals]

    def set_data_pins(self, value):
        """
        push the value to all of the data signal input pins.
        No clock cycle.

        :param value:
        :return:
        """
        for data_signal in self.data_signals:
            data_signal.write(value)

    def start_duration_measurement(self):
        for data_signal in self.data_signals:
            data_signal.start_duration_measurement()

    def check_cleared(self):
        for data_signal in self.data_signals:
            if data_signal.check_cleared():
                print(data_signal.signal_name + ' would not clear')

    def check_duration(self):
        for data_signal in self.data_signals:
            data_signal.check_duration()

    def ensure_duration_is_valid(self):
        for data_signal in self.data_signals:
            if data_signal.duration is None:
                self._max_duration = None
                data_signal.check_duration()

    @property
    def max_duration(self):
        self.ensure_duration_is_valid()
        if self._max_duration is None:
            duration = 0
            for data_signal in self.data_signals:
                signal_duration = data_signal.duration
                if signal_duration is not None and signal_duration > duration:
                    duration = signal_duration
            self._max_duration = duration
        return self._max_duration

    def determine_durations(self):
        """ Calculate and save duration as max of duration for any data signals. """
        self.set_data_pins(0)
        time.sleep(0.01)
        for _ in range(self.max_test_duration):
            self.shifting.pulse()
        self.check_cleared()
        self.set_data_pins(1)
        time.sleep(0.01)
        self.start_duration_measurement()
        for _ in range(self.max_test_duration):
            self.check_duration()
            self.shifting.pulse()
        duration = 0
        for data_signal in self.data_signals:
            data_duration = data_signal.duration
            if data_duration is None:
                raise SignalException("Unable to determine duration for " + data_signal.signal_name)
            elif data_duration > duration:
                duration = data_duration
        self.duration = duration

    def set_all(self, value):
        """ Set all bits to the same value """
        self.set_data_pins(value)
        for _ in range(self.max_duration):
            self.shifting.pulse()
        self.loading.pulse()
