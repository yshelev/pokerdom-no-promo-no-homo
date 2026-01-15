from models.GameStates.IState import IState
from models.actionType import ActionType
from models.gameMessage import GameMessage


class PostGameState(IState):    
    def __init__(
        self, 
        players, 
        game_instance
    ):
        print("post game state rn")

        self.game_instance = game_instance
        self.players = players
        self.disconnected = []
        
        self.cur_idx = 0
        
    async def _handle_message(self, player_id, message: GameMessage):
        print("post game state handling msg")
        if message.action != ActionType.IS_READY:
            self.disconnected.append(player_id)
            
        self.cur_idx += 1
        if self.cur_idx == len(self.players): 
            await self.game_instance.remove_disconnected_players(self.disconnected)
            return
            
        message = GameMessage(
            [], 
            ActionType.ARE_YOU_READY
        )