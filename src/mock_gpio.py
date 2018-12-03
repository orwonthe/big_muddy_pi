class DummyGPIO:
    def setmode(self, mode):
        pass

    def setwarnings(self, value):
        pass

    def input(self, pin_number):
        pass

    def output(self, pin_number, state):
        pass


class MockGPIO:
    def __init__(self, emulator=None):
        if emulator is None:
            emulator = DummyGPIO()

        self.emulator = emulator

    def setmode(self, mode):
        self.emulator.setmode(mode)

    def setwarnings(self, value):
        self.emulator.setwarnings(value)

    def input(self, pin_number):
        return self.emulator.input(pin_number)

    def output(self, pin_number, state):
        self.emulator.output(pin_number, state)


MOCK_GPIO = MockGPIO()
