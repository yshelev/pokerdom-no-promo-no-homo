import asyncio
import pickle
from models.gameMessage import GameMessage
from typing import Callable

class ClientSocket: 
    reader: asyncio.StreamReader 
    writer: asyncio.StreamWriter 
    
    def __init__(
        self,
        host: str,
        port: int, 
        on_message_receive: Callable[[GameMessage], None]
    ): 
        self.host = host
        self.port = port
        self.callback = on_message_receive
    
    def start(self, player_id: str):
        self.client_task = asyncio.create_task(self.connect_to_game(player_id))
        
    async def connect_to_game(self, player_id: str): 
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        asyncio.create_task(self.receive_message())
        await self.send_message({
            "player_id": player_id
        }) 
        
    async def receive_message(self): 
        try:
            while True: 
                data = await self.reader.read(1024)
                if not data:
                    continue
                
                message = pickle.loads(data)
                
                await self.callback(message)
        except (ConnectionError, asyncio.CancelledError):
            return
        
    async def send_message(self, message_dict): 
        try:
            pickled_data = pickle.dumps(message_dict)
            
            self.writer.write(pickled_data)
            await self.writer.drain()
            
            return True
        except Exception as e:
            return False