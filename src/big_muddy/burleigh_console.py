# Copyright 2022 WillyMillsLLC
from burleigh_console_daisy_module import BurleighConsoleDaisyModule
from burleigh_console_socket_collection import BurleighConsoleSocketCollection
from console import Console


class BurleighConsole(Console):
    def __init__(self):
        super().__init__(BurleighConsoleDaisyModule(), BurleighConsoleSocketCollection())
