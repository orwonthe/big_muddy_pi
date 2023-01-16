def find_district_descriptions(district, descriptions):
    """ Generate the descriptions that match the district """
    for description in descriptions:
        if description["district"] == district:
            yield description


def normalize_cube_dictionary_list(district, purpose, cube_dictionary_list):
    """ Add various entries to a cube dictionary and sort by socket index """
    for gui_index, cube_dictionary in enumerate(cube_dictionary_list):
        cube_dictionary["district"] = district
        cube_dictionary["purpose"] = purpose
        cube_dictionary["gui_index"] = gui_index  # Dictionary is given in a natural gui display order. Remember it.
    return sorted(cube_dictionary_list, key=lambda item: item["console_socket"])
