from big_muddy_districts import BURLEIGH_COUNTY_CUBE_RECIPES, MORTON_COUNTY_CUBE_RECIPES
from cubes import generate_cubes_from_descriptions
from daisy_module import DaisyModule
from daisy_socket import DaisySocketCollection
from daisy_unit import BlockConsoleDaisyUnit, TurnoutConsoleDaisyUnit
from districts import DistrictConsoleMaster


class BurleighSocketCollection(DaisySocketCollection):
    """ Collection of cubes for Burleigh County console """

    def __init__(self):
        cubes = list(generate_cubes_from_descriptions("Burleigh", BURLEIGH_COUNTY_CUBE_RECIPES))
        super().__init__(cubes)


class MortonSocketCollection(DaisySocketCollection):
    """ Collection of cubes for Morton County console """

    def __init__(self):
        cubes = list(generate_cubes_from_descriptions("Morton", MORTON_COUNTY_CUBE_RECIPES))
        super().__init__(cubes)


class BurleighDaisyModule(DaisyModule):
    """ A daisy module representing a Burleigh County district console """

    def __init__(self):
        super().__init__("Burleigh", [
            BlockConsoleDaisyUnit(),
            TurnoutConsoleDaisyUnit(),
            BlockConsoleDaisyUnit(),
        ])


class MortonDaisyModule(DaisyModule):
    """ A daisy module representing a Morton County district console """

    def __init__(self):
        super().__init__("Morton", [
            BlockConsoleDaisyUnit(),
            TurnoutConsoleDaisyUnit(),
            TurnoutConsoleDaisyUnit(),
            BlockConsoleDaisyUnit(),
        ])


class BurleighCountyMaster(DistrictConsoleMaster):
    """ DaisyMaster for Burleigh County """

    def __init__(self):
        district_console = BurleighDaisyModule()
        daisy_socket_collection = BurleighSocketCollection()
        super().__init__(district_console, daisy_socket_collection)


class MortonCountyMaster(DistrictConsoleMaster):
    """ DaisyMaster for Morton County """

    def __init__(self):
        district_console = MortonDaisyModule()
        daisy_socket_collection = MortonSocketCollection()
        super().__init__(district_console, daisy_socket_collection)
