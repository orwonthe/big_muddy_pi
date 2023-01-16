from block_servo_tester_daisy_unit import BlockServoTesterDaisyUnit
from block_servo_tester_master import BlockServoTesterMaster
from block_servo_testing_socket import BlockServoTestingSocket
from daisy_module import DaisyModule
from daisy_unit import BlockServoDaisyUnit, Daisy8to16Unit
from servo_socket_client import BlockServoDaisySocket


class BlockServoTester(DaisyModule):
    """ The main test fixture for testing bloc servo boards """

    SERVO_SOCKET_INDEX_BY_LETTER = {
        "A": 0,
        "B": 1,
        "C": 2,
        "D": 3,
    }

    def __init__(self):
        self.servo_unit = BlockServoDaisyUnit()
        self.test_unit = BlockServoTesterDaisyUnit()
        super().__init__("Daisy Servo Module", [self.servo_unit, self.test_unit])
        self.daisy_master = BlockServoTesterMaster(self.daisy_units)
        self.servo_sockets = [BlockServoDaisySocket(socket_index=index)
                              for index in Daisy8to16Unit.SOCKETS_ABCD]
        self.test_sockets = [BlockServoTestingSocket(socket_index=index) for index in Daisy8to16Unit.SOCKETS_ABCD]
        self.add_sockets(self.servo_sockets)
        self.add_sockets(self.test_sockets)
        self.daisy_master.set_for_action()

    def _servo_socket(self, letter):
        return self.servo_sockets[self.SERVO_SOCKET_INDEX_BY_LETTER[letter]]

    def kick_start(self):
        self.daisy_master.kick_start()

    def pull_data(self):
        self.daisy_master.pull_data()

    def push_data(self):
        self.daisy_master.push_data()

    def set_is_shorted(self, value):
        self.test_sockets[0].send3(0 if value else 1)

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
                return "Normal"
        else:
            if contrary:
                return "Contrary"
            else:
                return "off"

    @property
    def go_status(self):
        return "STOP" if self.is_stop else "Go"

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
    def status_report(self):
        return [
            self.go_status,
            f'x {self.x_status}',
            f'y {self.y_status}',
            f'z {self.z_status}',
        ]

    @property
    def daisy_shorts(self):
        return ["Bang" if socket.bit1 else "Okay" for socket in self.servo_sockets]

    @property
    def daisy_nulls(self):
        return ["High" if socket.bit0 else "Low" for socket in self.servo_sockets]

    def _set_others_off(self, selected_socket):
        for socket in self.servo_sockets:
            if socket != selected_socket:
                socket.set_off()

    def set_off(self, socket_letter):
        selected_socket = self._servo_socket(socket_letter)
        selected_socket.set_off()
        self._set_others_off(selected_socket)

    def set_flash(self, socket_letter):
        selected_socket = self._servo_socket(socket_letter)
        selected_socket.set_flash()
        self._set_others_off(selected_socket)

    def set_x_normal(self, socket_letter):
        selected_socket = self._servo_socket(socket_letter)
        selected_socket.set_x_normal()
        self._set_others_off(selected_socket)

    def set_x_contrary(self, socket_letter):
        selected_socket = self._servo_socket(socket_letter)
        selected_socket.set_x_contrary()
        self._set_others_off(selected_socket)

    def set_y_normal(self, socket_letter):
        selected_socket = self._servo_socket(socket_letter)
        selected_socket.set_y_normal()
        self._set_others_off(selected_socket)

    def set_y_contrary(self, socket_letter):
        selected_socket = self._servo_socket(socket_letter)
        selected_socket.set_y_contrary()
        self._set_others_off(selected_socket)

    def set_z_normal(self, socket_letter):
        selected_socket = self._servo_socket(socket_letter)
        selected_socket.set_z_normal()
        self._set_others_off(selected_socket)

    def set_z_contrary(self, socket_letter):
        selected_socket = self._servo_socket(socket_letter)
        selected_socket.set_z_contrary()
        self._set_others_off(selected_socket)


