# Copyright 2022 WillyMillsLLC

class Servo:
    def __init__(self, daisy_module, socket_collection, client_collection):
        self.daisy_module = daisy_module
        self.socket_collection = socket_collection
        self.client_collection = client_collection
