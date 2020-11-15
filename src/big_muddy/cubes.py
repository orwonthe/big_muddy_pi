from daisy_socket import TurnoutConsoleDaisySocket, BlockConsoleDaisySocket


def find_descriptions_and_create_cubes(district, descriptions):
    yield from create_cubes(find_district_descriptions(district, descriptions))


def find_district_descriptions(district, descriptions):
    for description in descriptions:
        if description["district"] == district:
            yield description


def create_cubes(descriptions):
    for description in descriptions:
        yield create_cube_from_description(description)


def create_cube_from_description(description):
    if description["purpose"] == "block":
        return BlockConsoleDaisySocket(
            district=description["district"],
            name=description["name"],
            color=description["color"],
            row=description["row"],
            column=description["column"],
            socket_index=description["socket"],
            gui_index=description["gui_index"]
        )
    elif description["direction"] == "left":
        return LeftTurnoutControlCube(
            district=description["district"],
            name=description["name"],
            color=description["color"],
            row=description["row"],
            column=description["column"],
            socket_index=description["socket"],
            gui_index=description["gui_index"]
        )
    elif description["direction"] == "right":
        return RightTurnoutControlCube(
            district=description["district"],
            name=description["name"],
            color=description["color"],
            row=description["row"],
            column=description["column"],
            socket_index=description["socket"],
            gui_index=description["gui_index"]
        )
    else:
        raise Exception("Cannot understand cube from description")


class LeftTurnoutControlCube(TurnoutConsoleDaisySocket):
    """ A turnout control cube for turnouts with the divergence to the left """

    @property
    def direction(self):
        return "left"


class RightTurnoutControlCube(TurnoutConsoleDaisySocket):
    """ A turnout control cube for turnouts with the divergence to the right """

    @property
    def direction(self):
        return "right"
