from big_muddy.console import ConsoleCube
from big_muddy.daisy_domain import BlockMixin, TurnoutMixin


def find_description_and_create_cube(district, descriptions):
    yield from create_cubes(find_district_descriptions(district, descriptions))


def find_district_descriptions(district, descriptions):
    for description in descriptions:
        if description["district"] == district:
            yield description


def create_cubes(descriptions):
    for description in descriptions:
        if description["purpose"] == "block":
            yield BlockControlCube(
                district=description["district"],
                name=description["name"],
                color=description["color"],
                row=description["row"],
                column=description["column"],
                socket_index=description["socket"],
                gui_index=description["gui_index"]
            )
        elif description["direction"] == "left":
            yield LeftTurnoutControlCube(
                district=description["district"],
                name=description["name"],
                color=description["color"],
                row=description["row"],
                column=description["column"],
                socket_index=description["socket"],
                gui_index=description["gui_index"]
            )
        else:
            yield RightTurnoutControlCube(
                district=description["district"],
                name=description["name"],
                color=description["color"],
                row=description["row"],
                column=description["column"],
                socket_index=description["socket"],
                gui_index=description["gui_index"]
            )


class BlockControlCube(ConsoleCube, BlockMixin):
    """
    A block control cube controls an electrically isolated set of tracks.

    Each block has, in a somewhat arbitrary manner, been designated with a natural
    or contrary direction. On the actual railroad this would correspond to east or west bound etc.

    It has a 3 position toggle switch for natural, none, and contrary.
    When the user is requesting a block, the user requests the block
    to match the direction the locomotive is facing.

    In the center (none) position the block is not requested.

    In the natural position, the block is requested with positive power moving
    a locomotive forward in the direction designated as natural.
    Reversing power will move the locomotive in the contrary direction.

    In the contrary position, the block is requested with positive power moving
    the locomotive in the contrary position and negative power moving in the natural direction.

    There are two leds, one on each side of the toggle switch.
    Each led can be off, red, green, or yellow.

    """

    def __init__(self, district=None, name=None, color=None, row=None, column=None, socket_index=None, gui_index=None):
        super().__init__(district=district, name=name, color=color, row=row, column=column, socket_index=socket_index,
                         gui_index=gui_index)

    def set_normal_off(self):
        self.daisy_unit.set_to_send(self.output_bit_index, 0)
        self.daisy_unit.set_to_send(self.output_bit_index + 1, 0)

    def set_normal_green(self):
        self.daisy_unit.set_to_send(self.output_bit_index, 0)
        self.daisy_unit.set_to_send(self.output_bit_index + 1, 1)

    def set_normal_red(self):
        self.daisy_unit.set_to_send(self.output_bit_index, 1)
        self.daisy_unit.set_to_send(self.output_bit_index + 1, 0)

    def set_normal_yellow(self):
        self.daisy_unit.set_to_send(self.output_bit_index, 1)
        self.daisy_unit.set_to_send(self.output_bit_index + 1, 1)

    def set_contrary_off(self):
        self.daisy_unit.set_to_send(self.output_bit_index + 2, 0)
        self.daisy_unit.set_to_send(self.output_bit_index + 3, 0)

    def set_contrary_green(self):
        self.daisy_unit.set_to_send(self.output_bit_index + 2, 0)
        self.daisy_unit.set_to_send(self.output_bit_index + 3, 1)

    def set_contrary_red(self):
        self.daisy_unit.set_to_send(self.output_bit_index + 2, 1)
        self.daisy_unit.set_to_send(self.output_bit_index + 3, 0)

    def set_contrary_yellow(self):
        self.daisy_unit.set_to_send(self.output_bit_index + 2, 1)
        self.daisy_unit.set_to_send(self.output_bit_index + 3, 1)

    def get_toggle_state(self):
        return 1 - self.daisy_unit.get_received(self.input_bit_index + 1), 1 - self.daisy_unit.get_received(
            self.input_bit_index)

    def reflect(self):
        contrary, normal = self.get_toggle_state()
        if normal:
            self.set_normal_green()
        else:
            self.set_normal_off()
        if contrary:
            self.set_contrary_green()
        else:
            self.set_contrary_off()


class TurnoutControlCube(ConsoleCube, TurnoutMixin):
    """
    A turnout control cube controls a railroad turnout.

    It has two momentary push buttons each with an led next to it.
    The two leds are driven by the same signal so if one is on, the other is off.
    The purpose of the leds are to indicate the actual position of the turnout.
    The purpose of the push buttons is to indicate a desired position of the turnout.

    The operation of a model railroad differs from that of a prototype.
    On the model railroad an operator may have a reasonable need to control a turnout
    that is within a block controlled by another operator.
    An example would be when the first operator is backing a long train into a siding.
    The first operator needs to adjust the turnout for the siding but the
    locomotive is on a different electrical block.
    Meanwhile a second operator is using the electrical block containing
    the siding for some unrelated purpose.

    """

    def __init__(self, district=None, name=None, color=None, row=None, column=None, socket_index=None, gui_index=None):
        super().__init__(district=district, name=name, color=color, row=row, column=column, socket_index=socket_index,
                         gui_index=gui_index)

    @property
    def action(self):
        return f'{self.direction} {self.purpose}'

    def set_at_main(self):
        """ Indicate turnout is set for main (straight) """
        self.daisy_unit.set_to_send(self.output_bit_index, 0)

    def set_at_siding(self):
        """ Indicate turnout is set for siding (curve) """
        self.daisy_unit.set_to_send(self.output_bit_index, 1)

    def get_push_button_state(self):
        return 1 - self.daisy_unit.get_received(self.input_bit_index + 1), 1 - self.daisy_unit.get_received(
            self.input_bit_index)

    def reflect(self):
        contrary, normal = self.get_push_button_state()
        if normal:
            self.set_at_main()
        elif contrary:
            self.set_at_siding()


class LeftTurnoutControlCube(TurnoutControlCube):
    @property
    def direction(self):
        return "left"


class RightTurnoutControlCube(TurnoutControlCube):
    @property
    def direction(self):
        return "right"
