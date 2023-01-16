# Copyright 2022 WillyMillsLLC
from gpio_linked_pins import GpioLinkedPins
from signal_exception import SignalException


class DataPins(GpioLinkedPins):
    """ Pair of gpio pins used for serialized data """

    def __init__(self,
                 in_pin_number,
                 out_pin_number,
                 signal_prefix,
                 gpio=None):
        self.duration = None
        self._duration = 0
        super().__init__(
            signal_prefix=signal_prefix,
            in_pin_number=in_pin_number,
            out_pin_number=out_pin_number,
            gpio=gpio
        )

    def check_cleared(self):
        """ Used as part of daisy chain length self measurement """
        return self.read()

    def start_duration_measurement(self):
        """ Called at start of duration measurement """
        self.duration = None
        self._duration = 0

    def check_duration(self):
        """ Called at each cycle of duration measurement """
        if self.duration is None:
            if self.read():
                self.duration = self._duration
            else:
                self._duration += 1
        elif not self.read():
            raise SignalException("ERROR: broken data chain at " + self.signal_name)
