# Copyright 2022 WillyMillsLLC
from console import Console
from morton_console_daisy_module import MortonConsoleDaisyModule
from morton_console_socket_collection import MortonConsoleSocketCollection


class MortonConsole(Console):
    def __init__(self):
        super().__init__(MortonConsoleDaisyModule(), MortonConsoleSocketCollection())