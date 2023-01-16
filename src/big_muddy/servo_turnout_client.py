# Copyright 2022 WillyMillsLLC
class ServoTurnoutClient:
    def __init__(self, description):
        self.description = description
        self.servo_socket = None
        self.socket_index = description['servo_socket']


def create_servo_turnout_client(description):
    if description['servo_half']:
        return UpperServoTurnoutClient(description)
    else:
        return LowerServoTurnoutClient(description)


class LowerServoTurnoutClient(ServoTurnoutClient):
    pass


class UpperServoTurnoutClient(ServoTurnoutClient):
    pass
