import time

from RPi import GPIO

from signals import ShiftingPins, SerialDataSystem, set_modes_and_warnings, \
    DataPins, LoadingPins

DATA_A_OUT = 26
DATA_B_OUT = 24
SHIFT_OUT = 23
LOAD_OUT = 21

DATA_A_IN = 19
DATA_B_IN = 15
SHIFT_IN = 22
LOAD_IN = 18


class BigMuddyIO(SerialDataSystem):
    def __init__(self, gpio=None):
        if gpio is None:
            gpio = GPIO
        self.gpio = gpio
        self.consoles = DataPins(
            signal_prefix="consoles",
            in_pin_number=DATA_A_IN,
            out_pin_number=DATA_A_OUT,
            gpio=self.gpio
        )
        self.servos = DataPins(
            signal_prefix="servos",
            in_pin_number=DATA_B_IN,
            out_pin_number=DATA_B_OUT,
            gpio=self.gpio
        )
        super().__init__(
            loading=LoadingPins(
                in_pin_number=LOAD_IN,
                out_pin_number=LOAD_OUT,
                gpio=self.gpio
            ),
            shifting=ShiftingPins(
                in_pin_number=SHIFT_IN,
                out_pin_number=SHIFT_OUT,
                gpio=self.gpio
            ),
            data_signals=[
                self.consoles,
                self.servos
            ]
        )
        self.shifting.input.inverted = True
        self.shifting.output.inverted = True
        self.consoles.input.inverted = True
        self.consoles.output.inverted = True
        self.servos.input.inverted = True
        self.servos.output.inverted = True

    def setup(self):
        set_modes_and_warnings(self.gpio)
        super().setup()
        self.loading.write(0)

    @staticmethod
    def system():
        big_muddy = BigMuddyIO()
        big_muddy.setup()
        return big_muddy

