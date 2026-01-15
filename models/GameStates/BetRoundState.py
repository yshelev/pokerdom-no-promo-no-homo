from models.gameMessage import GameMessage
from models.actionType import ActionType
from models.GameStates.IState import IState
class BetRoundState(IState): 
    players: list[str]
    
    bets: dict
    
    def __init__(
        self, 
        players, 
        callback,  
        game_instance             
    ):
        self.bets = {}
        
        self.players = players
        self.callback = callback
        self.game_instance = game_instance
        
        self.current_player_idx = 0
        
    async def _handle_message(self, player_id: str, message: GameMessage): 
        if message.action == ActionType.FOLD: 
            self.players.remove(player_id)
            _ = self.bets.pop(player_id, None)
            
            self.current_player_idx %= len(self.players)
        if message.action == ActionType.RAISE: 
            self.bets[player_id] = message.data[0]
            
        if message.action == ActionType.CALL: 
            if self.bets:
                self.bets[player_id] = max(list(self.bets.values()))
            else: 
                self.bets[player_id] = 0
        if len(self.players) == 1: 
            await self.game_instance.to_end_game(self.players)
            return
            
        if len(self.bets) == len(self.players) and len(set(self.bets.values())) == 1: 
            await self.callback(self.players)
            return
        
        message = GameMessage(
            self.bets, 
            ActionType.MAKE_BET
        )
        self.current_player_idx += 1
        self.current_player_idx %= len(self.players)
        player = self.players[self.current_player_idx]
        
        await self.game_instance.send_message_to_player(player, message)
    