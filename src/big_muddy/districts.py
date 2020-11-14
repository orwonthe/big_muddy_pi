from daisy_master import DaisyMaster


def normalize(district, purpose, cube_dictionary_list):
    for gui_index, cube_dictionary in enumerate(cube_dictionary_list):
        cube_dictionary["district"] = district
        cube_dictionary["purpose"] = purpose
        cube_dictionary["gui_index"] = gui_index
    return sorted(cube_dictionary_list, key= lambda item: item["socket"])

class DistrictConsoleMaster(DaisyMaster):
    def __init__(self, district_console):
        self.district_console = district_console
        super().__init__(district_console.daisy_units)
        self.set_for_action()

