from models.GameStates.IState import IState
from models.gameMessage import GameMessage
from services.bestHandFinder import BestHandFinder
from models.actionType import ActionType

class EndGameState(IState): 
    players: list[str]
    _best_hand_finder: BestHandFinder = BestHandFinder()
    
    def __init__(
        self, 
        players: list[str],
        game_instance 
    ):
        print("WHERE AM I")
        self.players = players
        self.game_instance = game_instance
        
        self.all_combinations = {}
        
    async def handle_message(self, player_id: str, message: GameMessage):
        self.all_combinations[player_id] = message.data
        print(self.all_combinations, self.players)
        if len(self.all_combinations) == len(self.players): 
            await self.get_best_hand()
            
    async def get_best_hand(self): 
        player_index = self._best_hand_finder.find_best_hand_index(self.all_combinations)
        
        final_message = GameMessage(
            [player_index], 
            ActionType.WINNER
        )
        
        for player in self.players: 
            await self.game_instance.send_message_to_player(
                player, 
                final_message
            )
            
            # gg)) 