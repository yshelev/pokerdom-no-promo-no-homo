from models.GameStates.IState import IState
from models.gameMessage import GameMessage
from models.actionType import ActionType

class InitialState(IState): 
    def __init__(self,
        players: list[str],
        game_instance
    ):
        print("initial state")
        
        super().__init__()
        
        self.players = players

        self.start_player = 1
        self.current_player = self.start_player
        
        self.game_instance = game_instance
        
        print(self.players)
    
    async def handle_message(self, player_id: str, message: GameMessage): 
        print("handling message")
        data = message.data
        
        if self.current_player >= len(self.players): 
            await self.game_instance.start_dealing_cards(
                data, 
                self.players
            )
            return  
            
        cur_player = self.players[self.current_player]
        
        
        message_to_player = GameMessage(
            data=data,
            action=ActionType.ENCODE
        )
        
        await self.game_instance.send_message_to_player(
            cur_player, 
            message_to_player,
        )
        
        self.current_player += 1