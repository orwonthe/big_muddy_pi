# Copyright 2022 WillyMillsLLC
from burleigh_console_daisy_module import BurleighConsoleDaisyModule
from burleigh_console_socket_collection import BurleighConsoleSocketCollection
from district_console_master import DistrictConsoleMaster


class BurleighCountyMaster(DistrictConsoleMaster):
    """ DaisyMaster for Burleigh County """

    def __init__(self):
        district_console = BurleighConsoleDaisyModule()
        daisy_socket_collection = BurleighConsoleSocketCollection()
        super().__init__(district_console, daisy_socket_collection)
