from big_muddy.daisy_unit import DaisyUnitDelay


class DaisyMaster:
    def __init__(self, big_muddy, daisy_units):
        self.big_muddy = big_muddy
        self.servo_loop = DaisyLoop()
        self.console_loop = DaisyLoop()
        for daisy_unit in daisy_units:
            if daisy_unit.is_console:
                self.console_loop.add_daisy_unit(daisy_unit)
            else:
                self.servo_loop.add_daisy_unit(daisy_unit)
        self.initial_console_bits = self.console_loop.bit_count
        self.initial_servo_bits = self.servo_loop.bit_count
        self.bit_count = max(self.initial_console_bits, self.initial_servo_bits)
        print(f"bit count={self.bit_count} console={self.initial_console_bits} servo={self.initial_servo_bits}")
        self.console_loop.add_delay(self.initial_servo_bits - self.initial_console_bits)
        self.servo_loop.add_delay(self.initial_console_bits - self.initial_servo_bits)
        # print("console_loop.set_for_action")
        self.console_loop.set_for_action()
        # print("servo_loop.set_for_action")
        self.servo_loop.set_for_action()

    def bits_to_send(self, index):
        return self.console_loop.bit_to_send(index), self.servo_loop.bit_to_send(index)

    def receive_bits(self, index, console_bit, servo_bit):
        self.console_loop.receive_bit(index, console_bit)
        self.servo_loop.receive_bit(index, servo_bit)

    def transfer_data(self):
        for index in range(self.bit_count):
            console_bit_to_send, servo_bit_to_send = self.bits_to_send(index)
            data = self.big_muddy.read_data()
            console_bit_received = data[0]
            servo_bit_received = data[1]
            # print(f'index={index} sending {console_bit_to_send} {servo_bit_to_send}')
            self.receive_bits(index, console_bit_received, servo_bit_received)
            self.big_muddy.write_data([console_bit_to_send, servo_bit_to_send])
            self.big_muddy.shifting.pulse()
        self.big_muddy.loading.pulse()

class DaisyLoop:
    def __init__(self):
        self.daisy_units = []
        self.delay_unit = None
        self.bit_count = 0
        self.delay = None
        self.bit_receiver = []
        self.bit_sender = []

    def add_daisy_unit(self, daisy_unit):
        self.daisy_units.append(daisy_unit)
        self.bit_count += daisy_unit.bit_count

    def add_delay(self, delay):
        if (delay > 0):
            self.delay = delay
            self.bit_count += delay
            self.delay_unit = DaisyUnitDelay(delay)

    def set_for_action(self):
        if self.delay_unit:
            send_list = [self.delay_unit] + self.daisy_units
            receive_list = self.daisy_units + [self.delay_unit]
        else:
            send_list = self.daisy_units
            receive_list = self.daisy_units
        # print("bit_sender list")
        self.bit_sender = list(self.indexing_list(send_list))
        # print("bit_receiver list")
        self.bit_receiver = list(self.indexing_list(receive_list))

    def indexing_list(self, daisy_units):
        for daisy_unit in daisy_units:
            for index in range(daisy_unit.bit_count):
                # print(f'dz={daisy_unit.description} {index}')
                yield daisy_unit, index

    def bit_to_send(self, index):
        sender, send_index = self.bit_sender[index]
        return sender.bit_to_send(send_index)

    def receive_bit(self, index, bit):
        receiver, receive_index = self.bit_receiver[index]
        receiver.receive_bit(receive_index, bit)


