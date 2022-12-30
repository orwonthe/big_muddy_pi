# Copyright 2022 WillyMillsLLC
from counties import BurleighDaisyModule, BurleighSocketCollection, MortonDaisyModule, MortonSocketCollection
from daisy_master import DaisyMaster

DEFAULT_CONSOLE_RECIPE = "MBMBMB"

class OperationsMaster(DaisyMaster):
    """ A DaisyMaster set up to operate the full railroad """

    def __init__(self, console_recipe=DEFAULT_CONSOLE_RECIPE):
        super().__init__()
        self.modules = []
        self.socket_collections = []
        self.consoles = []
        self.apply_console_recipe(console_recipe)
        self.set_for_action()
        self.add_sockets_to_consoles()

    def add_console(self, daisy_module, socket_collection):
        self.modules.append(daisy_module)
        self.socket_collections.append(socket_collection)
        self.consoles.append((daisy_module, socket_collection))

    def apply_console_recipe(self, console_recipe):
        for letter in console_recipe:
            if letter == 'M':
                self.add_console(
                    BurleighDaisyModule(),
                    BurleighSocketCollection()
                )
            elif letter == 'B':
                self.add_console(
                    MortonDaisyModule(),
                    MortonSocketCollection()
                )

    def add_sockets_to_consoles(self):
        for module, sockets in self.consoles:
            module.add_sockets(sockets)

