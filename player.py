from clientSocket import ClientSocket
from serverSocket import ServerSocket

class Player: 
    _server_socket: ServerSocket
    _client_socket: ClientSocket
    
    def __init__(
        self, 
        player_id, 
        host, 
        port
    ): 
        self._server_socket = ServerSocket(host, port)