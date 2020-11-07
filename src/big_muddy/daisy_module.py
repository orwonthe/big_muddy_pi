class DaisyModule:
    """
    Daisy module is a collection of daisy units.
    """
    def __init__(self, name, daisy_units):
        self.name = name
        self.daisy_units = daisy_units
        self.console_block_daisy_units = []
        self.console_turnout_daisy_units = []
        self.servo_block_daisy_units = []
        self.servo_turnout_daisy_units = []
        self.sockets = []

    def add_daisy_units(self, daisy_units):
        for daisy_unit in daisy_units:
            self.add_daisy_unit(daisy_unit)

    def add_daisy_unit(self, daisy_unit):
        self.find_daisy_unit_list(daisy_unit).append(daisy_unit)

    def find_daisy_unit_list(self, key):
        if key.is_console:
            return self.console_block_daisy_units if key.is_block else self.console_turnout_daisy_units
        else:
            return self.servo_block_daisy_units if key.is_block else self.servo_turnout_daisy_units

    def current_daisy_unit(self, socket):
        daisy_units = self.find_daisy_unit_list(socket)
        for daisy_unit in daisy_units:
            if not daisy_unit.is_complete:
                return daisy_unit
        return None

    def add_socket(self, socket):
        daisy_unit = self.current_daisy_unit(socket)
        if daisy_unit:
            socket.add_to_daisy_unit(daisy_unit)
            self.sockets.append(socket)
        return daisy_unit
