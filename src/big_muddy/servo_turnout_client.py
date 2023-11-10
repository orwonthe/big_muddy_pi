# Copyright 2022 WillyMillsLLC
from daisy_domain import Domain


def create_servo_turnout_client(description):
    if description['servo_half']:
        return UpperServoTurnoutClient(description)
    else:
        return LowerServoTurnoutClient(description)


class ServoTurnoutClient(Domain):
    def __init__(self, description):
        self.description = description
        self.servo_socket = None
        self.socket_index = description['servo_socket']
        self.servo_half = description['servo_half']
        self.inverted = 1 if description.get('inverted') else 0
        self.ab_swap = 1 if description.get('ab_swap') else 0

    @property
    def name(self):
        return self.description.get('name')

    @property
    def district(self):
        return self.description.get('district')


class LowerServoTurnoutClient(ServoTurnoutClient):
    @property
    def direction(self):
        return self.servo_socket.bit0 ^ self.inverted

    def set_push(self, normal, contrary):
        if self.ab_swap:
            self.servo_socket.send1(normal)
            self.servo_socket.send0(contrary)
        else:
            self.servo_socket.send0(normal)
            self.servo_socket.send1(contrary)


class UpperServoTurnoutClient(ServoTurnoutClient):
    @property
    def direction(self):
        return self.servo_socket.bit1 ^ self.inverted

    def set_push(self, normal, contrary):
        if self.ab_swap:
            self.servo_socket.send3(normal)
            self.servo_socket.send2(contrary)
        else:
            self.servo_socket.send2(normal)
            self.servo_socket.send3(contrary)

