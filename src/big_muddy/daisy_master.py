from big_muddy_io import BigMuddyIO
from daisy_loop import ServoDaisyLoop, ConsoleDaisyLoop
import logging

class DaisyMaster:
    """ DaisyMaster has two DaisyLoop and is in charger of communicating with the hardware. """

    def __init__(self, daisy_units=None):
        self.__set_for_action = False
        self.big_muddy_io = BigMuddyIO.system()
        self.servo_loop = ServoDaisyLoop()
        self.console_loop = ConsoleDaisyLoop()
        if daisy_units:
            self.add_daisy_units(daisy_units)

    def set_for_action(self):
        """ Do the one time setup of locating all the bits and balancing the delays (call exactly once). """
        if self.__set_for_action:
            raise Exception("Can only set daisy master for action once.")
        initial_console_bits = self.console_loop.bit_count
        initial_servo_bits = self.servo_loop.bit_count
        self.bit_count = max(initial_console_bits, initial_servo_bits)
        print(f"bit count={self.bit_count} console={initial_console_bits} servo={initial_servo_bits}")
        self.console_loop.add_delay(initial_servo_bits - initial_console_bits)
        self.servo_loop.add_delay(initial_console_bits - initial_servo_bits)
        self.console_loop.set_for_action()
        self.servo_loop.set_for_action()
        self.__set_for_action = True

    def add_daisy_units(self, daisy_units):
        """ Add daisy units to the loop on which they belong."""
        for daisy_unit in daisy_units:
            self.add_daisy_unit(daisy_unit)

    def add_daisy_unit(self, daisy_unit):
        """ Add daisy unit to the loop on which it belongs."""
        if daisy_unit.is_console:
            self.console_loop.add_daisy_unit(daisy_unit)
        else:
            self.servo_loop.add_daisy_unit(daisy_unit)

    def bits_to_send(self, index):
        """ Retrieve the indexed servo and console loop bits. """
        return self.console_loop.bit_to_send(index), self.servo_loop.bit_to_send(index)

    def receive_bits(self, index, console_bit, servo_bit):
        """ Store the received console and servo bits at the indexed location of the respective loops. """
        self.console_loop.receive_bit(index, console_bit)
        self.servo_loop.receive_bit(index, servo_bit)

    def pull_data(self):
        """ Grab the actual data from the hardware. """
        self.big_muddy_io.loading.pulse()
        self._transfer_data()

    def kick_start(self):
        """ Redundant load pulse ensures valid data read when not in continuous cycle """
        self.big_muddy_io.loading.pulse()

    def push_data(self):
        """ Transfer data to the actual hardware. """
        self._transfer_data()
        self.big_muddy_io.loading.pulse()

    def _transfer_data(self):
        """ Do the serial data shifting sans load pulse. """
        if not self.__set_for_action:
            raise Exception("No data transfer allowed before DaisyMaster is set for action.")
        for index in range(self.bit_count):
            console_bit_to_send, servo_bit_to_send = self.bits_to_send(index)
            data = self.big_muddy_io.read_data()
            console_bit_received = data[0]
            servo_bit_received = data[1]
            logging.debug('index=%2d sending %d %d', index, console_bit_to_send, servo_bit_to_send)
            logging.debug('index=%2d getting %d %d', index, console_bit_received, servo_bit_received)
            self.receive_bits(index, console_bit_received, servo_bit_received)
            self.big_muddy_io.write_data([console_bit_to_send, servo_bit_to_send])
            self.big_muddy_io.shifting.pulse()

    def show_status(self):
        """ Show the status of the two loops """
        self.console_loop.show_status()
        self.servo_loop.show_status()
