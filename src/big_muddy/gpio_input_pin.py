# Copyright 2022 WillyMillsLLC
from gpio_pin import GpioPin


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
