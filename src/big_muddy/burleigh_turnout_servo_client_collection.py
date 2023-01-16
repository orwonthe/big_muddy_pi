# Copyright 2022 WillyMillsLLC
from big_muddy_districts import BURLEIGH_COUNTY_TURNOUTS
from servo_turnout_client import create_servo_turnout_client


class BurleighTurnoutServoClientCollection:
    """ Collection of Servo Clients for Burleigh County """

    def __init__(self):
        self.clients = [create_servo_turnout_client(description) for description in BURLEIGH_COUNTY_TURNOUTS]
