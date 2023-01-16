# Copyright 2022 WillyMillsLLC
from daisy_socket import TurnoutConsoleDaisySocket


class LeftTurnoutControlCube(TurnoutConsoleDaisySocket):
    """ A turnout control cube for turnouts with the divergence to the left """

    @property
    def direction(self):
        return "left"


class RightTurnoutControlCube(TurnoutConsoleDaisySocket):
    """ A turnout control cube for turnouts with the divergence to the right """

    @property
    def direction(self):
        return "right"
