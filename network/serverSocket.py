import asyncio
import pickle
from models.messageTypes import MessageTypes
from typing import Callable
from models.actionType import ActionType
from models.gameMessage import GameMessage
from services.generator import Generator

class ServerSocket: 
    host: str
    port: int
    
    readers: dict[str, asyncio.StreamReader] = {}
    writers: dict[str, asyncio.StreamWriter] = {}
    
    public_key: int = Generator.generate_large_prime()
    
    def __init__(
        self,
        host: str,
        port: int, 
        on_message_receive: Callable[[dict], None], 
        on_connection_received: Callable[[str], None]
    ): 
        self.host = host
        self.port = port
        self.on_connection_received_callback = on_connection_received
        self.callback = on_message_receive
    
    def start(self):
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
            print("no data")
            return
        
        identification = pickle.loads(data) 
        player_id = identification.get('player_id')
        
        self.readers[player_id] = reader
        self.writers[player_id] = writer
        
        ack = GameMessage(
            [self.public_key],
            ActionType.ACKNOWLEDGMENT, 
        )

        writer.write(pickle.dumps(ack))
        await writer.drain()
        
        asyncio.create_task(self.receive_from_player(player_id, reader))
        
        await self.on_connection_received_callback(player_id)
        
    
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
        
    async def handle_message(self, player_id: str, message: GameMessage):
        await self.callback(player_id, message)
        
    def cleanup_connection(self, player_id: str):
        if player_id in self.writers:
            writer = self.writers[player_id]
            if not writer.is_closing():
                writer.close()
            del self.writers[player_id]
        
        if player_id in self.readers:
            del self.readers[player_id]
            
    async def send_to_player(self, player_id: str, message): 
        writer = self.writers[player_id]
        data = pickle.dumps(message)
        writer.write(data)
        await writer.drain()
        
        