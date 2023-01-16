# Copyright 2022 WillyMillsLLC
from districts import find_district_descriptions
from turnout_servo_daisy_socket import TurnoutServoDaisySocket


def generate_servos_from_descriptions(district, descriptions):
    """ Generate servos from descriptions matching requested district. """
    yield from generate_servos(find_district_descriptions(district, descriptions))


def generate_servos(descriptions):
    """ Use descriptions to generate servos"""
    for description in descriptions:
        servo = create_servo_from_description(description)
        if servo:
            yield servo


def create_servo_from_description(description):
    """ Use description to create a matching cube """
    if description["purpose"] == "turnout" and description['servo_half'] == 0:
        return TurnoutServoDaisySocket(
            district=description["district"],
            socket_index=description["servo_socket"],
        )
    else:
        return None
