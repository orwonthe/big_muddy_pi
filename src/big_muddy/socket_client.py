from daisy_domain import Domain


class SocketClient(Domain):
    """
    A socket client here is intended as a one to one match for a physical socket on some daisy unit.

    The input/output sense of the console cube is opposite of the matching physical socket.
    An input (Led, control signal, etc) on the physical socket is an input of the physical cube
     but an output of the software socket.
    An output on the physical socket (switch, short detector, etc) is an output of the physical cube
     but an input of the software socket.

    """

    def __init__(self, district=None, name=None, socket_index=None, gui_index=None):
        """

        :param district: a SocketClient object represents a physical division of the railroad
        :param name: the name of the cube for user display
        :param socket_index: The index specifying which available socket is used to connect this cube.
        :param gui_index: The index of the cube in the console's master list.
        """
        self.district = district
        self.name = name
        self.socket_index = socket_index
        self.gui_index = gui_index
        # TODO: consider using lambda functions for read/write access
        self.daisy_unit = None  # Will get set to point to the daisy unit containing this cube.
        self.input_bit_index = None  # Will get set to the index of the first input bit within the daisy unit.
        self.output_bit_index = None  # Will get set to the index of the first output bit within the daisy unit.

    # @property
    # def full_name(self):
    #     """ User friendly full name of the cube """
    #     return f'{self.district.name} {self.short_name}'
    #
    # @property
    # def short_name(self):
    #     """ User friendly name (sans county) of the cube """
    #     return f'{self.name} {self.color}'
    #
    # @property
    # def action(self):
    #     """ User friendly description of what the cube does """
    #     return self.purpose

    # def find_daisy_unit(self, daisy_units):
    #     """ In the list of daisy units, find the right one and set up read/write access to it """
    #     remaining_socket_index = self.socket_index
    #     for daisy_unit in daisy_units:
    #         if self.is_my_kind_of_daisy_unit(daisy_unit):
    #             if remaining_socket_index < daisy_unit.socket_count:
    #                 self.daisy_unit = daisy_unit
    #                 self.input_bit_index = remaining_socket_index * daisy_unit.input_bits_per_socket
    #                 self.output_bit_index = remaining_socket_index * daisy_unit.output_bits_per_socket
    #                 break
    #             else:
    #                 remaining_socket_index -= daisy_unit.socket_count
    #
