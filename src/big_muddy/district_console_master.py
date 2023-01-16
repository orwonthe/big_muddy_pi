# Copyright 2022 WillyMillsLLC
from daisy_master import DaisyMaster


class DistrictConsoleMaster(DaisyMaster):
    """ A DaisyMaster set up for a single console district """

    def __init__(self, district_console, daisy_socket_collection):
        self.district_console = district_console
        self.daisy_socket_collection = daisy_socket_collection
        super().__init__(district_console.daisy_units)
        self.set_for_action()
        self.district_console.add_sockets(daisy_socket_collection.cubes)

    @property
    def block_cubes(self):
        return sorted(self.daisy_socket_collection.block_consoles, key=lambda item: item.gui_index)

    @property
    def turnout_cubes(self):
        return sorted(self.daisy_socket_collection.turnout_consoles, key=lambda item: item.gui_index)
