from models.gameMessage import GameMessage
from models.actionType import ActionType
from models.GameStates.IState import IState
from services.GetOnlyIntService import GetOnlyIntFromListService
class BetRoundState(IState): 
    players: list[str]
    bets: dict
    
    def __init__(
        self, 
        players, 
        callback,  
        game_instance             
    ):
        self.players_to_remove = []
        self.bets = {}
        
        self.players = players
        self.callback = callback
        self.game_instance = game_instance
        
        self.current_player_idx = 0
        
    async def _handle_message(self, player_id: str, message: GameMessage): 
        if message.action == ActionType.FOLD: 
            self.players_to_remove.append(player_id)
            
            self.bets[player_id] = "fold"
        if message.action == ActionType.RAISE: 
            self.bets[player_id] = message.data[0]
        int_bets = GetOnlyIntFromListService.clear(self.bets.values())        
            
        if message.action == ActionType.CALL: 
            if self.bets:
                self.bets[player_id] = max(list(int_bets))
            else: 
                self.bets[player_id] = 0
        check_to_winner = [player for player in self.players if self.bets.get(player, 0) != 'fold']
        if len(check_to_winner) == 1: 
            winner = check_to_winner
            await self.game_instance.to_end_game(winner, sum(int_bets))
            return
                        
        if len(self.bets) == len(self.players) and len(set(int_bets)) == 1: 
            for player in self.players_to_remove:
                self.players.remove(player)
            await self.callback(self.players, sum(int_bets))
            return
        
        message = GameMessage(
            self.bets, 
            ActionType.MAKE_BET
        )
        self.current_player_idx += 1
        self.current_player_idx %= len(self.players)
        player = self.players[self.current_player_idx]
        while self.bets.get(player, 0) == "fold": 
            self.current_player_idx += 1
            self.current_player_idx %= len(self.players)
            player = self.players[self.current_player_idx]
            
        await self.game_instance.send_message_to_player(player, message)
    