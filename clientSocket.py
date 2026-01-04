import asyncio

class ClientSocket: 
    reader: asyncio.StreamReader 
    writer: asyncio.StreamWriter 
    
    def __init__(
        self,
        host: str,
        port: int, 
        on_message_receive: callable[[dict], None]
    ): 
        ... 