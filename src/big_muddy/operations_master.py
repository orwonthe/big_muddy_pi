# Copyright 2022 WillyMillsLLC
from counties import BurleighDaisyModule, BurleighSocketCollection, MortonDaisyModule, MortonSocketCollection
from daisy_master import DaisyMaster

# Console recipe is the sequence of consoles in their order of appearance in the daisy chain.
# 'M' Means a Morton County Console.
# 'B' Means a Burleigh County Console.
DEFAULT_CONSOLE_RECIPE = "MBMBMB"


class Operator:
    def __init__(self):
        self.cubes = []

    def add_cube(self, cube):
        self.cubes.append(cube)

    @property
    def category(self):
        for cube in self.cubes:
            return cube.category
        return None

    @property
    def status(self):
        return f'{self.category}:{len(self.cubes)}'


class OperationsMaster(DaisyMaster):
    """ A DaisyMaster set up to operate the full railroad """

    def __init__(self, console_recipe=DEFAULT_CONSOLE_RECIPE):
        super().__init__()
        self.modules = []
        self.socket_collections = []
        self.consoles = []
        self.operator_list = []
        self.operator_dict = {}
        self.apply_console_recipe(console_recipe)
        self.set_for_action()
        self.add_sockets_to_consoles()
        self.add_operators()

    def apply_console_recipe(self, console_recipe):
        for letter in console_recipe:
            if letter == 'M':
                self.add_console(
                    BurleighDaisyModule(),
                    BurleighSocketCollection()
                )
            elif letter == 'B':
                self.add_console(
                    MortonDaisyModule(),
                    MortonSocketCollection()
                )

    def add_console(self, daisy_module, socket_collection):
        self.modules.append(daisy_module)
        self.socket_collections.append(socket_collection)
        self.consoles.append((daisy_module, socket_collection))

    def add_sockets_to_consoles(self):
        for module, sockets in self.consoles:
            module.add_sockets(sockets.cubes)

    def cycle(self):
        self.push_data()

    def print_status(self):
        print('Hello from Big Muddy RR. All aboard!')
        for operator in self.operator_list:
            print(operator.status)

    def add_operators(self):
        for socket_collection in self.socket_collections:
            for cube in socket_collection.cubes:
                operator = self.find_or_create_operator(cube)
                operator.add_cube(cube)

    def find_or_create_operator(self, cube):
        category = cube.category
        operator = self.operator_dict.get(category)
        if operator is None:
            operator = Operator()
            self.operator_dict[category] = operator
            self.operator_list.append(operator)
        return operator


if __name__ == '__main__':
    master = OperationsMaster()
    master.print_status()
