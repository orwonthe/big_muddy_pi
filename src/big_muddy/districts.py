from daisy_master import DaisyMaster


class District:
    """ A district is an object that knows what district it is. """
    pass


def normalize(district, purpose, cube_dictionary_list):
    """ Add various entries to a cube dictionary and sort by socket index """
    for gui_index, cube_dictionary in enumerate(cube_dictionary_list):
        cube_dictionary["district"] = district
        cube_dictionary["purpose"] = purpose
        cube_dictionary["gui_index"] = gui_index  # Dictionary is given in a natural gui display order. Remember it.
    return sorted(cube_dictionary_list, key=lambda item: item["socket"])


class DistrictConsoleMaster(DaisyMaster):
    """ A DaisyMaster set up for a single console district """

    def __init__(self, district_console, daisy_socket_collection):
        self.district_console = district_console
        self.daisy_socket_collection = daisy_socket_collection
        super().__init__(district_console.daisy_units)
        self.set_for_action()
        self.add_sockets(daisy_socket_collection.cubes)

    @property
    def block_cubes(self):
        return sorted(self.daisy_socket_collection.block_consoles, key=lambda item: item.gui_index)

    @property
    def turnout_cubes(self):
        return sorted(self.daisy_socket_collection.turnout_consoles, key=lambda item: item.gui_index)
