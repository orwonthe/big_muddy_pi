class ConsoleCube:
    """
    A software console cube here is intended as a one to one match for a physical cube in a console.

    The input/output sense of the console cube is opposite of the matching physical cube.
    An led on the physical cube is an input of the physical cube but an output of the software cube.
    An electrical switch on the physical cube is an output of the physical cube but an input of the software cube.

    """

    def __init__(self, county=None, name=None, color=None, row=None, column=None, socket_index=None, index=None):
        """

        :param county: a CountyConsole object represents a physical division of the railroad
        :param name: the name of the cube for user display
        :param color: the color key(s) for the map of the railroad. Turnouts sometimes have two.
        :param row: The row of the console containing this cube.
        :param column: The column of the console containing this cube.
        :param socket_index: The index specifying which available socket is used to connect this cube.
        :param index: The index of the cube in the console's master list.
        """
        self.county = county
        self.name = name
        self.color = color
        self.row = row
        self.column = column
        self.socket_index = socket_index
        self.index = index
        # TODO: consider using lambda functions for read/write access
        self.daisy_unit = None  # Will get set to point to the daisy unit containing this cube.
        self.input_bit_index = None  # Will get set to the index of the first input bit within the daisy unit.
        self.output_bit_index = None  # Will get set to the index of the first output bit within the daisy unit.

    @property
    def full_name(self):
        """ User friendly full name of the cube """
        return f'{self.county.name} {self.short_name}'

    @property
    def short_name(self):
        """ User friendly name (sans county) of the cube """
        return f'{self.name} {self.color}'

    @property
    def action(self):
        """ User friendly description of what the cube does """
        return self.purpose

    @property
    def is_block(self):
        """ Whether the cube is used to control blocks of track """
        return self.purpose == "block"

    @property
    def is_turnout(self):
        """ Whether the cube is used to control a turnout """
        return self.purpose == "turnout"

    def is_my_kind_of_daisy_unit(self, daisy_unit):
        """ Different kinds of cubes connect to different types of daisy units """
        return daisy_unit.is_console and (
            (daisy_unit.is_block and self.is_block) or (daisy_unit.is_turnout and self.is_turnout)
        )

    def find_daisy_unit(self, daisy_units):
        """ In the list of daisy units, find the right one and set up read/write access to it """
        remaining_socket_index = self.socket_index
        for daisy_unit in daisy_units:
            if self.is_my_kind_of_daisy_unit(daisy_unit):
                if remaining_socket_index < daisy_unit.socket_count:
                    self.daisy_unit = daisy_unit
                    self.input_bit_index = remaining_socket_index * daisy_unit.input_bits_per_socket
                    self.output_bit_index = remaining_socket_index * daisy_unit.output_bits_per_socket
                    break
                else:
                    remaining_socket_index -= daisy_unit.socket_count


class BlockControlCube(ConsoleCube):
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

    def __init__(self, county=None, name=None, color=None, row=None, column=None, socket_index=None, index=None):
        super().__init__(county=county, name=name, color=color, row=row, column=column, socket_index=socket_index,
                         index=index)
        self.state = [0, 0, 0, 0]

    @property
    def purpose(self):
        """ Indicate that this cube is for block control """
        return "block"

    # TODO: consider using lambda functions for read/write access

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


class TurnoutControlCube(ConsoleCube):
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

    def __init__(self, county=None, name=None, color=None, row=None, column=None, socket_index=None, index=None):
        super().__init__(county=county, name=name, color=color, row=row, column=column, socket_index=socket_index,
                         index=index)
        self.state = [0, 0, 0, 0]

    @property
    def purpose(self):
        """ Indicate that this cube is for block control """
        return "turnout"

    @property
    def action(self):
        return f'{self.direction} {self.purpose}'

    # TODO: consider using lambda functions for read/write access

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
