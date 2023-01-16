# Copyright 2022 WillyMillsLLC
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
