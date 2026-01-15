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
        
        self._num_of_player_to_start = 2
        
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
        if len(self.connected_players) < self._num_of_player_to_start: 
            self.connected_players.append(player_id)
        
        if len(self.connected_players) == self._num_of_player_to_start: 
            await self.on_ready_callback(self.connected_players)
        
    async def send_message_to_player(self, player_id: str, message: GameMessage): 
        await self._socket.send_to_player(player_id, message)
        
    async def remove_disconnected_players(self, disconnected): 
        for player in disconnected: 
            self.connected_players.remove(player)
            
        if len(self.connected_players) == self._num_of_player_to_start: 
            await self.on_ready_callback(self.connected_players)