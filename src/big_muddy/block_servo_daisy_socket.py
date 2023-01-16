# Copyright 2022 WillyMillsLLC
from daisy_domain import BlockMixin, ServoMixin
from daisy_socket import DaisySocketOn8to16


class BlockServoDaisySocket(DaisySocketOn8to16, BlockMixin, ServoMixin):
    def __init__(self, district=None, name=None, socket_index=None):
        super().__init__()
        self.district = district
        self.name = name
        self.socket_index = socket_index

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
        self.set_selection(0)

    def set_flash(self):
        self.set_selection(8)

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
