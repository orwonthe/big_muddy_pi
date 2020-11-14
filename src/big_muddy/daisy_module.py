from daisy_domain import DomainLists


class DaisyModule(DomainLists):
    """
    Daisy module is a collection of daisy units.
    """
    def __init__(self, name, daisy_units=None):
        super().__init__()
        self.name = name
        self.daisy_units = []  # Ordered according to hardware daisy sequence
        self.sockets = []
        if daisy_units:
            self.add_daisy_units(daisy_units)

    def add_to_master(self, daisy_master):
        daisy_master.add_daisy_units(self.daisy_units)

    def add_daisy_units(self, daisy_units):
        for daisy_unit in daisy_units:
            self.add_daisy_unit(daisy_unit)

    def add_daisy_unit(self, daisy_unit):
        self.append(daisy_unit)
        self.daisy_units.append(daisy_unit)

    def first_incomplete_daisy_unit(self, socket):
        daisy_units = self.domain_list(socket)
        for daisy_unit in daisy_units:
            if not daisy_unit.is_complete:
                return daisy_unit
        return None

    def add_socket(self, socket):
        daisy_unit = self.first_incomplete_daisy_unit(socket)
        if daisy_unit:
            socket.add_to_daisy_unit(daisy_unit)
            self.sockets.append(socket)
        return daisy_unit
