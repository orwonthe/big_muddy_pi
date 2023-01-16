# Copyright 2022 WillyMillsLLC
try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    from big_muddy import mock_gpio as GPIO

# Inverse of clocking frequency, default value.
JUST_TESTING = False
GOOD_TEST_FREQUENCY = 500.0  # hz
GOOD_LIVE_FREQUENCY = 50 * 1000.0  # hz
DEFAULT_CLOCKING_CYCLE_SECONDS = (1.0 / GOOD_TEST_FREQUENCY) if JUST_TESTING else (1.0 / GOOD_LIVE_FREQUENCY)


class GpioPin:
    """ base class for Named and numbered GPIO pin """

    def __init__(self, signal_name, pin_number, gpio=None):
        if gpio is None:
            gpio = GPIO
        self.gpio = gpio
        self.signal_name = signal_name
        self.pin_number = pin_number
        self.inverted = False
