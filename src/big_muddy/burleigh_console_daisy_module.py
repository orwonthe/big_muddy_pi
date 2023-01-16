# Copyright 2022 WillyMillsLLC
from daisy_module import DaisyModule
from daisy_unit import BlockConsoleDaisyUnit, TurnoutConsoleDaisyUnit


class BurleighConsoleDaisyModule(DaisyModule):
    """ A daisy module representing a Burleigh County district console """

    def __init__(self):
        super().__init__("Burleigh", [
            BlockConsoleDaisyUnit(),
            TurnoutConsoleDaisyUnit(),
            BlockConsoleDaisyUnit(),
        ])
