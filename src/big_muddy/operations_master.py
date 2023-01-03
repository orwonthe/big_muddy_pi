# Copyright 2022 WillyMillsLLC
from counties import BurleighDaisyModule, BurleighSocketCollection, MortonDaisyModule, MortonSocketCollection
from daisy_master import DaisyMaster

# Console recipe is the sequence of consoles in their order of appearance in the daisy chain.
# 'M' Means a Morton County Console.
# 'B' Means a Burleigh County Console.
DEFAULT_CONSOLE_RECIPE = "BMBMBM"


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
        return f' {self.function} at {self.category}:{len(self.cubes)}'


class BlockOperator(Operator):
    @property
    def function(self):
        return "Block Control"

    def clear(self):
        for cube in self.cubes:
            cube.set_normal_off()

    def cycle(self):
        self.clear()


class TurnoutOperator(Operator):
    def __init__(self):
        super(TurnoutOperator, self).__init__()
        self.contrary = False

    @property
    def function(self):
        return "Turnout Control"

    def clear(self):
        for cube in self.cubes:
            cube.set_at_main()

    def cycle(self):
        self.determine_next_state()
        self.invoke_next_state()

    def determine_next_state(self):
        contrary_requested = 0
        normal_requested = 0
        bit_weight = 1
        for cube in self.cubes:
            contrary, normal = cube.push_button_state
            contrary_requested += bit_weight * contrary
            normal_requested += bit_weight * normal
            bit_weight *= 2
        if contrary_requested and not normal_requested:
            print(f'{self.status} siding {contrary_requested}')
            self.contrary = True
        elif normal_requested and not contrary_requested:
            print(f'{self.status} main {normal_requested}')
            self.contrary = False

    def invoke_next_state(self):
        if self.contrary:
            for cube in self.cubes:
                cube.set_at_siding()
        else:
            for cube in self.cubes:
                cube.set_at_main()


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
        for daisy_unit in daisy_module.daisy_units:
            self.add_daisy_unit(daisy_unit)

    def add_sockets_to_consoles(self):
        for module, sockets in self.consoles:
            module.add_sockets(sockets.cubes)

    def add_operators(self):
        for socket_collection in self.socket_collections:
            for cube in socket_collection.cubes:
                operator = self.find_or_create_operator(cube)
                operator.add_cube(cube)

    def find_or_create_operator(self, cube):
        category = cube.category
        operator = self.operator_dict.get(category)
        if operator is None:
            if cube.first_term == "block":
                operator = BlockOperator()
            else:
                operator = TurnoutOperator()
            self.operator_dict[category] = operator
            self.operator_list.append(operator)
        return operator

    def print_status(self):
        print('Hello from Big Muddy RR. All aboard!')
        for operator in self.operator_list:
            print(operator.status)

    def clear(self):
        for operator in self.operator_list:
            operator.clear()
        print('Cleared.')

    def cycle(self):
        for operator in self.operator_list:
            operator.cycle()
        self.push_data()


if __name__ == '__main__':
    master = OperationsMaster()
    master.print_status()
    master.clear()
    while True:
        master.cycle()
