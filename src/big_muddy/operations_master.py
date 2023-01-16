# Copyright 2022 WillyMillsLLC
from counties import BurleighConsoleDaisyModule, MortonConsoleDaisyModule, \
    MortonConsoleSocketCollection, BurleighTurnoutServoDaisyModule
from burleigh_console_socket_collection import BurleighConsoleSocketCollection
from burleigh_turnout_servo_client_collection import BurleighTurnoutServoClientCollection
from burleigh_turnout_servo_socket_collection import BurleighTurnoutServoSocketCollection
from daisy_master import DaisyMaster

# Console recipe is the sequence of consoles in their order of appearance in the daisy chain.
# 'M' Means a Morton County Console.
# 'B' Means a Burleigh County Console.
DEFAULT_CONSOLE_RECIPE = "MBMBMB"

# Servo recipe is the sequence of servos in their order of appearance in the daisy chain.
# 'b' is Burleigh turnout servo.
DEFAULT_SERVO_RECIPE = "b"


class Operator:
    def __init__(self):
        self.cubes = []
        self.servo = None

    def add_cube(self, cube_or_servo):
        if cube_or_servo.is_console:
            print(f'adding console cube {cube_or_servo.name}')
            self.cubes.append(cube_or_servo)
        elif self.servo is None:
            print(f'adding servo {cube_or_servo.name}')
            self.servo = cube_or_servo
        else:
            raise Exception("ERROR: Operator can only have one servo. ")

    @property
    def category(self):
        for cube in self.cubes:
            return cube.category
        for servo in self.servos:
            return servo.category
        return None

    @property
    def status(self):
        suffix = 's' if self.servo else ''
        return f' {self.function} at {self.category}:{len(self.cubes)}{suffix}'


class BlockOperator(Operator):
    def __init__(self):
        super(BlockOperator, self).__init__()
        self.state = 0
        self.conflicted = False

    @property
    def function(self):
        return "Block Control"

    def clear(self):
        for cube in self.cubes:
            cube.set_normal_red()
            cube.set_contrary_red()

    def cycle(self):
        self.determine_next_state()
        self.invoke_next_state()

    def determine_next_state(self):
        next_state = 0
        requests_made = 0
        for index, cube in enumerate(self.cubes):
            contrary, normal = cube.toggle_state
            if contrary:
                next_state = -index - 1
                requests_made += 1
            if normal:
                next_state = index + 1
                requests_made += 1
        if requests_made < 2:
            self.state = next_state
            self.conflicted = False
        else:
            self.state = -1
            self.conflicted = True

    def invoke_next_state(self):
        for index, cube in enumerate(self.cubes):
            if self.conflicted:
                contrary, normal = cube.toggle_state
                if contrary:
                    cube.set_normal_yellow()
                    cube.set_contrary_red()
                elif normal:
                    cube.set_normal_red()
                    cube.set_contrary_yellow()
                else:
                    cube.set_normal_yellow()
                    cube.set_contrary_yellow()
            elif self.state == 1 + index:
                cube.set_normal_green()
                cube.set_contrary_off()
            elif self.state == -1 - index:
                cube.set_normal_off()
                cube.set_contrary_green()
            elif self.state < 0:
                cube.set_normal_off()
                cube.set_contrary_red()
            elif self.state > 0:
                cube.set_normal_red()
                cube.set_contrary_off()
            else:
                cube.set_normal_off()
                cube.set_contrary_off()


class TurnoutOperator(Operator):
    def __init__(self):
        super(TurnoutOperator, self).__init__()
        self.direction = None
        self.push_contrary = False
        self.push_normal = False

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
        should_push_normal = False
        should_push_contrary = False
        bit_weight = 1
        for cube in self.cubes:
            contrary, normal = cube.push_button_state
            contrary_requested += bit_weight * contrary
            normal_requested += bit_weight * normal
            bit_weight *= 2
        if contrary_requested and not normal_requested:
            print(f'{self.status} siding {contrary_requested}')
            should_push_contrary = True
        elif normal_requested and not contrary_requested:
            print(f'{self.status} main {normal_requested}')
            should_push_normal = True
        if self.servo:
            self.direction = self.servo.direction
            if should_push_normal and self.direction:
                self.push_normal = True
            elif should_push_contrary and not self.direction:
                self.push_contrary = True
        else:
            # If there is no servo yet, pretend wishes can come true.
            if should_push_normal:
                self.direction = 0
            elif should_push_contrary:
                self.direction = 1

    def invoke_next_state(self):
        if self.direction:
            for cube in self.cubes:
                cube.set_at_siding()
        else:
            for cube in self.cubes:
                cube.set_at_main()
        if self.servo:
            self.servo.set_push(self.push_normal, self.push_contrary)


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
