import socket
from dataclasses import dataclass

@dataclass
class Client: 
    socket_: socket.socket
    address: any