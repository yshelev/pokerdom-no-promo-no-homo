from server import ServerSocket
from decoder import Decoder
from encoder import Encoder 

class Table: 
    _socket: ServerSocket = None
    _encoder: Encoder = None
    _decoder: Decoder = None
    
    def __init__(
        self, 
        server_socket: ServerSocket
    ):
        self._socket = server_socket
    
    def get_deck_from_user(): 