from RPi import GPIO

from big_muddy.signals import ShiftingPins, SerialDataSystem, set_modes_and_warnings, \
    DataPins, LoadingPins

# GPIO data input and output pin numbers.
DATA_A_OUT = 26
DATA_B_OUT = 24
SHIFT_OUT = 23
LOAD_OUT = 21

DATA_A_IN = 19
DATA_B_IN = 15
SHIFT_IN = 22
LOAD_IN = 18

class BigMuddyIO(SerialDataSystem):
    """
    Serial data system for Big Muddy Railroad.

    Contains two daisy chains: one for mechanical servos controlling railroad functions,
    the other for user consoles to operate the railroad.
    As there are only one set of gpio pins, the architecture should normally use this as a singleton.
    """

    def __init__(self, gpio=None, raise_clock_loop_exceptions=True):
        """
        Create the singleton serial data system.
        The data and clock bits of the serial system normally return back.
        So if a clock line is changed, and its return line does not change,
        the loop is broken. Normally this will throw an exception.

        :param gpio: the gpio data system
        :param raise_clock_loop_exceptions: set to false when probing broken hardware.
        """
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
            # The parallel load clock line, and its return echo.
            loading=LoadingPins(
                in_pin_number=LOAD_IN,
                out_pin_number=LOAD_OUT,
                gpio=self.gpio,
                raise_exceptions=raise_clock_loop_exceptions
            ),
            # The serial shift clock line, and its return echo.
            shifting=ShiftingPins(
                in_pin_number=SHIFT_IN,
                out_pin_number=SHIFT_OUT,
                gpio=self.gpio,
                raise_exceptions=raise_clock_loop_exceptions
            ),
            # The list of serial data lines, which share clocking
            data_signals=[
                self.consoles, # user consoles for user input and response.
                self.servos # servos and sensors that control and observe the railroad proper.
            ]
        )
        # Whether the semantics of a signal are inverted in the hardware logic.
        # True here means active low signals.
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
        # If this print statement does not occur exactly once, the singleton assumption is broken.
        print("Big Muddy IO Setup")

    @staticmethod
    def system(raise_clock_loop_exceptions=True):
        """ Create and setup the BigMuddyIO system """
        big_muddy = BigMuddyIO(raise_clock_loop_exceptions=raise_clock_loop_exceptions)
        big_muddy.setup()
        return big_muddy
