from big_muddy_districts import BURLEIGH_COUNTY_CUBE_RECIPES, MORTON_COUNTY_CUBE_RECIPES, BURLEIGH_COUNTY_TURNOUTS
from cubes import generate_cubes_from_descriptions, generate_servos_from_descriptions
from daisy_module import DaisyModule
from daisy_socket import DaisySocketCollection
from daisy_unit import BlockConsoleDaisyUnit, TurnoutConsoleDaisyUnit, TurnoutServoDaisyUnit
from districts import DistrictConsoleMaster


class BurleighTurnoutServoSocketCollection(DaisySocketCollection):
    """ Collection of servos for Burleigh County turnout servos"""

    def __init__(self):
        cubes = list(generate_servos_from_descriptions("Burleigh", BURLEIGH_COUNTY_TURNOUTS))
        super().__init__(cubes)


class BurleighTurnoutServoClientCollection:
    """ Collection of Servo Clients for Burleigh County """

    def __init__(self):
        self.clients = [create_servo_turnout_client(description) for description in BURLEIGH_COUNTY_TURNOUTS]


class ServoTurnoutClient:
    def __init__(self, description):
        self.description = description
        self.servo_socket = None
        self.socket_index = description['servo_socket']


def create_servo_turnout_client(description):
    if description['servo_half']:
        return UpperServoTurnoutClient(description)
    else:
        return LowerServoTurnoutClient(description)


class LowerServoTurnoutClient(ServoTurnoutClient):
    pass


class UpperServoTurnoutClient(ServoTurnoutClient):
    pass


class BurleighConsoleSocketCollection(DaisySocketCollection):
    """ Collection of cubes for Burleigh County console """

    def __init__(self):
        cubes = list(generate_cubes_from_descriptions("Burleigh", BURLEIGH_COUNTY_CUBE_RECIPES))
        super().__init__(cubes)


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
