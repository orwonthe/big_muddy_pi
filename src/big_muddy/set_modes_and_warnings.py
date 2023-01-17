# Copyright 2022 WillyMillsLLC
try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    from big_muddy import mock_gpio as GPIO

def set_modes_and_warnings(gpio):
    """
    Sets the GPIO system for normal operation.
    :param gpio: GPIO system, unless mocking
    """
    gpio.setmode(GPIO.BOARD)
    gpio.setwarnings(False)
