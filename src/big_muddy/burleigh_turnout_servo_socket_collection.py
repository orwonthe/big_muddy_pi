# Copyright 2022 WillyMillsLLC
from big_muddy_districts import BURLEIGH_COUNTY_TURNOUTS
from servos import generate_servos_from_descriptions
from daisy_socket import DaisySocketCollection


class BurleighTurnoutServoSocketCollection(DaisySocketCollection):
    """ Collection of servos for Burleigh County turnout servos"""

    def __init__(self):
        cubes = list(generate_servos_from_descriptions("Burleigh", BURLEIGH_COUNTY_TURNOUTS))
        super().__init__(cubes)
