from daisy_domain import ServoMixin, TurnoutMixin

from daisy_socket import DaisySocketOn8to16


class TurnoutServoDaisySocket(DaisySocketOn8to16, TurnoutMixin, ServoMixin):
    def __init__(self, district=None, socket_index=None):
        super().__init__()
        self.district = district
        self.socket_index = socket_index
        self.lower_turnout = None
        self.upper_turnout = None

    @property
    def lower_name(self):
        return self.lower_turnout.name if self.lower_turnout else "~"

    @property
    def upper_name(self):
        return self.upper_turnout.name if self.upper_turnout else "~"

    @property
    def name(self):
        return f'{self.lower_name} {self.upper_name}'

    @property
    def moniker(self):
        return f'{self.socket_index} {self.name}'

    def add_client(self, client):
        if client.socket_half:
            if self.upper_turnout is None:
                self.upper_turnout = client
            else:
                raise Exception("ERROR: Servo Socket already has upper turnout ")
        else:
            if self.lower_turnout is None:
                self.lower_turnout = client
            else:
                raise Exception("ERROR: Servo Socket already has lower turnout ")
        client.servo_socket = self
