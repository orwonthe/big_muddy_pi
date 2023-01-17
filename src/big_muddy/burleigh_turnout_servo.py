# Copyright 2022 WillyMillsLLC
from burleigh_turnout_servo_client_collection import BurleighTurnoutServoClientCollection
from burleigh_turnout_servo_daisy_module import BurleighTurnoutServoDaisyModule
from burleigh_turnout_servo_socket_collection import BurleighTurnoutServoSocketCollection
from servo import Servo


class BurleighTurnoutServo(Servo):
    def __init__(self):
        super().__init__(BurleighTurnoutServoDaisyModule(),
                         BurleighTurnoutServoSocketCollection(),
                         BurleighTurnoutServoClientCollection())
