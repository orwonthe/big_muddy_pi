# Copyright 2022 WillyMillsLLC
from gpio_pin import GpioPin


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
