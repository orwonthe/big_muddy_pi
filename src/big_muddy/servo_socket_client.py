from daisy_domain import ServoMixin, BlockMixin, TurnoutMixin

from daisy_socket import DaisySocketOn8to16


class BlockServoDaisySocket(DaisySocketOn8to16, BlockMixin, ServoMixin):
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

    def set_selection(self, signal_bits):
        self.send3(signal_bits & 1)
        signal_bits //= 2
        self.send2(signal_bits & 1)
        signal_bits //= 2
        self.send1(signal_bits & 1)
        signal_bits //= 2
        self.send0(signal_bits & 1)

    def set_off(self):
        self.set_selection(8)

    def set_flash(self):
        self.set_selection(0)

    def set_x_normal(self):
        self.set_selection(1)

    def set_x_contrary(self):
        self.set_selection(7)

    def set_y_normal(self):
        self.set_selection(2)

    def set_y_contrary(self):
        self.set_selection(6)

    def set_z_normal(self):
        self.set_selection(3)

    def set_z_contrary(self):
        self.set_selection(5)

    @property
    def is_shorted(self):
        return 0 == self.bit0


class TurnoutServoDaisySocket(DaisySocketOn8to16, TurnoutMixin, ServoMixin):
    def __init__(self, district=None, name=None, socket_index=None, gui_index=None, color=None, row=None,
                 column=None):
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
