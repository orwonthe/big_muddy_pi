import time

from RPi import GPIO

from signals import GpioLinkedPins, SignalList, ClockingPins, ShiftingPins, SerialDataSystem, set_modes_and_warnings, \
    DataPins

DATA_A_OUT = 26
DATA_B_OUT = 24
SHIFT_OUT = 23
CLOCK_OUT = 21

DATA_A_IN = 19
DATA_B_IN = 15
SHIFT_IN = 22
CLOCK_IN = 18


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
            clocking=ClockingPins(
                in_pin_number=CLOCK_IN,
                out_pin_number=CLOCK_OUT,
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

    def setup(self):
        set_modes_and_warnings(self.gpio)
        super().setup()

def clock_probe(big_muddy):
    big_muddy.clocking.pulse()

def data_probe(big_muddy):
    error_count = 0
    for data_signal in big_muddy.signals:
        for index in range(10):
            for value in [0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1]:
                data_signal.write(value)
                time.sleep(0.001)
                read_value = data_signal.read()
                if read_value != value:
                    print('ERROR!')
                    error_count += 1
                print(data_signal.signal_name, index, value, read_value)
    print('errors = ', error_count)

def clocked_data_probe(big_muddy):
    error_count = 0
    for data_signal in big_muddy.data_signals:
        for index in range(10):
            for value in [0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1]:
                data_signal.write(value)
                big_muddy.clocking.pulse()
                # time.sleep(0.001)
                read_value = data_signal.read()
                if read_value != value:
                    print('ERROR!')
                    error_count += 1
                print(data_signal.signal_name, index, value, read_value)
    print('errors = ', error_count)

def duration_testing(big_muddy):
    big_muddy.determine_durations()
    for data_signal in big_muddy.data_signals:
        print(data_signal.signal_name, data_signal.duration)
    print(big_muddy.duration)

def main():
    print(GPIO.RPI_INFO)
    big_muddy = BigMuddyIO()
    big_muddy.setup()
    # clocked_data_probe(big_muddy)
    clock_probe(big_muddy)
    # data_probe(big_muddy)
    duration_testing(big_muddy)


if __name__ == '__main__':
    main()