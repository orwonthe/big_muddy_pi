from daisy_socket import TurnoutConsoleDaisySocket, BlockConsoleDaisySocket


def generate_cubes_from_descriptions(district, descriptions):
    """ Generate cubes from descriptions matching requested district. """
    yield from generate_cubes(find_district_descriptions(district, descriptions))


def find_district_descriptions(district, descriptions):
    """ Generate the descriptions that match the district """
    for description in descriptions:
        if description["district"] == district:
            yield description


def generate_cubes(descriptions):
    """ Use descriptions to generate cubes"""
    for description in descriptions:
        yield create_cube_from_description(description)


def create_cube_from_description(description):
    """ Use description to create a matching cube """
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
        raise Exception("ERROR: Cannot understand cube from description")


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
