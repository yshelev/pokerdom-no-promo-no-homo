from network.clientSocket import ClientSocket
from models.gameMessage import GameMessage

class Player: 
    _socket: ClientSocket
    player_id: str
    
    def __init__(
        self,
        player_id: str, 
        host: str, 
        port: int
    ): 
        self._socket = ClientSocket(
            host, 
            port, 
            self.handle_message
        )
        self.player_id = player_id
                
        self._socket.start(player_id)
        
    def handle_message(self, message: GameMessage):
        ... 
        
    async def send_message(self, message: GameMessage): 
        ... 