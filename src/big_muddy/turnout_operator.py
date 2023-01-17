# Copyright 2022 WillyMillsLLC
from operater import Operator


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
        if self.servo_client:
            self.direction = self.servo_client.direction
            if should_push_normal: # and self.direction:
                self.push_normal = True
            elif should_push_contrary: # and not self.direction:
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
        if self.servo_client:
            self.servo_client.set_push(self.push_normal, self.push_contrary)
