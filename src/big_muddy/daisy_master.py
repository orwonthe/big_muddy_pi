from big_muddy.big_muddy_io import BigMuddyIO
from big_muddy.daisy_loop import ServoDaisyLoop, ConsoleDaisyLoop


class DaisyMaster:
    def __init__(self, daisy_units=None):
        self.big_muddy_io = BigMuddyIO.system()
        self.servo_loop = ServoDaisyLoop()
        self.console_loop = ConsoleDaisyLoop()
        if daisy_units:
            self.add_daisy_units(daisy_units)

    def set_for_action(self):
        initial_console_bits = self.console_loop.bit_count
        initial_servo_bits = self.servo_loop.bit_count
        self.bit_count = max(initial_console_bits, initial_servo_bits)
        print(f"bit count={self.bit_count} console={initial_console_bits} servo={initial_servo_bits}")
        self.console_loop.add_delay(initial_servo_bits - initial_console_bits)
        self.servo_loop.add_delay(initial_console_bits - initial_servo_bits)
        self.console_loop.set_for_action()
        self.servo_loop.set_for_action()

    def add_daisy_units(self, daisy_units):
        for daisy_unit in daisy_units:
            self.add_daisy_unit(daisy_unit)

    def add_daisy_unit(self, daisy_unit):
        if daisy_unit.is_console:
            self.console_loop.add_daisy_unit(daisy_unit)
        else:
            self.servo_loop.add_daisy_unit(daisy_unit)

    def bits_to_send(self, index):
        return self.console_loop.bit_to_send(index), self.servo_loop.bit_to_send(index)

    def receive_bits(self, index, console_bit, servo_bit):
        self.console_loop.receive_bit(index, console_bit)
        self.servo_loop.receive_bit(index, servo_bit)

    def pull_data(self):
        self.big_muddy_io.loading.pulse()
        self.transfer_data()

    def transfer_data(self):
        for index in range(self.bit_count):
            console_bit_to_send, servo_bit_to_send = self.bits_to_send(index)
            data = self.big_muddy_io.read_data()
            console_bit_received = data[0]
            servo_bit_received = data[1]
            # print(f'index={index} sending {console_bit_to_send} {servo_bit_to_send}')
            self.receive_bits(index, console_bit_received, servo_bit_received)
            self.big_muddy_io.write_data([console_bit_to_send, servo_bit_to_send])
            self.big_muddy_io.shifting.pulse()
        self.big_muddy_io.loading.pulse()

    def show_status(self):
        self.console_loop.show_status()
        self.servo_loop.show_status()
