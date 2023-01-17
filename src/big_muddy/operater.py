# Copyright 2022 WillyMillsLLC
class Operator:
    def __init__(self):
        self.cubes = []
        self.servo_client = None

    def add_cube(self, cube_or_servo):
        if cube_or_servo.is_console:
            print(f'adding console cube {cube_or_servo.category}')
            self.cubes.append(cube_or_servo)
        elif self.servo_client is None:
            print(f'adding servo {cube_or_servo.category}')
            self.servo_client = cube_or_servo
        else:
            message = f'ERROR: Operator can only have one servo of category {cube_or_servo.category}.'
            raise Exception(message)

    @property
    def category(self):
        for cube in self.cubes:
            return cube.category
        if self.servo_client:
            return self.servo_client.category
        return None

    @property
    def status(self):
        suffix = 's' if self.servo_client else ''
        return f' {self.function} at {self.category}:{len(self.cubes)}{suffix}'
