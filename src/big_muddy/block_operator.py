# Copyright 2022 WillyMillsLLC
from operater import Operator


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
