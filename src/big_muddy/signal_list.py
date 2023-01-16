# Copyright 2022 WillyMillsLLC
class SignalList:
    """ Base class implements setup method for signal list """

    def __init__(self, signals):
        self.signals = signals

    def setup(self):
        for signal in self.signals:
            signal.setup()
