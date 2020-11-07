from big_muddy.daisy_unit import DaisyUnitDelay


class DaisyLoop:
    def __init__(self):
        self.daisy_units = []
        self.delay_unit = None
        self.bit_count = 0
        self.delay = None
        self.bit_receiver = []
        self.bit_sender = []

    def show_status(self):
        for daisy_unit in self.daisy_units:
            daisy_unit.show_status()

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
