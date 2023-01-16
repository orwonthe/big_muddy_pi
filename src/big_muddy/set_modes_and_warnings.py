# Copyright 2022 WillyMillsLLC
import mock_gpio as GPIO


def set_modes_and_warnings(gpio):
    """
    Sets the GPIO system for normal operation.
    :param gpio: GPIO system, unless mocking
    """
    gpio.setmode(GPIO.BOARD)
    gpio.setwarnings(False)
