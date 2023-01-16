# Copyright 2022 WillyMillsLLC
import time

from signal_exception import SignalException
from signal_list import SignalList


class SerialDataSystem(SignalList):
    """
    Class for managing a serial data source
    """

    def __init__(self,
                 loading,
                 shifting,
                 data_signals=None,
                 max_test_duration=540,
                 ):
        """
        :param loading: ClockingPins for parallel load of data
        :param shifting: ClockingPins for data shifting
        :param data_signals: list of data signals driven by loading and shifting
        :param max_test_duration: maximum expected length of serial data
        """
        if data_signals is None:
            data_signals = []
        self.data_signals = data_signals
        self.loading = loading
        self.shifting = shifting
        self.max_test_duration = max_test_duration
        self.duration = None
        self._max_duration = None
        super().__init__(
            [self.loading, self.shifting] + data_signals
        )

    def shift(self, state_list):
        """
        Read current data, then push new data into the serial stream.

        Uses one clock cycle.
        :param state_list: List of signal values, one per data signal line
        :return: current data
        """
        result = self.read_data()
        self.write_data(state_list)
        self.shifting.pulse()
        return result

    def write_data(self, state_list):
        """
        Push data to the output pins of the data signals.

        No clock cycles.
        :param state_list: list of values for the data signals.
        """
        for data_signal, state in zip(self.data_signals, state_list):
            data_signal.write(state)

    def read_data(self):
        """
        Read the data from the data signal input pins, no clock cycle

        :return: list of values from the data signals.
        """
        return [data_signal.read() for data_signal in self.data_signals]

    def set_data_pins(self, value):
        """
        push the value to all the data signal input pins.
        No clock cycle.

        :param value:
        :return:
        """
        for data_signal in self.data_signals:
            data_signal.write(value)

    def start_duration_measurement(self):
        for data_signal in self.data_signals:
            data_signal.start_duration_measurement()

    def check_cleared(self):
        for data_signal in self.data_signals:
            if data_signal.check_cleared():
                print('Warning: ' + data_signal.signal_name + ' would not clear')

    def check_duration(self):
        for data_signal in self.data_signals:
            data_signal.check_duration()

    def ensure_duration_is_valid(self):
        for data_signal in self.data_signals:
            if data_signal.duration is None:
                self._max_duration = None
                data_signal.check_duration()

    @property
    def max_duration(self):
        self.ensure_duration_is_valid()
        if self._max_duration is None:
            duration = 0
            for data_signal in self.data_signals:
                signal_duration = data_signal.duration
                if signal_duration is not None and signal_duration > duration:
                    duration = signal_duration
            self._max_duration = duration
        return self._max_duration

    def determine_durations(self):
        """ Calculate and save duration as max of duration for any data signals. """
        self.set_data_pins(0)
        time.sleep(0.01)
        for _ in range(self.max_test_duration):
            self.shifting.pulse()
        self.check_cleared()
        self.set_data_pins(1)
        time.sleep(0.01)
        self.start_duration_measurement()
        for _ in range(self.max_test_duration):
            self.check_duration()
            self.shifting.pulse()
        duration = 0
        for data_signal in self.data_signals:
            data_duration = data_signal.duration
            if data_duration is None:
                raise SignalException("Error: Unable to determine duration for " + data_signal.signal_name)
            elif data_duration > duration:
                duration = data_duration
        self.duration = duration

    def set_all(self, value):
        """ Set all bits to the same value """
        self.set_data_pins(value)
        for _ in range(self.max_duration):
            self.shifting.pulse()
        self.loading.pulse()
