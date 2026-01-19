from models.GameStates.IState import IState
from models.gameMessage import GameMessage
from models.actionType import ActionType

class FlopState(IState): 
    def __init__(
        self, 
        players: list[str],
        game_instance
    ):
        self.players = players
        self.game_instance = game_instance
        self.start_pos = 0
        self.current_player = self.start_pos
        self.flag = False
        
    async def _handle_message(self, player_id, message: GameMessage):
        if self.current_player == self.start_pos and self.flag: 
            confirm_message = GameMessage(
                message.data, 
                ActionType.TAKE_TABLE_CARDS
            )
            
            for player in self.players: 
                await self.game_instance.send_message_to_player(
                    player, 
                    confirm_message
                )
            
            await self.game_instance.start_flop_bet_round()
            
            return
            
        cur_player = self.players[self.current_player]
        
        decode_message = GameMessage(
            message.data,     
            ActionType.DECODE
        )
        
        await self.game_instance.send_message_to_player(
            cur_player, 
            decode_message
        )
        
        self.current_player += 1
        self.current_player %= len(self.players)
        self.flag = True
        
        