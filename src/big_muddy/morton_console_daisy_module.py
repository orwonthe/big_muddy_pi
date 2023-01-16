# Copyright 2022 WillyMillsLLC
from daisy_module import DaisyModule
from daisy_unit import BlockConsoleDaisyUnit, TurnoutConsoleDaisyUnit


class MortonConsoleDaisyModule(DaisyModule):
    """ A daisy module representing a Morton County district console """

    def __init__(self):
        super().__init__("Morton", [
            BlockConsoleDaisyUnit(),
            TurnoutConsoleDaisyUnit(),
            TurnoutConsoleDaisyUnit(),
            BlockConsoleDaisyUnit(),
        ])
