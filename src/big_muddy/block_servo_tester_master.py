# Copyright 2022 WillyMillsLLC
from daisy_master import DaisyMaster


class BlockServoTesterMaster(DaisyMaster):
    """ Defines setup for testing block servo controller board """

    def __init__(self, daisy_units):
        super().__init__(daisy_units)
