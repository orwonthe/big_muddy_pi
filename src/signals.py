import time

try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    import mock_gpio.MOCK_GPIO as GPIO

# Default for whether to raise clocking exceptions.
# Normally true for actual operations.
# Sometimes handy to set to false when debugging hardware.
RAISE_CLOCKING_EXCEPTIONS = True

# Inverse of clocking frequency, default value.
DEFAULT_CLOCKING_CYCLE = 0.00001


def set_modes_and_warnings(gpio):
    """
    Sets the GPIO system for normal operation.
    :param gpio: GPIO system, unless mocking
    """
    gpio.setmode(GPIO.BOARD)
    gpio.setwarnings(False)


class SignalException(Exception):
    """  Used when some hardware enforced constraint fails. """
    pass


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
                 cycle=DEFAULT_CLOCKING_CYCLE,
                 raise_exceptions=RAISE_CLOCKING_EXCEPTIONS
                 ):
        """
        :param in_pin_number: pin number for returning clock signal
        :param out_pin_number: pin number for sending clock signal
        :param signal_prefix: name of clock signal ("shift", "load" etc.)
        :param gpio: real or mocked GPIO system
        :param cycle: clock period (reciprocal of frequency)
        :param raise_exceptions:
        """
        self.half_cycle = cycle / 2
        self.raise_exceptions = raise_exceptions
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
            if not self.read() and self.raise_exceptions:
                raise SignalException("Clock stuck low")
            self.output.write(0)
            time.sleep(self.half_cycle)
            if self.read() and self.raise_exceptions:
                raise SignalException("Clock stuck high")


class LoadingPins(ClockingPins):
    """
    Clock pins used for parallel load signal
    """

    def __init__(self,
                 in_pin_number,
                 out_pin_number,
                 signal_prefix="load",
                 raise_exceptions=RAISE_CLOCKING_EXCEPTIONS,
                 gpio=None):
        super().__init__(
            signal_prefix=signal_prefix,
            in_pin_number=in_pin_number,
            out_pin_number=out_pin_number,
            gpio=gpio,
            raise_exceptions=raise_exceptions
        )


class ShiftingPins(ClockingPins):
    """ Clock pins used for data shifting """

    def __init__(self,
                 in_pin_number,
                 out_pin_number,
                 signal_prefix="shift",
                 raise_exceptions=RAISE_CLOCKING_EXCEPTIONS,
                 gpio=None):
        super().__init__(
            signal_prefix=signal_prefix,
            in_pin_number=in_pin_number,
            out_pin_number=out_pin_number,
            gpio=gpio,
            raise_exceptions=raise_exceptions
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
