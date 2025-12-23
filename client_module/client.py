from config import ClientConfig
import socket

class ClientSocket: 
    _socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _client_config: ClientConfig = ClientConfig()
    
    def __init__(self):
        pass
    
    def start_connection(self): 
        self._socket.connect((
            self._client_config.address,
            self._client_config.port
        ))
        
    def release(self): 
        self._socket.close()