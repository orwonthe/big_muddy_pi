from big_muddy_districts import MORTON_COUNTY_CUBE_RECIPES
from burleigh_console_socket_collection import BurleighConsoleSocketCollection
from cubes import generate_cubes_from_descriptions
from daisy_module import DaisyModule
from daisy_socket import DaisySocketCollection
from daisy_unit import BlockConsoleDaisyUnit, TurnoutConsoleDaisyUnit, TurnoutServoDaisyUnit
from districts import DistrictConsoleMaster


class MortonConsoleSocketCollection(DaisySocketCollection):
    """ Collection of cubes for Morton County console """

    def __init__(self):
        cubes = list(generate_cubes_from_descriptions("Morton", MORTON_COUNTY_CUBE_RECIPES))
        super().__init__(cubes)


class BurleighTurnoutServoDaisyModule(DaisyModule):
    """ A daisy module representing the Burleigh County turnout servo"""

    def __init__(self):
        super().__init__("Burleigh Turnout Servos", [
            TurnoutServoDaisyUnit(),
        ])


class BurleighConsoleDaisyModule(DaisyModule):
    """ A daisy module representing a Burleigh County district console """

    def __init__(self):
        super().__init__("Burleigh", [
            BlockConsoleDaisyUnit(),
            TurnoutConsoleDaisyUnit(),
            BlockConsoleDaisyUnit(),
        ])


class MortonConsoleDaisyModule(DaisyModule):
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
        district_console = BurleighConsoleDaisyModule()
        daisy_socket_collection = BurleighConsoleSocketCollection()
        super().__init__(district_console, daisy_socket_collection)


class MortonCountyMaster(DistrictConsoleMaster):
    """ DaisyMaster for Morton County """

    def __init__(self):
        district_console = MortonConsoleDaisyModule()
        daisy_socket_collection = MortonConsoleSocketCollection()
        super().__init__(district_console, daisy_socket_collection)
