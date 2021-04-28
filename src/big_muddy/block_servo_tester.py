from daisy_domain import BlockMixin, ConsoleMixin
from daisy_master import DaisyMaster
from daisy_module import DaisyModule
from daisy_socket import DaisySocketOn8to16
from daisy_unit import BlockServoDaisyUnit, BlockConsoleDaisyUnit, Daisy8to16Unit
from servo_socket_client import BlockServoDaisySocket


class BlockServoTesterDaisyUnit(BlockConsoleDaisyUnit):
    """ Tester uses any 8to16 unit but should be hooked up on console loop """
    pass


class BlockServoTestingSocket(DaisySocketOn8to16, BlockMixin, ConsoleMixin):
    """ Test fixture uses 4 of these sockets """

    def __init__(self, socket_index):
        self.socket_index = socket_index
        super().__init__()


class BlockServoTester(DaisyModule):
    """ The main test fixture for testing bloc servo boards """

    def __init__(self, using_upper_half):
        self.using_upper_half = using_upper_half
        self.servo_unit = BlockServoDaisyUnit()
        self.test_unit = BlockServoTesterDaisyUnit()
        super().__init__("Daisy Servo Module", [self.servo_unit, self.test_unit])
        self.daisy_master = BlockServoTesterMaster(self.daisy_units)
        self.servo_sockets = [BlockServoDaisySocket(socket_index=index)
                              for index in [Daisy8to16Unit.SOCKET_A, Daisy8to16Unit.SOCKET_B]]
        self.test_sockets = [BlockServoTestingSocket(socket_index=index) for index in Daisy8to16Unit.SOCKETS_ABCD]
        self.add_sockets(self.servo_sockets)
        self.add_sockets(self.test_sockets)
        self.choose_client_socket(self.using_upper_half)
        self.daisy_master.set_for_action()

    def choose_client_socket(self, using_upper_half):
        client_socket_index = 1 if using_upper_half else 0
        non_client_socket_index = 0 if using_upper_half else 1
        self.client_socket = self.servo_sockets[client_socket_index]
        self.non_client_socket = self.servo_sockets[non_client_socket_index]

    def kick_start(self):
        self.daisy_master.kick_start()

    def push_data(self):
        self.daisy_master.push_data()

    def set_is_shorted(self, value):
        self.test_sockets[0].send3(0 if value else 1)

    @property
    def is_shorted(self):
        return self.client_socket.is_shorted

    @property
    def is_stop(self):
        return not self.test_sockets[0].bit1

    @property
    def is_x_normal(self):
        return not self.test_sockets[1].bit1

    @property
    def is_y_normal(self):
        return not self.test_sockets[1].bit0

    @property
    def is_z_normal(self):
        return not self.test_sockets[2].bit0

    @property
    def is_z_contrary(self):
        return not self.test_sockets[2].bit1

    @property
    def is_y_contrary(self):
        return not self.test_sockets[3].bit0

    @property
    def is_x_contrary(self):
        return not self.test_sockets[3].bit1

    def _status(self, normal, contrary):
        if normal:
            if contrary:
                return "BROKEN"
            else:
                return "normal"
        else:
            if contrary:
                return "contrary"
            else:
                return "off"

    @property
    def on_status(self):
        return "Stop" if self.is_stop else "Go"

    @property
    def x_status(self):
        return self._status(self.is_x_normal, self.is_x_contrary)

    @property
    def y_status(self):
        return self._status(self.is_y_normal, self.is_y_contrary)

    @property
    def z_status(self):
        return self._status(self.is_z_normal, self.is_z_contrary)

    @property
    def short_status(self):
        return "SHORTED" if self.is_shorted else "no short"

    @property
    def status_report(self):
        return [
            self.on_status,
            self.short_status,
            f'x {self.x_status}',
            f'y {self.y_status}',
            f'z {self.z_status}',
        ]

    def set_off(self):
        self.client_socket.set_off()
        self.non_client_socket.set_off()

    def set_flash(self):
        self.client_socket.set_flash()
        self.non_client_socket.set_off()

    def set_x_normal(self):
        self.client_socket.set_x_normal()
        self.non_client_socket.set_off()

    def set_x_contrary(self):
        self.client_socket.set_x_contrary()
        self.non_client_socket.set_off()

    def set_y_normal(self):
        self.client_socket.set_y_normal()
        self.non_client_socket.set_off()

    def set_y_contrary(self):
        self.client_socket.set_y_contrary()
        self.non_client_socket.set_off()

    def set_z_normal(self):
        self.client_socket.set_z_normal()
        self.non_client_socket.set_off()

    def set_z_contrary(self):
        self.client_socket.set_z_contrary()
        self.non_client_socket.set_off()


class BlockServoTesterMaster(DaisyMaster):
    """ Defines setup for testing block servo controller board """

    def __init__(self, daisy_units):
        super().__init__(daisy_units)
