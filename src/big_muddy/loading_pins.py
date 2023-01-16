# Copyright 2022 WillyMillsLLC
from gpio_linked_pins import ClockingPins


class LoadingPins(ClockingPins):
    """
    Clock pins used for parallel load signal
    """

    def __init__(self,
                 in_pin_number,
                 out_pin_number,
                 signal_prefix="load",
                 gpio=None):
        super().__init__(
            signal_prefix=signal_prefix,
            in_pin_number=in_pin_number,
            out_pin_number=out_pin_number,
            gpio=gpio,
        )
