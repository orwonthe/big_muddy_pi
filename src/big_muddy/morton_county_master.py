from district_console_master import DistrictConsoleMaster
from morton_console_daisy_module import MortonConsoleDaisyModule
from morton_console_socket_collection import MortonConsoleSocketCollection


class MortonCountyMaster(DistrictConsoleMaster):
    """ DaisyMaster for Morton County """

    def __init__(self):
        district_console = MortonConsoleDaisyModule()
        daisy_socket_collection = MortonConsoleSocketCollection()
        super().__init__(district_console, daisy_socket_collection)
