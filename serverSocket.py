import asyncio
import pickle
from messageTypes import MessageTypes

class ServerSocket: 
    host: str
    port: int
    
    readers: dict[str, asyncio.StreamReader]
    writers: dict[str, asyncio.StreamWriter]
    def __init__(
        self,
        host: str,
        port: int, 
        on_message_receive: callable[[dict], None]
    ): 
        self.host = host
        self.port = port
        
    async def start(self):
        self.server_task = asyncio.create_task(self.run_server())
        
    async def run_server(self): 
        try: 
            server = await asyncio.start_server(
                self.handle_incoming_connections,
                self.host, 
                self.port 
            )
            
            async with server: 
                await server.serve_forever()
            
        except Exception as e: 
            print(e)
            
    async def handle_incoming_connections(
        self, 
        reader: asyncio.StreamReader, 
        writer: asyncio.StreamWriter
    ): 
        data = await reader.read(4096)
        if not data:
            return
        
        identification = pickle.loads(data) 
        player_id = identification.get('player_id')
        
        self.readers[player_id] = reader
        
        ack = {
                'type': MessageTypes.ACKNOWLEDGMENT,
                'player_id': self.player_id
        }
        writer.write(pickle.dumps(ack))
        await writer.drain()
        
        asyncio.create_task(self.receive_from_player(player_id, reader))
    
    async def receive_from_player(self, player_id: str, reader: asyncio.StreamReader):
        try:
            while True:
                data = await reader.read(4096)
                if not data:
                    break
                
                message = pickle.loads(data)
                await self.handle_message(player_id, message)
        finally:
            self.cleanup_connection(player_id)
        
    async def handle_message(self, from_player: str, message: dict):
        msg_type = message.get('type')
        
        # Обработка игровой логики... TODO??)))0
        
    def cleanup_connection(self, player_id: str):
        """Очистка соединения"""
        if player_id in self.writers:
            writer = self.writers[player_id]
            if not writer.is_closing():
                writer.close()
            del self.writers[player_id]
        
        if player_id in self.readers:
            del self.readers[player_id]