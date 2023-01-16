# Copyright 2022 WillyMillsLLC
from block_operator import BlockOperator
from morton_console_daisy_module import MortonConsoleDaisyModule
from burleigh_console_daisy_module import BurleighConsoleDaisyModule
from burleigh_turnout_servo_daisy_module import BurleighTurnoutServoDaisyModule
from morton_console_socket_collection import MortonConsoleSocketCollection
from burleigh_console_socket_collection import BurleighConsoleSocketCollection
from burleigh_turnout_servo_client_collection import BurleighTurnoutServoClientCollection
from burleigh_turnout_servo_socket_collection import BurleighTurnoutServoSocketCollection
from daisy_master import DaisyMaster
from turnout_operator import TurnoutOperator

# Console recipe is the sequence of consoles in their order of appearance in the daisy chain.
# 'M' Means a Morton County Console.
# 'B' Means a Burleigh County Console.
DEFAULT_CONSOLE_RECIPE = "MBMBMB"

# Servo recipe is the sequence of servos in their order of appearance in the daisy chain.
# 'b' is Burleigh turnout servo.
DEFAULT_SERVO_RECIPE = "b"


class OperationsMaster(DaisyMaster):
    """ A DaisyMaster set up to operate the full railroad """

    def __init__(self, console_recipe=DEFAULT_CONSOLE_RECIPE, servo_recipe=DEFAULT_SERVO_RECIPE):
        super().__init__()
        self.modules = []
        self.socket_collections = []
        self.consoles = []
        self.servos = []
        self.clients = []
        self.operator_list = []
        self.operator_dict = {}
        self.apply_console_recipe(console_recipe)
        self.apply_servo_recipe(servo_recipe)
        self.set_for_action()
        self.add_sockets_to_consoles()
        self.add_sockets_to_servos()
        self.add_operators()

    def apply_console_recipe(self, console_recipe):
        for letter in console_recipe:
            if letter == 'B':
                print("adding console B")
                self.add_console(
                    BurleighConsoleDaisyModule(),
                    BurleighConsoleSocketCollection()
                )
            elif letter == 'M':
                print("adding console M")
                self.add_console(
                    MortonConsoleDaisyModule(),
                    MortonConsoleSocketCollection()
                )

    def apply_servo_recipe(self, servo_recipe):
        for letter in servo_recipe:
            if letter == 'b':
                print("adding servo b")
                self.add_servo(
                    BurleighTurnoutServoDaisyModule(),
                    BurleighTurnoutServoSocketCollection(),
                    BurleighTurnoutServoClientCollection()
                )

    def add_console(self, daisy_module, socket_collection):
        self.modules.append(daisy_module)
        self.socket_collections.append(socket_collection)
        self.consoles.append((daisy_module, socket_collection))
        for daisy_unit in daisy_module.daisy_units:
            self.add_daisy_unit(daisy_unit)

    def add_servo(self, daisy_module, socket_collection, client_collection):
        self.modules.append(daisy_module)
        self.socket_collections.append(socket_collection)
        self.clients.append(client_collection)
        self.servos.append((daisy_module, socket_collection, client_collection))
        for daisy_unit in daisy_module.daisy_units:
            self.add_daisy_unit(daisy_unit)

    def add_sockets_to_consoles(self):
        for module, sockets in self.consoles:
            module.add_sockets(sockets.cubes)

    def add_sockets_to_servos(self):
        for module, socket_collection, client_collection in self.servos:
            module.add_sockets(socket_collection.cubes)
            for client in client_collection:
                client_socket = client.servo_socket
                for socket in socket_collection.cubes:
                    if socket.socket_index == client_socket:
                        socket.add_client(client)


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
        # print('O')
        for operator in self.operator_list:
            operator.cycle()
        # print('p')
        self.push_data()


if __name__ == '__main__':
    master = OperationsMaster()
    master.print_status()
    master.clear()
    while True:
        master.cycle()
