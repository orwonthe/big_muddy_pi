class DaisySocket:
    """ A DaisySocket is a socket on a DaisyUnit """

    def __init__(self, daisy_unit=None):
        self.daisy_unit = daisy_unit
        if daisy_unit:
            self.add_to_daisy_unit(daisy_unit)

    def add_to_daisy_unit(self, daisy_unit):
        self.daisy_unit = daisy_unit
        self.input_bits = daisy_unit.input_bits_per_socket
        self.output_bits = daisy_unit.output_bits_per_socket
        self.socket_index = daisy_unit.add_daisy_socket(self)
        self.input_bit_index = self.input_bits * self.socket_index
        self.output_bit_index = self.output_bits * self.socket_index


    def input_bit_index(self, index):
        return self.daisy_unit.input_bit_mapping(self.input_bit_index + index)

    def output_bit_index(self, index):
        return self.daisy_unit.output_bit_mapping(self.output_bit_index + index)

class DaisySocketOn8to16(DaisySocket):
    def __init__(self, daisy_unit):
        super().__init__(daisy_unit)
        self.index_input_bit0 = self.input_bit_index(0)
        self.index_input_bit1 = self.input_bit_index(1)
        self.index_output_bit0 = self.output_bit_index(0)
        self.index_output_bit1 = self.output_bit_index(1)
        self.index_output_bit2 = self.output_bit_index(2)
        self.index_output_bit3 = self.output_bit_index(3)

    @property
    def bit0(self):
        return self.daisy_unit.bits_received[self.index_input_bit0]

    @property
    def bit1(self):
        return self.daisy_unit.bits_received[self.index_input_bit1]

    def send0(self, value):
        self.daisy_unit.bits_to_send[self.index_output_bit0] = value

    def send1(self, value):
        self.daisy_unit.bits_to_send[self.index_output_bit1] = value

    def send2(self, value):
        self.daisy_unit.bits_to_send[self.index_output_bit2] = value

    def send3(self, value):
        self.daisy_unit.bits_to_send[self.index_output_bit3] = value

class DaisySocketOn16to8(DaisySocket):
    def __init__(self, daisy_unit):
        super().__init__(daisy_unit)
        self.index_input_bit0 = self.input_bit_index(0)
        self.index_input_bit1 = self.input_bit_index(1)
        self.index_output_bit0 = self.output_bit_index(0)

    @property
    def bit0(self):
        return self.daisy_unit.bits_received[self.index_input_bit0]

    @property
    def bit1(self):
        return self.daisy_unit.bits_received[self.index_input_bit1]

    def send0(self, value):
        self.daisy_unit.bits_to_send[self.index_output_bit0] = value


class BlockConsoleDaisySocket(DaisySocketOn8to16):
    @property
    def toggle_state(self):
        return 1 - self.bit1, 1 - self.bit0

    def set_normal_off(self):
        self.send0(0)
        self.send1(0)

    def set_normal_green(self):
        self.send0(0)
        self.send1(1)

    def set_normal_red(self):
        self.send0(1)
        self.send1(0)

    def set_normal_yellow(self):
        self.send0(1)
        self.send1(1)

    def set_contrary_off(self):
        self.send2(0)
        self.send3(0)

    def set_contrary_green(self):
        self.send2(0)
        self.send3(1)

    def set_contrary_red(self):
        self.send2(1)
        self.send3(0)

    def set_contrary_yellow(self):
        self.send2(1)
        self.send3(1)

class TurnoutConsoleDaisySocket(DaisySocketOn16to8):
    @property
    def push_button_states(self):
        return 1 - self.bit1, 1 - self.bit0

    @property
    def main_push_button(self):
        return 1 - self.bit1

    @property
    def siding_push_button(self):
        return 1 - self.bit0

    def set_at_main(self):
        """ Indicate turnout is set for main (straight) """
        self.send0(0)

    def set_at_siding(self):
        """ Indicate turnout is set for siding (curve) """
        self.send0(1)

