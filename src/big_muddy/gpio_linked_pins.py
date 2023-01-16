# Copyright 2022 WillyMillsLLC
import time

from clocking_checker import ClockingChecker
from gpio_input_pin import GpioInputPin
from gpio_output_pin import GpioOutputPin
from signal_list import SignalList
from gpio_pin import DEFAULT_CLOCKING_CYCLE_SECONDS


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
    """ Pair of gpio pins used for daisy-chained clocking signal. """

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

    def pulse(self):
        """
        Transmit clock pulses
        """
        self.output.write(1)
        while True:
            if self.read():
                break
        self.output.write(0)
        while True:
            if not self.read():
                break

    def timed_pulse(self, count=1):
        """
        Transmit clock pulses
        :param count: how many (default is just one)
        """
        for _ in range(count):
            self.output.write(1)
            time.sleep(self.half_cycle)
            ClockingChecker.expect_true(self.read())
            self.output.write(0)
            time.sleep(self.half_cycle)
            ClockingChecker.expect_false(self.read())
