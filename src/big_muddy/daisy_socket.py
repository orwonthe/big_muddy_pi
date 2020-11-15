from daisy_domain import Domain, BlockMixin, ConsoleMixin, TurnoutMixin, DomainLists


class DaisySocket(Domain):
    """ A DaisySocket is a socket on a DaisyUnit """

    def __init__(self):
        self.daisy_unit = None

    def on_add_to_daisy_unit(self, daisy_unit_socket_index):
        self.input_bits = self.daisy_unit.input_bits_per_socket
        self.output_bits = self.daisy_unit.output_bits_per_socket
        self.daisy_unit_socket_index = self.daisy_unit.add_daisy_socket(self, daisy_unit_socket_index)
        self.input_bit_start = self.input_bits * self.daisy_unit_socket_index
        self.output_bit_start = self.output_bits * self.daisy_unit_socket_index

    @property
    def action(self):
        """ User friendly description of what the daisy socket does """
        return self.purpose

    def add_to_daisy_unit(self, daisy_unit, daisy_unit_socket_index):
        """ Add self to the given daisy unit """
        if self.daisy_unit is not None:
            raise Exception("DaisySocket can only be added once to a daisy unit.")
        if not self.is_same_domain(daisy_unit):
            raise Exception("DaisySocket can only be added to daisy unit with matching domain.")
        self.daisy_unit = daisy_unit
        self.on_add_to_daisy_unit(daisy_unit_socket_index)

    def input_bit_index(self, index):
        return self.daisy_unit.input_bit_mapping(self.input_bit_start + index)

    def output_bit_index(self, index):
        return self.daisy_unit.output_bit_mapping(self.output_bit_start + index)


class DaisySocketOn8to16(DaisySocket):
    def __init__(self):
        super().__init__()

    def on_add_to_daisy_unit(self, daisy_unit_socket_index):
        super().on_add_to_daisy_unit(daisy_unit_socket_index)
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
    def __init__(self):
        super().__init__()
        self.index_input_bit0 = None
        self.index_input_bit1 = None
        self.index_output_bit0 = None

    def on_add_to_daisy_unit(self, daisy_unit_socket_index):
        super().on_add_to_daisy_unit(daisy_unit_socket_index)
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


class BlockConsoleDaisySocket(DaisySocketOn8to16, BlockMixin, ConsoleMixin):
    def __init__(self, district=None, name=None, socket_index=None, gui_index=None, color=None, row=None, column=None):
        super().__init__()
        self.district = district
        self.name = name
        self.socket_index = socket_index
        self.gui_index = gui_index
        self.color = color
        self.row = row
        self.column = column

    @property
    def moniker(self):
        return f'{self.socket_index} {self.color} {self.name}'

    @property
    def toggle_state(self):
        return 1 - self.bit1, 1 - self.bit0

    def reflect(self):
        """ Use the state of the toggle switch to control the LEDs """
        contrary, normal = self.toggle_state
        if normal:
            self.set_normal_green()
        else:
            self.set_normal_off()
        if contrary:
            self.set_contrary_green()
        else:
            self.set_contrary_off()

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


class TurnoutConsoleDaisySocket(DaisySocketOn16to8, TurnoutMixin, ConsoleMixin):
    def __init__(self, district=None, name=None, socket_index=None, gui_index=None, color=None, row=None, column=None):
        super().__init__()
        self.district = district
        self.name = name
        self.socket_index = socket_index
        self.gui_index = gui_index
        self.color = color
        self.row = row
        self.column = column

    @property
    def moniker(self):
        return f'{self.socket_index} {self.color} {self.name} {self.direction}'

    @property
    def push_button_state(self):
        return 1 - self.bit1, 1 - self.bit0

    def reflect(self):
        contrary, normal = self.push_button_state
        if normal:
            self.set_at_main()
        elif contrary:
            self.set_at_siding()

    @property
    def action(self):
        return f'{self.direction} {self.purpose}'

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


class DaisySocketCollection(DomainLists):
    def __init__(self, cubes):
        super().__init__()
        self.cubes = cubes
        for cube in cubes:
            self.append(cube)
