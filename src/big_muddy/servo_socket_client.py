from big_muddy.daisy_domain import ServoMixin
from big_muddy.socket_client import SocketClient


class ServoSocketClient(SocketClient, ServoMixin):
    def __init__(self, district=None, name=None, socket_index=None, gui_index=None):
        """

        :param district: a SocketClient object represents a physical division of the railroad
        :param name: the name of the cube for user display
        :param socket_index: The index specifying which available socket is used to connect this cube.
        :param gui_index: The index of the cube in the console's master list.
        """
        super().__init__(district, name, socket_index, gui_index)
