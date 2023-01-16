# Copyright 2022 WillyMillsLLC
from daisy_module import DaisyModule
from daisy_unit import TurnoutServoDaisyUnit


class BurleighTurnoutServoDaisyModule(DaisyModule):
    """ A daisy module representing the Burleigh County turnout servo"""

    def __init__(self):
        super().__init__("Burleigh Turnout Servos", [
            TurnoutServoDaisyUnit(),
        ])
