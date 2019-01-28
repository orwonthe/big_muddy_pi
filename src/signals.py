import time

try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    import mock_gpio.MOCK_GPIO as GPIO


def set_modes_and_warnings(gpio):
    gpio.setmode(GPIO.BOARD)
    gpio.setwarnings(False)

class SignalException(Exception):
    pass

class SignalList:
    def __init__(self, signals):
        self.signals = signals

    def setup(self):
        for signal in self.signals:
            signal.setup()


class GpioPin:
    def __init__(self, signal_name, pin_number, gpio=None):
        if gpio is None:
            gpio = GPIO
        self.gpio = gpio
        self.signal_name = signal_name
        self.pin_number = pin_number
        self.inverted = False


class GpioInputPin(GpioPin):
    def setup(self):
        self.gpio.setup(self.pin_number, self.gpio.IN)


    def read(self):
        if self.inverted:
            return 1 - self.gpio.input(self.pin_number)
        else:
            return self.gpio.input(self.pin_number)


class GpioOutputPin(GpioPin):
    def setup(self):
        self.gpio.setup(self.pin_number, self.gpio.OUT)

    def write(self, state):
        if self.inverted:
            self.gpio.output(self.pin_number, 1 - state)
        else:
            self.gpio.output(self.pin_number, state)


class GpioLinkedPins(SignalList):
    def __init__(self,
                 signal_prefix,
                 in_pin_number,
                 out_pin_number,
                 gpio=None):
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
    def __init__(self,
                 in_pin_number,
                 out_pin_number,
                 signal_prefix="clock",
                 gpio=None,
                 cycle=0.0015
                 ):
        self.half_cycle=cycle/2
        super().__init__(
            signal_prefix=signal_prefix,
            in_pin_number=in_pin_number,
            out_pin_number=out_pin_number,
            gpio=gpio
        )

    def pulse(self):
        self.output.write(1)
        time.sleep(self.half_cycle)
        if not self.read():
            raise SignalException("Clock stuck low")
        self.output.write(0)
        time.sleep(self.half_cycle)
        if self.read():
            raise SignalException("Clock stuck high")



class LoadingPins(ClockingPins):
    def __init__(self,
                 in_pin_number,
                 out_pin_number,
                 signal_prefix="load",
                 gpio=None):
        super().__init__(
            signal_prefix=signal_prefix,
            in_pin_number=in_pin_number,
            out_pin_number=out_pin_number,
            gpio=gpio
        )

class ShiftingPins(ClockingPins):
    def __init__(self,
                 in_pin_number,
                 out_pin_number,
                 signal_prefix="shift",
                 gpio=None):
        super().__init__(
            signal_prefix=signal_prefix,
            in_pin_number=in_pin_number,
            out_pin_number=out_pin_number,
            gpio=gpio
        )

class DataPins(GpioLinkedPins):
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
        return self.read()

    def start_duration_measurement(self):
        self.duration = None
        self._duration = 0

    def check_duration(self):
        if self.duration is None:
            if self.read():
                self.duration = self._duration
            else:
                self._duration += 1
        elif not self.read():
            raise SignalException("broken data chain at " + self.signal_name)


class SerialDataSystem(SignalList):
    def __init__(self,
                 loading,
                 shifting,
                 data_signals=None,
                 max_test_duration=500,
                 ):
        if data_signals is None:
            data_signals = []
        self.data_signals = data_signals
        self.loading = loading
        self.shifting = shifting
        self.max_test_duration=max_test_duration
        self.duration = None
        super().__init__(
            [self.loading, self.shifting] + data_signals
        )

    def shift(self, state_list):
        result = self.read_data()
        self.write_data(state_list)
        self.shifting.pulse()
        return result

    def write_data(self, state_list):
        for data_signal, state in zip(self.data_signals, state_list):
            data_signal.write(state)

    def read_data(self):
        return [data_signal.read() for data_signal in self.data_signals]

    def set_data_pins(self, value):
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
        self.set_data_pins(0)
        time.sleep(0.01)
        for _ in range(self.max_test_duration):
            self.shifting.pulse()
        self.check_cleared()
        self.set_data_pins(1)
        time.sleep(0.01)
        self.start_duration_measurement()
        # for _ in range(self.max_test_duration):
        for _ in range(50):
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





