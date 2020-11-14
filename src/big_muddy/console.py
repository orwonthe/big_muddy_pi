from daisy_domain import ConsoleMixin
from socket_client import SocketClient


class ConsoleCube(SocketClient, ConsoleMixin):
    def __init__(self, district=None, name=None, socket_index=None, gui_index=None, color=None, row=None, column=None):
        """

        :param district: a SocketClient object represents a physical division of the railroad
        :param name: the name of the cube for user display
        :param color: the color key(s) for the map of the railroad. Turnouts sometimes have two.
        :param row: The row of the console containing this cube.
        :param column: The column of the console containing this cube.
        :param socket_index: The index specifying which available socket is used to connect this cube.
        :param gui_index: The index of the cube in the console's master list.
        """
        super().__init__(district, name, socket_index, gui_index)
        self.color = color
        self.row = row
        self.column = column
