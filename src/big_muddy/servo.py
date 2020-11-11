from big_muddy.daisy_domain import ServoMixin
from big_muddy.socket_client import SocketClient


class ServoSocketClient(SocketClient, ServoMixin):
    pass


class BlockControlServoSocket(ServoSocketClient):
    """
    A block control servo socket controls an electrically isolated set of tracks.

    Each block has, in a somewhat arbitrary manner, been designated with a natural
    or contrary direction. On the actual railroad this would correspond to east or west bound etc.

    A block servo can direct, via solid state relays, which power controller is connected to a block of track.
    The servo can choose one of three controllers (X, Y, or Z).
    The servo also controls the direction, normal or contrary, of the connection.

    The servo receives on feedback bit, normally 1, but goes to zero if a short circuit is detected.

    """

    def __init__(self, district=None, name=None, socket_index=None, gui_index=None):
        super().__init__(district, name, socket_index, gui_index)

    @property
    def is_console(self):
        return False

    @property
    def purpose(self):
        """ Indicate that this cube is for block control """
        return "block"

    def set_selection(self, signal_bits):
        self.daisy_unit.set_to_send(self.output_bit_index, signal_bits & 1)
        signal_bits //= 2
        self.daisy_unit.set_to_send(self.output_bit_index + 1, 0)
        signal_bits //= 2
        self.daisy_unit.set_to_send(self.output_bit_index + 2, signal_bits & 1)
        signal_bits //= 2
        self.daisy_unit.set_to_send(self.output_bit_index + 3, signal_bits & 1)

    def set_off(self):
        self.set_selection(8)

    def set_x_normal(self):
        self.set_selection(1)

    def set_x_contrary(self):
        self.set_selection(6)

    def set_y_normal(self):
        self.set_selection(2)

    def set_y_contrary(self):
        self.set_selection(5)

    def set_z_normal(self):
        self.set_selection(3)

    def set_z_contrary(self):
        self.set_selection(4)

    def get_is_shorted(self):
        0 == self.daisy_unit.get_received(self.input_bit_index)
