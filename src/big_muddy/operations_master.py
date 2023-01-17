# Copyright 2022 WillyMillsLLC
from block_operator import BlockOperator
from burleigh_console import BurleighConsole
from burleigh_turnout_servo import BurleighTurnoutServo
from daisy_master import DaisyMaster
from morton_console import MortonConsole
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
        self.servos_cubes = []
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
                self.add_console(BurleighConsole())
            elif letter == 'M':
                print("adding console M")
                self.add_console(MortonConsole())

    def apply_servo_recipe(self, servo_recipe):
        for letter in servo_recipe:
            if letter == 'b':
                print("adding servo b")
                self.add_servo(BurleighTurnoutServo())

    def add_console(self, console):
        self.modules.append(console.daisy_module)
        self.socket_collections.append(console.socket_collection)
        self.consoles.append(console)
        for daisy_unit in console.daisy_module.daisy_units:
            self.add_daisy_unit(daisy_unit)

    def add_servo(self, servo):
        self.modules.append(servo.daisy_module)
        self.socket_collections.append(servo.socket_collection)
        self.clients.append(servo.client_collection)
        self.servos.append(servo)
        for daisy_unit in servo.daisy_module.daisy_units:
            self.add_daisy_unit(daisy_unit)

    def add_sockets_to_consoles(self):
        for console in self.consoles:
            console.daisy_module.add_sockets(console.socket_collection.cubes)

    def add_sockets_to_servos(self):
        for servo in self.servos:
            servo.daisy_module.add_sockets(servo.socket_collection.cubes)
            for client in servo.client_collection.clients:
                client_socket = client.socket_index
                add_count = 0
                for socket in servo.socket_collection.cubes:
                    if socket.socket_index == client_socket:
                        socket.add_client(client)
                        add_count += 1
                    # else:
                    #     print(f'{client.name}: {socket.socket_index} != {client_socket}')
                if add_count == 0:
                    print(f'lost client {client.name}')
                elif add_count > 1:
                    print(f'duplicated client {client.name}')

    def add_operators(self):
        for socket_collection in self.socket_collections:
            for cube_or_servo in socket_collection.cubes:
                if cube_or_servo.is_console:
                    operator = self.find_or_create_operator(cube_or_servo)
                    operator.add_cube(cube_or_servo)
                else:
                    self.servos_cubes.append(cube_or_servo)
        for servo_cube in self.servos_cubes:
            lower_operator = self.operator_dict.get(servo_cube.lower_category)
            if lower_operator:
                lower_operator.servo_client = servo_cube.lower_turnout
            upper_operator = self.operator_dict.get(servo_cube.upper_category)
            if upper_operator:
                upper_operator.servo_client = servo_cube.upper_turnout

    def find_or_create_operator(self, cube):
        category = cube.category
        operator = self.operator_dict.get(category)
        if operator is None:
            if cube.first_term == "block":
                print(f' adding block operator for {category}')
                operator = BlockOperator()
            else:
                print(f' adding turnout operator for {category}')
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
