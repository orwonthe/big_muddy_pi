from daisy_master import DaisyMaster

from big_muddy.big_muddy_districts import MORTON_COUNTY_BLOCKS
from big_muddy.cubes import BlockControlCube, RightTurnoutControlCube, LeftTurnoutControlCube
from big_muddy.daisy_module import DaisyModule
from big_muddy.daisy_unit import BlockConsoleDaisyUnit, TurnoutConsoleDaisyUnit
from big_muddy.districts import DistrictMaster


def create_burleigh_console_module(name="burleigh"):
    return DaisyModule(name, [
        [
            BlockConsoleDaisyUnit(),
            TurnoutConsoleDaisyUnit(),
            BlockConsoleDaisyUnit(),
        ]
    ])

def create_morton_console_module(name="morton"):
    return DaisyModule(name, [
        [
            BlockConsoleDaisyUnit(),
            TurnoutConsoleDaisyUnit(),
            TurnoutConsoleDaisyUnit(),
            BlockConsoleDaisyUnit(),
        ]
    ])

def create_burleigh_console():
    return BurleighCountyConsole()


def create_morton_console():
    return MortonCountyConsole()


class CountyConsole:
    """
    County console is dedicated to one half of the railroad.

    The console consists of a 6 row and 9 column panel of cubes.

    """

    def __init__(self, name, block_cubes, turnout_cubes, daisy_units):
        """

        :param name: district name
        :param block_cubes: list of block control cubes
        :param turnout_cubes: list of turnout control cubes
        :param daisy_units:  list of associated daisy units
        """
        self.name = name
        self.block_cubes = block_cubes
        self.turnout_cubes = turnout_cubes
        self.daisy_units = daisy_units
        self.block_daisy_units = [daisy_unit for daisy_unit in daisy_units if daisy_unit.is_block]
        self.turnout_daisy_units = [daisy_unit for daisy_unit in daisy_units if not daisy_unit.is_block]
        for index, cube in enumerate(self.cubes):
            cube.district = self
            cube.index = index
            cube.find_daisy_unit(daisy_units)

    @property
    def cubes(self):
        return self.block_cubes + self.turnout_cubes

    def reflect(self):
        for cube in self.cubes:
            cube.reflect()


class BurleighCountyConsole(CountyConsole):
    def __init__(self):
        super().__init__(
            "Burleigh",
            create_burleigh_county_block_cubes(),
            create_burleigh_county_turnout_cubes(),
            [
                BlockConsoleDaisyUnit(),
                TurnoutConsoleDaisyUnit(),
                BlockConsoleDaisyUnit(),
            ]
        )


class MortonCountyConsole(CountyConsole):
    def __init__(self):
        super().__init__(
            "Morton",
            create_morton_county_block_cubes(),
            create_morton_county_turnout_cubes(),
            [
                BlockConsoleDaisyUnit(),
                TurnoutConsoleDaisyUnit(),
                TurnoutConsoleDaisyUnit(),
                BlockConsoleDaisyUnit(),
            ]
        )


def create_burleigh_county_block_cubes(maker=None):
    if maker is None:
        maker = BlockControlCube
    return [
    ]


def create_morton_county_block_cubes(maker=None):
    if maker is None:
        maker = BlockControlCube
    return [
    ]


def create_burleigh_county_turnout_cubes(left_maker=None, right_maker=None):
    if left_maker is None:
        left_maker = LeftTurnoutControlCube
    if right_maker is None:
        right_maker = RightTurnoutControlCube
    return [
    ]


MORTON_COUNTY_CONSOLE = [

]


def create_morton_county_turnout_cubes(left_maker=None, right_maker=None):
    if left_maker is None:
        left_maker = LeftTurnoutControlCube
    if right_maker is None:
        right_maker = RightTurnoutControlCube
    return [
    ]


class BurleighCountyMaster(DistrictMaster):
    def __init__(self, big_muddy):
        super().__init__(big_muddy, create_burleigh_console())


class MortonCountyMaster(DistrictMaster):
    def __init__(self, big_muddy):
        super().__init__(big_muddy, create_morton_console())

if __name__ == '__main__':
    print(MORTON_COUNTY_BLOCKS)