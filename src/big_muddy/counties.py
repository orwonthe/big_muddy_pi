from big_muddy_districts import MORTON_COUNTY_BLOCKS, BURLEIGH_COUNTY_CUBE_RECIPES, MORTON_COUNTY_CUBE_RECIPES
from cubes import find_descriptions_and_create_cubes
from daisy_module import DaisyModule
from daisy_socket import DaisySocketCollection
from daisy_unit import BlockConsoleDaisyUnit, TurnoutConsoleDaisyUnit
from districts import DistrictConsoleMaster


# TODO: finish this

class BurleighSocketCollection(DaisySocketCollection):
    def __init__(self):
        cubes = list(find_descriptions_and_create_cubes("burleigh", BURLEIGH_COUNTY_CUBE_RECIPES))
        print(f'burleigh cube count = {len(cubes)}')
        super().__init__(cubes)


class MortonSocketCollection(DaisySocketCollection):
    def __init__(self):
        cubes = list(find_descriptions_and_create_cubes("morton", MORTON_COUNTY_CUBE_RECIPES))
        print(f'morton cube count = {len(cubes)}')
        super().__init__(cubes)


class BurleighDaisyModule(DaisyModule):
    """ A daisy module representing a Burleigh County district console """

    def __init__(self):
        super().__init__("burleigh", [
            BlockConsoleDaisyUnit(),
            TurnoutConsoleDaisyUnit(),
            BlockConsoleDaisyUnit(),
        ])


class MortonDaisyModule(DaisyModule):
    """ A daisy module representing a Morton County district console """

    def __init__(self):
        super().__init__("morton", [
            BlockConsoleDaisyUnit(),
            TurnoutConsoleDaisyUnit(),
            TurnoutConsoleDaisyUnit(),
            BlockConsoleDaisyUnit(),
        ])


class BurleighCountyMaster(DistrictConsoleMaster):
    def __init__(self):
        district_console = BurleighDaisyModule()
        daisy_socket_collection = BurleighSocketCollection()
        super().__init__(district_console, daisy_socket_collection)


class MortonCountyMaster(DistrictConsoleMaster):
    def __init__(self):
        district_console = MortonDaisyModule()
        daisy_socket_collection = MortonSocketCollection()
        super().__init__(district_console, daisy_socket_collection)


if __name__ == '__main__':
    print(MORTON_COUNTY_BLOCKS)
