# Copyright 2022 WillyMillsLLC
from big_muddy_districts import MORTON_COUNTY_CUBE_RECIPES
from cubes import generate_cubes_from_descriptions
from daisy_socket import DaisySocketCollection


class MortonConsoleSocketCollection(DaisySocketCollection):
    """ Collection of cubes for Morton County console """

    def __init__(self):
        cubes = list(generate_cubes_from_descriptions("Morton", MORTON_COUNTY_CUBE_RECIPES))
        super().__init__(cubes)
