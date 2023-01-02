from daisy_domain import ConsoleMixin, ServoMixin
from daisy_unit import DaisyUnitDelay


class DaisyLoop:
    """ An ordered list of all the daisy units in a daisy loop (either servo or console) """

    def __init__(self):
        self.daisy_units = []
        self.delay_unit = None
        self.bit_count = 0
        self.delay = None
        self.bit_receiver = []
        self.bit_sender = []

    def show_status(self):
        """ Show the status of all the contained daisy units """
        print(f'{self.second_term} loop:')
        for daisy_unit in self.daisy_units:
            daisy_unit.show_status()

    def add_daisy_unit(self, daisy_unit):
        """ Add another daisy unit """
        if self.delay is not None:
            raise Exception("ERROR: Cannot add units once delay is fixed.")
        self.daisy_units.append(daisy_unit)
        self.bit_count += daisy_unit.bit_count

    def add_delay(self, delay):
        """
        If needed, add a delay unit to have same duration as other loop

        :param delay: positive if this loop is too short, negative if this loop is longer and needs no delay
        """
        if self.delay is not None:
            raise Exception("ERROR: Can only set delay once.")
        if delay > 0:
            self.delay = delay
            self.bit_count += delay
            # Delay unit handles the fact that there are more bits in a cycle than physical shift registers.
            self.delay_unit = DaisyUnitDelay(delay)
        else:
            self.delay = 0

    def set_for_action(self):
        """ Once all the units are added and delay is known, organize for the task of sending and receiving data bits"""
        if self.delay is None:
            raise Exception("ERROR: Can only set for action once delay is known.")
        if self.delay_unit:
            send_list = [self.delay_unit] + self.daisy_units
            receive_list = self.daisy_units + [self.delay_unit]
        else:
            send_list = self.daisy_units
            receive_list = self.daisy_units
        self.bit_sender = list(self.indexing_list(send_list))
        self.bit_receiver = list(self.indexing_list(receive_list))

    def indexing_list(self, daisy_units):
        """ Create an order list of tuples for daisy unit and bit index within the unit """
        for daisy_unit in daisy_units:
            for index in range(daisy_unit.bit_count):
                yield daisy_unit, index

    def bit_to_send(self, index):
        """
        Given an index to a bit somewhere in the loop, find the daisy unit and the bit to send within it.
        This is how the DaisyMaster knows what to put on the GPIO output pin.

        :param index: which bit of all the hundreds of bits is requested?
        :return: value of the bit at that location
        """
        sender, send_index = self.bit_sender[index]
        return sender.bit_to_send(send_index)

    def receive_bit(self, index, bit):
        """
        Given an index to a bit somewhere in the loop, find the daisy unit and the bit to send within it.
        This is how the DaisyMaster stores the bit it just read from the GPIO input pin.

        :param index: which bit of all the hundreds of bits is being set ?
        :param bit: value to set
        """
        receiver, receive_index = self.bit_receiver[index]
        receiver.receive_bit(receive_index, bit)


class ConsoleDaisyLoop(DaisyLoop, ConsoleMixin):
    """ A DaisyLoop for all daisy units connected to the console loop """
    pass


class ServoDaisyLoop(DaisyLoop, ServoMixin):
    """ A DaisyLoop for all daisy units connected to the servo loop """
    pass
