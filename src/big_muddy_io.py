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


def keep_on_loading(big_muddy):
    print('loading')
    while True:
        big_muddy.set_data_pins(0)
        big_muddy.loading.pulse()
        big_muddy.set_data_pins(1)
        big_muddy.loading.pulse()


def keep_on_shifting(big_muddy):
    print('shifting')
    while True:
        big_muddy.set_data_pins(0)
        big_muddy.shifting.pulse()
        big_muddy.set_data_pins(0)
        big_muddy.shifting.pulse()
        big_muddy.set_data_pins(0)
        big_muddy.shifting.pulse()
        big_muddy.set_data_pins(1)
        big_muddy.shifting.pulse()
        big_muddy.set_data_pins(1)
        big_muddy.shifting.pulse()


def keep_on_shift_clocking(big_muddy):
    print('shift clocking')
    while True:
        big_muddy.shifting.pulse()


def client_connector_test(big_muddy, sleep_time=0.25):
    print('pin test')
    client_signals = [signal << 4 for signal in [1, 3, 5, 7]]
    cycle_count = 0
    bits_read = [[0, 0], [0, 0], [0, 0], [0, 0]]
    bits_expected = [[0, 0], [0, 0], [0, 0], [0, 0]]
    client_names = ["D", "C", "B", "A"]
    bit_names = ["SW1 (Green)", "SW0 (green/white)"]
    while True:
        bits_connected = [[True, True], [True, True], [True, True], [True, True]]
        for cycle_index in range(5):
            for shift_index in range(8):
                time.sleep(sleep_time)
                for client_index in range(4):
                    for bit_index in range(2):
                        bits_read[client_index][bit_index] = big_muddy.servos.read()
                        big_muddy.shifting.pulse()
                for client_index in range(4):
                    client_signal = client_signals[client_index]
                    bits = client_signal >> shift_index
                    for bit_index in range(4):
                        send_bit = bits & 1
                        if bit_index < 2:
                            bits_expected[client_index][bit_index] = send_bit
                        big_muddy.set_data_pins(send_bit)
                        bits = bits >> 1
                        big_muddy.shifting.pulse()
                big_muddy.loading.pulse()
                if cycle_index > 1:
                    for client_index in range(4):
                        for bit_index in range(2):
                            matching = bits_expected[client_index][bit_index] == bits_read[client_index][bit_index]
                            if not matching and bits_connected[client_index][bit_index]:
                                bits_connected[client_index][bit_index] = False
        for client_index in reversed(range(4)):
            if bits_connected[client_index][0] and bits_connected[client_index][1]:
                print("client " + client_names[client_index] + " appears to be okay")
            elif not bits_connected[client_index][0] and not bits_connected[client_index][1]:
                print("client " + client_names[client_index] + " is not connected")
            else:
                for bit_index in range(2):
                    if not bits_connected[client_index][bit_index]:
                        print("client " + client_names[client_index] + " is not connected at bit " + bit_names[
                            bit_index])
        print()

def main():
    print(GPIO.RPI_INFO)
    big_muddy = BigMuddyIO()
    big_muddy.setup()
    # clocked_data_probe(big_muddy)
    # clock_probe(big_muddy)
    # data_probe(big_muddy)
    # duration_testing(big_muddy)
    # keep_on_loading(big_muddy)
    # keep_on_shifting(big_muddy)
    # keep_on_shift_clocking(big_muddy)
    client_connector_test(big_muddy)


if __name__ == '__main__':
    main()
