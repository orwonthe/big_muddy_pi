from clocking_checker import ClockingChecker
from daisy_module import DaisyModule
from daisy_unit import BlockServoDaisyUnit, Daisy8to16Unit
from servo_cycler_master import ServoCycleMaster
from block_servo_daisy_socket import BlockServoDaisySocket
import logging


class ServoCycler(DaisyModule):
    """ The main test fixture for testing bloc servo boards """

    def __init__(self):
        ClockingChecker.set_raise_clock_exceptions(False)
        self.pattern = 0
        self.servo_unit = BlockServoDaisyUnit()
        super().__init__("Daisy Servo Module", [self.servo_unit])
        self.daisy_master = ServoCycleMaster(self.daisy_units)
        self.servo_sockets = [BlockServoDaisySocket(socket_index=index)
                              for index in Daisy8to16Unit.SOCKETS_ABCD]
        self.add_sockets(self.servo_sockets)
        self.daisy_master.set_for_action()

    def cycle(self, count):
        # self.pattern = 0;
        self.daisy_master.kick_start()
        while count != 0:
            count -= 1
            logging.debug('cycle=%d', self.pattern)
            offset = 0
            for socket in self.servo_sockets:
                socket.set_selection(self.pattern + offset)
                offset += 1
            self.pattern += 1
            self.daisy_master.push_data()


