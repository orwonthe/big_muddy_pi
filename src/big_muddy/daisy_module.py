from daisy_domain import DomainLists


class DaisyModule(DomainLists):
    """
    Daisy module is a named collection of daisy units.
    """

    def __init__(self, name, daisy_units=None):
        super().__init__()
        self._added_to_master = False
        self.name = name
        self.daisy_units = []  # Ordered according to hardware daisy sequence
        self.sockets = []
        if daisy_units:
            self.add_daisy_units(daisy_units)

    def add_to_master(self, daisy_master):
        """ One time call to add module to the daisy master. """
        if self._added_to_master:
            raise Exception("ERROR: Can only add once to daisy master. ")
        daisy_master.add_daisy_units(self.daisy_units)
        self._added_to_master = True

    def add_daisy_units(self, daisy_units):
        """ Add a list of daisy units to the module. """
        for daisy_unit in daisy_units:
            self.add_daisy_unit(daisy_unit)

    def add_daisy_unit(self, daisy_unit):
        """ Add a single daisy unit to the module: both in daisy sequence and also to specific domain list """
        self.append(daisy_unit)
        self.daisy_units.append(daisy_unit)

    def find_daisy_unit_and_index(self, socket, index_to_find=None):
        """
        Find the correct socket index and daisy unit for the socket

        returns index, daisy_unit
        """
        if index_to_find is None:
            index_to_find = socket.socket_index
        daisy_units = self.domain_list(socket)
        for daisy_unit in daisy_units:
            sockets_in_unit = daisy_unit.socket_count
            if index_to_find < sockets_in_unit:
                return index_to_find, daisy_unit
            else:
                index_to_find -= sockets_in_unit
        return index_to_find, None

    def add_sockets(self, sockets):
        for socket in sockets:
            self.add_socket(socket)

    def add_socket(self, socket):
        """ Find the proper socket location of the proper domain and add the socket there. """
        daisy_socket_index, daisy_unit = self.find_daisy_unit_and_index(socket)
        if daisy_unit:
            socket.add_to_daisy_unit(daisy_unit, daisy_socket_index)
            self.sockets.append(socket)
        return daisy_unit

    def reflect(self):
        """ Reflect all the sockets. """
        for socket in self.sockets:
            socket.reflect()
