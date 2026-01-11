from network.serverSocket import ServerSocket
from models.gameMessage import GameMessage


class Server: 
    _socket: ServerSocket
    connected_players: list = []
    
    def __init__(
        self, 
        host, 
        port, 
        on_ready, 
        handle_message_callback
    ):  
        self._handle_message_callback = handle_message_callback
        
        self.on_ready_callback = on_ready
        self._socket = ServerSocket(
            host, 
            port, 
            self.handle_message, 
            self.handle_connection
        )
        
        self._socket.start()
        
    async def handle_message(self, player_id: str, message: GameMessage): 
        await self._handle_message_callback(player_id, message)
        
    async def handle_connection(self, player_id: str): 
        print(player_id)
        if len(self.connected_players) < 2: 
            self.connected_players.append(player_id)
        
        if len(self.connected_players) == 2: 
            await self.on_ready_callback(self.connected_players)
        
    async def send_message_to_player(self, player_id: str, message: GameMessage): 
        await self._socket.send_to_player(player_id, message)