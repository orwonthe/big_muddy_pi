class DaisyUnit:
    """
    A software DaisyUnit os the software companion to a hardware daisy unit.

    Each unit is embedded in a daisy chain of units that loop from the controlling
    raspberry pi machine, through several chained unit, then back to the pi.
    There are two loops.
    A console loop connects all the consoles.
    The servo loop connects all the servocs.
    Each daisy unit consists of 24 bits (3 bytes) of data that is looped in a serial fashion.
    Depending on the unit, each byte may be either input or output.
    """

    def __init__(self, is_console, is_block):
        """

        :param is_console: console (True) or servo (False)
        :param is_block: block (True) or turnout (False)
        """
        self.bits_to_send = [0] * 24  # 24 bit output buffer
        self.bits_received = [0] * 24  # 24 bit input buffer
        self.is_console = is_console
        self.is_block = is_block

    def show_status(self):
        # print("bits_to_send ", self.bits_to_send)
        print("bits_received", self.bits_received)

    @property
    def description(self):
        return "block" if self.is_block else "turnout"

    @property
    def bit_count(self):
        return 24

    @property
    def is_servo(self):
        return not self.is_console

    @property
    def is_turnout(self):
        return not self.is_block

    @property
    def input_bit_count(self):
        return self.socket_count * self.input_bits_per_socket

    @property
    def output_bit_count(self):
        return self.socket_count * self.output_bits_per_socket

    def bit_to_send(self, index):
        return self.bits_to_send[index]

    def receive_bit(self, index, bit):
        # print(f'self.bits_received[{index}] = {bit}')
        self.bits_received[index] = bit

    def set_to_send(self, index, value):
        """
        Sets one output bit to value to send on next cycle.
        :param index: which output bit
        :param value:  value (0 or 1) to send
        """
        mapping = self.output_map[index]
        # print(f"set to send({index}, {value}) --> {mapping}")
        self.bits_to_send[mapping] = value

    def get_to_send(self, index):
        """
        Retrieves current value of output bit for next cycle.
        :param index: which output bit
        :return: current value
        """
        return self.bits_to_send[self.output_map[index]]

    def get_was_sent(self, index):
        """
        Retrieves prior value of output bit sent on previous cycle and then returned back.
        For properly functioning hardware, this will be identical to what was sent.
        :param index: which output bit
        :return: current value
        """
        return self.bits_received[self.output_map[index]]

    def get_received(self, index):
        """
        Retrieves value received for input bit at last cycle.
        :param index: which input bit
        :return: current value of bit
        """
        return self.bits_received[self.input_map[index]]


class Daisy8to16Unit(DaisyUnit):
    """ Daisy unit with 8 inputs (switches and sensors) and 16 outputs (LEDs and relays) """
    def __init__(self, is_console, is_block):
        super().__init__(is_console, is_block)
        self.output_map = [8 + index for index in range(16)]
        self.input_map = [index for index in range(8)]
        self.socket_count = 4
        self.input_bits_per_socket = 2
        self.output_bits_per_socket = 4


class Daisy16to8Unit(DaisyUnit):
    """ Daisy unit with 16 inputs (switches and sensors) and 8 outputs (LEDs and relays) """
    def __init__(self, is_console, is_block):
        super().__init__(is_console, is_block)
        self.output_map = [index for index in range(8)]
        self.input_map = [8 + index for index in range(16)]
        self.socket_count = 8
        self.input_bits_per_socket = 2
        self.output_bits_per_socket = 1


class BlockConsoleDaisyUnit(Daisy8to16Unit):
    """ Daisy unit with 4 sockets for 4 block control console cubes """
    def __init__(self):
        super().__init__(True, True)


class TurnoutConsoleDaisyUnit(Daisy16to8Unit):
    """ Daisy unit with 8 sockets for 8 turnout console cubes """
    def __init__(self):
        super().__init__(True, False)

class DaisyUnitDelay:
    def __init__(self, delay_count):
        self.index = 0
        self.delay_count = delay_count

    @property
    def description(self):
        return "delay"

    @property
    def bit_count(self):
        return self.delay_count

    def bit_to_send(self, index):
        return 0

    def receive_bit(self, index, bit):
        pass

