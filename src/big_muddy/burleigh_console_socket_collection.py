# Copyright 2022 WillyMillsLLC
from big_muddy_districts import BURLEIGH_COUNTY_CUBE_RECIPES
from cubes import generate_cubes_from_descriptions
from daisy_socket import DaisySocketCollection


class BurleighConsoleSocketCollection(DaisySocketCollection):
    """ Collection of cubes for Burleigh County console """

    def __init__(self):
        cubes = list(generate_cubes_from_descriptions("Burleigh", BURLEIGH_COUNTY_CUBE_RECIPES))
        super().__init__(cubes)
