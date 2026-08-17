import socket


class HTBClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port