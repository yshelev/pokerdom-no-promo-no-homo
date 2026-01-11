class IState: 
    async def handle_message(self, player_id: str, message: ...):
        raise NotImplementedError
    
    