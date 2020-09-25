from big_muddy.cubes import BlockControlCube, RightTurnoutControlCube, LeftTurnoutControlCube
from big_muddy.daisy_unit import BlockConsoleDaisyUnit, TurnoutConsoleDaisyUnit


class CountyConsole:
    """
    County console is dedicated to one half of the railroad.

    The console consists of a 6 row and 9 column panel of cubes.

    """
    def __init__(self, name, block_cubes, turnout_cubes, daisy_units):
        """

        :param name: county name
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
            cube.county = self
            cube.index = index
            cube.find_daisy_unit(daisy_units)

    @property
    def cubes(self):
        return self.block_cubes + self.turnout_cubes

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


def create_burleigh_county_block_cubes():
    return [
        BlockControlCube(
            name="bridge",
            color="brown",
            row=4,
            column=0,
            socket_index=4
        ),
        BlockControlCube(
            name="rejoin",
            color="purple",
            row=0,
            column=1,
            socket_index=7
        ),
        BlockControlCube(
            name="main",
            color="green",
            row=0,
            column=7,
            socket_index=6
        ),
        BlockControlCube(
            name="loop",
            color="black",
            row=3,
            column=8,
            socket_index=1
        ),
        BlockControlCube(
            name="flats",
            color="blue",
            row=5,
            column=4,
            socket_index=0
        ),
        BlockControlCube(
            name="crossing",
            color="gray",
            row=4,
            column=5,
            socket_index=3
        ),
        BlockControlCube(
            name="depot",
            color="orange",
            row=1,
            column=5,
            socket_index=5
        ),
        BlockControlCube(
            name="commerce",
            color="yellow",
            row=1,
            column=5,
            socket_index=2
        ),
    ]


def create_burleigh_county_turnout_cubes():
    return [
        RightTurnoutControlCube(
            name="rejoin main",
            color="purple",
            row=0,
            column=2,
            socket_index=0
        ),
        RightTurnoutControlCube(
            name="depot west",
            color="green+orange",
            row=0,
            column=3,
            socket_index=1
        ),
        LeftTurnoutControlCube(
            name="depot east",
            color="green+orange",
            row=0,
            column=6,
            socket_index=2
        ),
        RightTurnoutControlCube(
            name="depot to yard",
            color="orange",
            row=1,
            column=4,
            socket_index=3
        ),
        RightTurnoutControlCube(
            name="yard to commerce",
            color="orange+yellow",
            row=2,
            column=5,
            socket_index=4
        ),
        RightTurnoutControlCube(
            name="yard to siding",
            color="orange",
            row=2,
            column=6,
            socket_index=5
        ),
        RightTurnoutControlCube(
            name="back yard",
            color="yellow",
            row=4,
            column=6,
            socket_index=6
        ),
        RightTurnoutControlCube(
            name="main to flat",
            color="blue+gray",
            row=5,
            column=5,
            socket_index=7
        ),
    ]

def create_burleigh_console():
    return BurleighCountyConsole()

