from network.serverSocket import ServerSocket
from models.gameMessage import GameMessage

class Server: 
    _socket: ServerSocket
    connected_players: list = []
    def __init__(
        self, 
        host, 
        port, 
        on_ready
    ): 
        self.on_ready_callback = on_ready
        self._socket = ServerSocket(
            host, 
            port, 
            self.handle_message, 
            self.handle_connection
        )
        
        self._socket.start()
        
    def handle_message(self, message: GameMessage): 
        print(message)
        
    def handle_connection(self, player_id: str): 
        if len(self.connected_players) < 4: 
            self.connected_players.append(player_id)
        
        if len(self.connected_players) == 4: 
            self.on_ready_callback(self.connected_players)
        
    def send_message_to_player(self, player_id: str, message: GameMessage): 
        ...