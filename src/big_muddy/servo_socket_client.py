from daisy_domain import ServoMixin, BlockMixin, TurnoutMixin

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


class TurnoutServoDaisySocket(DaisySocketOn8to16, TurnoutMixin, ServoMixin):
    def __init__(self, district=None, socket_index=None):
        super().__init__()
        self.district = district
        self.socket_index = socket_index
        self.lower_turnout = None
        self.upper_turnout = None

    @property
    def lower_name(self):
        return self.lower_turnout.name if self.lower_turnout else "~"

    @property
    def upper_name(self):
        return self.upper_turnout.name if self.upper_turnout else "~"

    @property
    def name(self):
        return f'{self.lower_name} {self.upper_name}'

    @property
    def moniker(self):
        return f'{self.socket_index} {self.name}'

    def add_client(self, client):
        if client.socket_half:
            if self.upper_turnout is None:
                self.upper_turnout = client
            else:
                raise Exception("ERROR: Servo Socket already has upper turnout ")
        else:
            if self.lower_turnout is None:
                self.lower_turnout = client
            else:
                raise Exception("ERROR: Servo Socket already has lower turnout ")
        client.servo_socket = self
