# Copyright 2022 WillyMillsLLC
from daisy_domain import BlockMixin, ConsoleMixin
from daisy_socket import DaisySocketOn8to16


class BlockServoTestingSocket(DaisySocketOn8to16, BlockMixin, ConsoleMixin):
    """ Test fixture uses 4 of these sockets """

    def __init__(self, socket_index):
        self.socket_index = socket_index
        super().__init__()
