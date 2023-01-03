from big_muddy_io import BigMuddyIO


class WideClientConnector:
    # Test jig hooks output bit to clock of binary counter.
    # Input bits read lowest two bits of counter.
    # Connection tests that the input bits form a binary sequence ...0,1,2,3,0,1,...
    client_names = ["A1", "A2", "B3", "B4", "C5", "C6", "D7", "D8"]

    def __init__(self):
        big_muddy_io = BigMuddyIO.system()
        self.big_muddy_io = big_muddy_io
        self.big_muddy_io.set_data_pins(0)

    def check_client(self, connector):
        self.connector = connector
        self.gather_bits()
        self.report_bits()

    @property
    def client_index(self):
        return self.connector - 1

    @property
    def client_name(self):
        return self.client_names[self.client_index]

    @property
    def client_description(self):
        return self.client_name + " on connector " + str(self.connector)

    def gather_bits(self, cycles=8):
        self.bits = []
        for cycle in range(cycles):
            self.bit_cycle()

    def bit_cycle(self):
        # set only client out bit high
        for out_bit_index in range(8):
            bit_to_send = 1 if out_bit_index == self.client_index else 0
            self.big_muddy_io.consoles.write(bit_to_send)
            self.big_muddy_io.shifting.timed_pulse()
        self.big_muddy_io.consoles.write(0)
        self.big_muddy_io.shifting.timed_pulse(16)

        # set all client out bits low
        self.big_muddy_io.loading.timed_pulse()
        self.big_muddy_io.shifting.timed_pulse(24)

        # read result
        self.big_muddy_io.loading.timed_pulse()
        self.big_muddy_io.shifting.timed_pulse(8)
        for in_client_index in range(8):
            number = 0
            for bit_index in range(2):
                bit_read = self.big_muddy_io.consoles.read()
                number += bit_read << bit_index
                self.big_muddy_io.shifting.timed_pulse()
            if self.client_index == in_client_index:
                self.bits.append(number)

    def report_bits(self):
        print(self.client_description, self.bits, self.status)

    @property
    def status(self):
        if self.bits_show_count():
            return "properly connected"
        else:
            return "BROKEN"

    def bits_show_count(self):
        for index in range(1, len(self.bits)):
            if (self.bits[index - 1] + 1) % 4 != self.bits[index]:
                return False
        return True


def wide_client_connector_test(connector):
    return WideClientConnector().check_client(connector)
