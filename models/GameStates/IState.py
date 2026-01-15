import asyncio

class IState: 
    state_lock = asyncio.Lock()
    
    async def handle_message(self, player_id: str, message: ...):
        async with self.state_lock: 
            await self._handle_message(player_id, message)
        
    async def _handle_message(self, player_id, message): 
        raise NotImplementedError
    
    